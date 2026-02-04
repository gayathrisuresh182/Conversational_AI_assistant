# Conversational AI Assistant

A production-ready, general-purpose conversational AI assistant with personalized memory, custom knowledge base, and multi-capability tool integration.

## Features

- 🤖 **AI-Powered Conversations**: Powered by Claude Sonnet 4.5 via Anthropic API
- 💾 **Personalized Memory**: Remembers user preferences and past conversations
- 📚 **Custom Knowledge Base**: RAG system for querying uploaded documents
- 🔍 **Web Search**: Real-time internet search capabilities
- 🧮 **Calculator**: Built-in mathematical computation
- ☁️ **Cloud-Ready**: Designed for AWS deployment (Lambda, API Gateway, RDS, Pinecone)

## Architecture

```
USER ↔ FRONTEND (React) ↔ BACKEND (FastAPI) ↔ AI BRAIN (Claude) ↔ CAPABILITIES
```

### Components

1. **Frontend**: React-based chat interface with real-time updates
2. **Backend**: FastAPI server with WebSocket support for real-time communication
3. **AI Brain**: Claude Sonnet 4.5 with function calling capabilities
4. **Capabilities**:
   - Web Search (Tavily/SerpAPI)
   - Calculator
   - Knowledge Base (RAG with vector embeddings)
   - Preference Memory (PostgreSQL)
   - Long-term Memory (Vector database)

## Project Structure

```
Conversational_AI_assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models/              # Database models
│   │   ├── services/            # Business logic
│   │   │   ├── ai_assistant.py  # Core AI assistant
│   │   │   ├── tools/           # Tool implementations
│   │   │   └── memory/          # Memory management
│   │   ├── api/                 # API routes
│   │   └── config.py            # Configuration
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (for preferences)
- Pinecone account (for vector database) or local vector DB
- Anthropic API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

5. Run database migrations (if needed):
```bash
# Setup will be handled automatically on first run
```

6. Start the server:
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your backend API URL
```

4. Start the development server:
```bash
npm start
```

## Environment Variables

### Backend (.env)

```env
# Anthropic API
ANTHROPIC_API_KEY=your_anthropic_api_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_assistant

# Vector Database (Pinecone)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_environment
PINECONE_INDEX_NAME=ai-assistant-index

# Web Search API (Tavily)
TAVILY_API_KEY=your_tavily_api_key

# Server
PORT=8000
ENVIRONMENT=development
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## Usage

1. Start both backend and frontend servers
2. Open the frontend in your browser (typically http://localhost:3000)
3. Start chatting! The assistant will:
   - Remember your preferences
   - Search the web when needed
   - Answer questions about uploaded documents
   - Maintain conversation context

## Example Interactions

**Basic Conversation:**
```
User: "Hi, I'm Sarah"
Assistant: "Hello Sarah! Nice to meet you. How can I help you today?"
```

**Document Query:**
```
User: "What's in my resume and does it mention AI experience?"
Assistant: [Searches uploaded resume and provides detailed answer]
```

**Web Search:**
```
User: "What's the weather in Boston?"
Assistant: [Searches web and provides current weather]
```

**Memory Recall:**
```
User: "What did I tell you about my interests?"
Assistant: [Recalls from long-term memory]
```

## Deployment

This project is designed for AWS deployment:

- **Frontend**: CloudFront + S3
- **Backend**: Lambda/App Runner + API Gateway
- **Database**: RDS (PostgreSQL)
- **Vector DB**: Pinecone (managed service)

See deployment documentation for detailed instructions.

## Technologies

- **Backend**: FastAPI, Python 3.10+
- **Frontend**: React 18+
- **AI**: Anthropic Claude 3.5 Sonnet API
- **Database**: PostgreSQL (for structured data)
- **Vector DB**: Pinecone (for embeddings and semantic search)
- **Search**: Tavily API (for web search)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Deployment**: AWS (Lambda, API Gateway, RDS, CloudFront, S3)

## License

See LICENSE file for details.

## Contributing

This is a personal project for learning and showcasing skills. Feel free to fork and adapt for your own use!

