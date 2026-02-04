"""Core AI Assistant service with Claude integration."""
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
from sqlalchemy.orm import Session
from app.config import settings
from app.services.tools import (
    WebSearchTool,
    CalculatorTool,
    KnowledgeBaseTool,
    PreferenceMemoryTool
)
from app.services.memory import LongTermMemory
from app.models.user import User
from app.models.conversation import Conversation, Message
import uuid
import json


class AIAssistant:
    """Main AI Assistant that coordinates Claude and tools."""
    
    def __init__(self, user_id: str, db: Session):
        self.user_id = user_id
        self.db = db
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        
        # Initialize tools
        self.web_search = WebSearchTool()
        self.calculator = CalculatorTool()
        self.knowledge_base = KnowledgeBaseTool()
        self.preference_memory = PreferenceMemoryTool()
        self.long_term_memory = LongTermMemory()
        
        # Get or create user
        self.user = self._get_or_create_user()
    
    def _get_or_create_user(self) -> User:
        """Get existing user or create new one."""
        user = self.db.query(User).filter(User.id == uuid.UUID(self.user_id)).first()
        if not user:
            user = User(id=uuid.UUID(self.user_id))
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def get_conversation_history(self, conversation_id: str, limit: int = 20) -> List[Dict[str, str]]:
        """Get conversation history for context."""
        messages = self.db.query(Message).filter(
            Message.conversation_id == uuid.UUID(conversation_id)
        ).order_by(Message.sequence_number.desc()).limit(limit).all()
        
        # Reverse to get chronological order
        messages.reverse()
        
        history = []
        for msg in messages:
            history.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return history
    
    def get_system_prompt(self) -> str:
        """Generate system prompt with available tools."""
        return """You are a helpful, intelligent AI assistant with access to various tools and capabilities.

You can help users with:
1. Answering questions using your knowledge
2. Searching the web for current information
3. Performing calculations
4. Searching through user's uploaded documents
5. Remembering user preferences and personal information
6. Recalling past conversations

When a user asks a question:
- If it requires current/recent information → use web_search
- If it requires math → use calculator
- If it's about their documents → use search_knowledge_base
- If they share personal info → use save_preference
- If you need to recall something about them → use get_preference

Be conversational, helpful, and proactive. Remember user preferences and use them to personalize responses."""
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get all available tool definitions."""
        return [
            self.web_search.get_tool_definition(),
            self.calculator.get_tool_definition(),
            self.knowledge_base.get_tool_definition(),
            self.preference_memory.get_tool_definition(),
            self.preference_memory.get_save_tool_definition(),
        ]
    
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call."""
        if tool_name == "web_search":
            return self.web_search.search(
                query=tool_input.get("query", ""),
                max_results=tool_input.get("max_results", 5)
            )
        
        elif tool_name == "calculator":
            return self.calculator.calculate(
                expression=tool_input.get("expression", "")
            )
        
        elif tool_name == "search_knowledge_base":
            return self.knowledge_base.search(
                query=tool_input.get("query", ""),
                user_id=self.user_id,
                top_k=tool_input.get("top_k", 5)
            )
        
        elif tool_name == "get_preference":
            value = self.preference_memory.get_preference(
                user_id=self.user_id,
                key=tool_input.get("key", ""),
                db=self.db
            )
            return {"key": tool_input.get("key", ""), "value": value}
        
        elif tool_name == "save_preference":
            success = self.preference_memory.save_preference(
                user_id=self.user_id,
                key=tool_input.get("key", ""),
                value=tool_input.get("value", ""),
                db=self.db
            )
            return {"success": success, "key": tool_input.get("key", ""), "value": tool_input.get("value", "")}
        
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def process_message(
        self,
        message: str,
        conversation_id: str,
        include_memories: bool = True
    ) -> Dict[str, Any]:
        """
        Process a user message and generate response.
        
        Args:
            message: User message
            conversation_id: Conversation ID
            include_memories: Whether to include relevant past memories
            
        Returns:
            Response dictionary with assistant message and metadata
        """
        # Get conversation history
        history = self.get_conversation_history(conversation_id)
        
        # Optionally search for relevant past memories
        relevant_memories = []
        if include_memories:
            memories = self.long_term_memory.search_memories(
                user_id=self.user_id,
                query=message,
                top_k=3
            )
            relevant_memories = [m["text"] for m in memories if m["score"] > 0.7]
        
        # Build messages for Claude
        messages = []
        
        # Add relevant memories if any
        if relevant_memories:
            memory_context = "\n\nRelevant past conversations:\n" + "\n".join(f"- {m}" for m in relevant_memories)
            messages.append({
                "role": "user",
                "content": memory_context
            })
        
        # Add conversation history
        for msg in history[-10:]:  # Last 10 messages for context
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Call Claude with function calling
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Claude 3.5 Sonnet
                max_tokens=4096,
                system=self.get_system_prompt(),
                messages=messages,
                tools=self.get_tools()
            )
            
            # Handle tool calls if any
            tool_results = []
            final_response = None
            tool_use_blocks = []
            
            # Process response
            for content_block in response.content:
                if content_block.type == "text":
                    final_response = content_block.text
                elif content_block.type == "tool_use":
                    tool_use_blocks.append(content_block)
                    # Execute tool
                    tool_result = self.execute_tool(
                        tool_name=content_block.name,
                        tool_input=content_block.input
                    )
                    tool_results.append({
                        "tool_use_id": content_block.id,
                        "tool": content_block.name,
                        "input": content_block.input,
                        "result": tool_result
                    })
            
            # If tools were called, send results back to Claude for final response
            if tool_results:
                # Build tool result messages
                tool_result_messages = []
                for tool_result in tool_results:
                    tool_result_messages.append({
                        "type": "tool_result",
                        "tool_use_id": tool_result["tool_use_id"],
                        "content": json.dumps(tool_result["result"], indent=2)
                    })
                
                # Append assistant message with tool use and tool results
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                messages.extend(tool_result_messages)
                
                # Get final response with tool results
                final_response_obj = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4096,
                    system=self.get_system_prompt(),
                    messages=messages
                )
                
                # Extract final text response
                final_response = None
                for content_block in final_response_obj.content:
                    if content_block.type == "text":
                        final_response = content_block.text
            
            # Store memory of this interaction
            if include_memories:
                memory_text = f"User: {message}\nAssistant: {final_response}"
                self.long_term_memory.store_memory(
                    user_id=self.user_id,
                    conversation_text=memory_text,
                    metadata={"conversation_id": conversation_id}
                )
            
            return {
                "response": final_response or "I apologize, but I couldn't generate a response.",
                "tool_calls": tool_results,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            return {
                "error": f"Error processing message: {str(e)}",
                "response": "I'm sorry, I encountered an error processing your message. Please try again.",
                "conversation_id": conversation_id
            }

