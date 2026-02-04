"""Chat API routes."""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.models.base import get_db
from app.models.conversation import Conversation, Message
from app.services.ai_assistant import AIAssistant
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    """Chat message request model."""
    user_id: str
    conversation_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    conversation_id: str
    tool_calls: Optional[list] = None


@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_message: ChatMessage,
    db: Session = Depends(get_db)
):
    """Send a message to the AI assistant."""
    try:
        # Get or create conversation
        if chat_message.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == uuid.UUID(chat_message.conversation_id)
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=uuid.UUID(chat_message.user_id),
                title=chat_message.message[:100]  # Use first 100 chars as title
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=chat_message.message,
            sequence_number=len(conversation.messages) + 1
        )
        db.add(user_message)
        db.commit()
        
        # Initialize AI assistant
        assistant = AIAssistant(user_id=chat_message.user_id, db=db)
        
        # Process message
        result = assistant.process_message(
            message=chat_message.message,
            conversation_id=str(conversation.id)
        )
        
        # Save assistant response
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=result["response"],
            tool_calls=result.get("tool_calls"),
            sequence_number=len(conversation.messages) + 2
        )
        db.add(assistant_message)
        db.commit()
        
        return ChatResponse(
            response=result["response"],
            conversation_id=str(conversation.id),
            tool_calls=result.get("tool_calls")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{user_id}")
async def get_conversations(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all conversations for a user."""
    try:
        conversations = db.query(Conversation).filter(
            Conversation.user_id == uuid.UUID(user_id)
        ).order_by(Conversation.updated_at.desc()).all()
        
        return [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "message_count": len(conv.messages)
            }
            for conv in conversations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation."""
    try:
        messages = db.query(Message).filter(
            Message.conversation_id == uuid.UUID(conversation_id)
        ).order_by(Message.sequence_number).all()
        
        return [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "tool_calls": msg.tool_calls,
                "created_at": msg.created_at.isoformat(),
                "sequence_number": msg.sequence_number
            }
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            user_id = data.get("user_id")
            conversation_id = data.get("conversation_id")
            message = data.get("message")
            
            if not user_id or not message:
                await websocket.send_json({"error": "Missing user_id or message"})
                continue
            
            # Get or create conversation
            if conversation_id:
                conversation = db.query(Conversation).filter(
                    Conversation.id == uuid.UUID(conversation_id)
                ).first()
            else:
                conversation = Conversation(
                    user_id=uuid.UUID(user_id),
                    title=message[:100]
                )
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
            
            # Save user message
            user_msg = Message(
                conversation_id=conversation.id,
                role="user",
                content=message,
                sequence_number=len(conversation.messages) + 1
            )
            db.add(user_msg)
            db.commit()
            
            # Process with AI
            assistant = AIAssistant(user_id=user_id, db=db)
            result = assistant.process_message(
                message=message,
                conversation_id=str(conversation.id)
            )
            
            # Save assistant response
            assistant_msg = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=result["response"],
                tool_calls=result.get("tool_calls"),
                sequence_number=len(conversation.messages) + 2
            )
            db.add(assistant_msg)
            db.commit()
            
            # Send response
            await websocket.send_json({
                "response": result["response"],
                "conversation_id": str(conversation.id),
                "tool_calls": result.get("tool_calls")
            })
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})

