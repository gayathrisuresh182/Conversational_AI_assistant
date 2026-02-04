# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Check

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL installed and running
- [ ] API keys ready (Anthropic, Pinecone, Tavily)

## Quick Setup

### 1. Backend (2 minutes)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

# Create .env file with your API keys
# Copy from .env.example and fill in your keys

python setup_database.py
uvicorn app.main:app --reload
```

### 2. Frontend (2 minutes)

```bash
cd frontend
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

npm start
```

### 3. Test It! (1 minute)

1. Open http://localhost:3000
2. Type: "Hello, my name is [Your Name]"
3. Then ask: "What's my name?"
4. Upload a PDF and ask about it!

## Common Issues

**"Module not found"** → Activate venv and reinstall: `pip install -r requirements.txt`

**"Database connection failed"** → Check PostgreSQL is running and DATABASE_URL is correct

**"API key error"** → Verify keys in `.env` file (not `.env.example`)

**"Port already in use"** → Change PORT in backend `.env` or use different port

## Next Steps

- Read [SETUP.md](SETUP.md) for detailed setup
- Read [README.md](README.md) for architecture details
- Check `/api/docs` for API documentation

## Need Help?

Check the troubleshooting section in [SETUP.md](SETUP.md)

