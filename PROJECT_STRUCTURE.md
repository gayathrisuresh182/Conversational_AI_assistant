# Project Structure

This document explains the organization of the Conversational AI Assistant project.

## Directory Structure

```
Conversational_AI_assistant/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py          # Configuration management
│   │   ├── models/            # Database models
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Base database setup
│   │   │   ├── user.py        # User and preferences
│   │   │   ├── conversation.py # Conversations and messages
│   │   │   └── document.py    # Documents and chunks
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── ai_assistant.py # Core AI assistant
│   │   │   ├── tools/         # Tool implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── web_search.py
│   │   │   │   ├── calculator.py
│   │   │   │   ├── knowledge_base.py # RAG tool
│   │   │   │   └── preference_memory.py
│   │   │   └── memory/        # Memory management
│   │   │       ├── __init__.py
│   │   │       └── long_term_memory.py
│   │   └── api/               # API routes
│   │       ├── __init__.py
│   │       ├── chat.py        # Chat endpoints
│   │       └── documents.py   # Document upload endpoints
│   ├── requirements.txt       # Python dependencies
│   ├── setup_database.py      # Database setup script
│   └── .env.example           # Environment variables template
│
├── frontend/                  # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx            # Main app component
│   │   ├── App.css
│   │   ├── index.js           # React entry point
│   │   ├── index.css
│   │   ├── components/        # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── ChatInterface.css
│   │   │   ├── MessageList.jsx
│   │   │   ├── MessageList.css
│   │   │   ├── Message.jsx
│   │   │   ├── Message.css
│   │   │   ├── MessageInput.jsx
│   │   │   ├── MessageInput.css
│   │   │   ├── DocumentUpload.jsx
│   │   │   └── DocumentUpload.css
│   │   └── services/
│   │       └── api.js          # API client
│   ├── package.json
│   └── .env.example
│
├── README.md                   # Main project documentation
├── SETUP.md                    # Detailed setup guide
├── QUICKSTART.md              # Quick start guide
├── PROJECT_STRUCTURE.md       # This file
└── .gitignore                 # Git ignore rules
```

## Key Components

### Backend (`backend/`)

**Models** (`app/models/`):
- `User`: User accounts
- `UserPreference`: Structured memory (key-value pairs)
- `Conversation`: Chat sessions
- `Message`: Individual messages in conversations
- `Document`: Uploaded files
- `DocumentChunk`: Text chunks for RAG

**Services** (`app/services/`):
- `ai_assistant.py`: Main orchestrator that:
  - Manages conversation context
  - Coordinates with Claude API
  - Handles tool calling
  - Manages memory systems

**Tools** (`app/services/tools/`):
- `web_search.py`: Tavily API integration
- `calculator.py`: Safe math evaluation
- `knowledge_base.py`: RAG with Pinecone
- `preference_memory.py`: PostgreSQL preference storage

**Memory** (`app/services/memory/`):
- `long_term_memory.py`: Semantic search of past conversations

**API** (`app/api/`):
- `chat.py`: REST and WebSocket chat endpoints
- `documents.py`: File upload and management

### Frontend (`frontend/`)

**Components**:
- `ChatInterface`: Main chat container
- `MessageList`: Displays conversation history
- `Message`: Individual message bubble
- `MessageInput`: Text input with send button
- `DocumentUpload`: File upload button

**Services**:
- `api.js`: Axios-based API client

## Data Flow

1. **User sends message** → `ChatInterface` → `api.js` → Backend `/api/chat/message`
2. **Backend receives** → `chat.py` → Creates/updates conversation
3. **AI processing** → `ai_assistant.py` → Calls Claude API with tools
4. **Tool execution** → Individual tool classes → Return results
5. **Claude generates response** → Backend saves to database
6. **Response sent** → Frontend displays in `MessageList`

## Memory Systems

1. **Short-term**: Conversation history in `Message` table
2. **Structured**: User preferences in `UserPreference` table
3. **Long-term**: Semantic memories in Pinecone vector DB
4. **Knowledge Base**: Document chunks in Pinecone vector DB

## Extension Points

To add new capabilities:

1. **New Tool**: Create class in `app/services/tools/` with:
   - `execute()` method
   - `get_tool_definition()` method
   - Register in `ai_assistant.py`

2. **New API Endpoint**: Add route in `app/api/` and register in `main.py`

3. **New Frontend Feature**: Add component in `frontend/src/components/`

## Configuration

All configuration via environment variables:
- Backend: `backend/.env`
- Frontend: `frontend/.env`

See `.env.example` files for required variables.

