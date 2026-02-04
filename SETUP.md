# Setup Guide

This guide will help you set up the Conversational AI Assistant project from scratch.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.10+** installed
2. **Node.js 18+** and npm installed
3. **PostgreSQL** installed and running
4. **API Keys** for:
   - Anthropic (Claude API)
   - Pinecone (Vector database)
   - Tavily (Web search)

## Step 1: Clone and Navigate

```bash
cd Conversational_AI_assistant
```

## Step 2: Backend Setup

### 2.1 Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.3 Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# Anthropic API (Get from https://console.anthropic.com/)
ANTHROPIC_API_KEY=sk-ant-...

# Database (Create a PostgreSQL database first)
DATABASE_URL=postgresql://username:password@localhost:5432/ai_assistant

# Pinecone (Get from https://www.pinecone.io/)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=ai-assistant-index

# Tavily (Get from https://tavily.com/)
TAVILY_API_KEY=your_tavily_api_key

# Server
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 2.4 Set Up Database

1. Create a PostgreSQL database:
```sql
CREATE DATABASE ai_assistant;
```

2. Run the setup script:
```bash
python setup_database.py
```

This will create all necessary tables.

### 2.5 Start Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

The backend should now be running at `http://localhost:8000`

## Step 3: Frontend Setup

### 3.1 Install Dependencies

Open a new terminal:

```bash
cd frontend
npm install
```

### 3.2 Set Up Environment Variables

Create a `.env` file in the `frontend` directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

### 3.3 Start Frontend Server

```bash
npm start
```

The frontend should open at `http://localhost:3000`

## Step 4: Verify Setup

1. **Backend Health Check**: Visit `http://localhost:8000/health`
   - Should return: `{"status": "healthy"}`

2. **Frontend**: Open `http://localhost:3000`
   - Should see the chat interface

3. **Test a Message**: Type "Hello" and send
   - Should receive a response from Claude

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running: `pg_isready` or check services
- Verify DATABASE_URL format: `postgresql://user:pass@host:port/dbname`
- Check database exists: `psql -l` to list databases

### Pinecone Issues

- Sign up at https://www.pinecone.io/
- Create an index (will be auto-created on first use)
- Verify API key is correct

### API Key Issues

- **Anthropic**: Get from https://console.anthropic.com/
- **Tavily**: Sign up at https://tavily.com/ for free tier
- Ensure keys are in `.env` file (not `.env.example`)

### Port Already in Use

- Backend: Change `PORT` in `.env` or use `--port 8001`
- Frontend: React will prompt to use a different port

### Module Not Found Errors

- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.10+)

## Next Steps

1. **Upload a Document**: Click the document icon and upload a PDF
2. **Ask About Document**: "What's in my document?"
3. **Test Web Search**: "What's the weather today?"
4. **Test Calculator**: "What's 25% of 1000?"
5. **Test Memory**: Tell it your name, then ask "What's my name?"

## Development Tips

- Backend auto-reloads on file changes (--reload flag)
- Frontend hot-reloads automatically
- Check browser console for frontend errors
- Check terminal for backend errors
- Use `/api/docs` for API documentation (Swagger UI)

## Production Deployment

For production deployment to AWS:

1. Set up RDS PostgreSQL instance
2. Set up Pinecone (already cloud-based)
3. Deploy backend to Lambda/App Runner
4. Deploy frontend to S3 + CloudFront
5. Configure API Gateway
6. Update environment variables for production

See README.md for more deployment details.

