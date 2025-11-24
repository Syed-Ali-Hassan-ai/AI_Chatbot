# Deployment Guide - CFO Chatbot

This guide explains how to deploy and run the CFO chatbot locally.

## For End Users (Client)

### What You Need

1. **Python 3.9+** installed on your system
   - Check: `python3 --version` or `python --version`
   - Download from: https://www.python.org/downloads/

2. **OpenAI API Key**
   - Get one at: https://platform.openai.com/api-keys
   - You'll need billing set up (~$1-5 for typical usage)

3. **Source PDF Documents**
   - Global Financial Architecture Assignment document
   - Architecture Diagram PDF
   - These should be provided separately

### Installation Steps

#### 1. Download/Extract the Project

```bash
# If you received a ZIP file, extract it
unzip AI_Chatbot.zip
cd AI_Chatbot

# Or if cloning from git
git clone <repository-url>
cd AI_Chatbot
```

#### 2. Create Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages. Takes 1-2 minutes.

#### 4. Configure API Key

```bash
# Copy the template
cp .env.example .env

# Edit .env file
# On macOS/Linux:
nano .env

# On Windows:
notepad .env
```

Replace `your_api_key_here` with your actual OpenAI API key:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
```

Save and close the file.

#### 5. Add PDF Documents

Copy your PDF files to the `data/` directory:

```bash
# The files MUST be named exactly:
data/assignment.pdf
data/diagram.pdf
```

**Important**: If your PDFs have different names, rename them to match the above.

#### 6. Verify Setup (Optional)

```bash
python test_setup.py
```

This will check that everything is configured correctly.

#### 7. Run the Application

```bash
streamlit run app.py
```

The browser should open automatically at `http://localhost:8501`.

If it doesn't, open your browser and go to: `http://localhost:8501`

### First Run

The first time you run the application:
- It will process the PDF files (30-60 seconds)
- Create embeddings and vector store
- This data is cached for future runs

Subsequent runs will start instantly.

### Using the Application

1. **Ask Questions**: Type in the chat input at the bottom
2. **View Sources**: Click "📚 View Sources" to see citations
3. **Clear Chat**: Use the "🔄 Clear Conversation" button in sidebar
4. **Example Questions**: Click any example in the sidebar

### Stopping the Application

Press `Ctrl+C` in the terminal where Streamlit is running.

## For Developers

### Project Structure

```
AI_Chatbot/
├── app.py              # Streamlit UI
├── rag_engine.py       # RAG implementation
├── prompts.py          # CFO persona and prompts
├── config.py           # Configuration management
├── test_setup.py       # Setup validation script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .gitignore          # Git ignore rules
├── README.md           # Full documentation
├── QUICKSTART.md       # Quick start guide
├── DEPLOYMENT.md       # This file
└── data/               # PDF documents directory
    └── README.md       # Data directory guide
```

### Development Setup

```bash
# Clone repository
git clone <repo-url>
cd AI_Chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API key

# Add PDF files to data/
cp /path/to/assignment.pdf data/
cp /path/to/diagram.pdf data/

# Run validation
python test_setup.py

# Start development server
streamlit run app.py
```

### Customization

**Change the LLM Model:**
Edit `.env`:
```
OPENAI_MODEL=gpt-3.5-turbo  # Faster, cheaper
OPENAI_MODEL=gpt-4o          # Latest model
```

**Adjust Temperature:**
Edit `.env`:
```
OPENAI_TEMPERATURE=0.0   # More deterministic
OPENAI_TEMPERATURE=0.3   # More creative
```

**Change Retrieval Settings:**
Edit `.env`:
```
CHUNK_SIZE=500          # Smaller chunks
RETRIEVAL_K=10          # Retrieve more context
```

**Modify CFO Persona:**
Edit `prompts.py` and change the `SYSTEM_PROMPT`.

### Rebuilding Vector Store

If you update the PDF files:

```bash
# Delete cached vector store
rm -rf vector_store/

# Restart the app - it will rebuild automatically
streamlit run app.py
```

### Running in Production

For production deployment:

1. **Use Environment Variables** (not `.env` file)
   ```bash
   export OPENAI_API_KEY=sk-...
   streamlit run app.py
   ```

2. **Set Production Port**
   ```bash
   streamlit run app.py --server.port 8080
   ```

3. **Disable Development Features**
   ```bash
   streamlit run app.py --server.headless true
   ```

4. **Use HTTPS** (if exposing to internet)
   - Set up reverse proxy (nginx, Apache)
   - Use SSL certificates
   - Consider authentication

### Monitoring

View Streamlit logs:
```bash
# Logs appear in terminal where you ran streamlit
# For file logging:
streamlit run app.py 2>&1 | tee app.log
```

### Troubleshooting

**Dependencies Won't Install:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Then try again
pip install -r requirements.txt
```

**Port Already in Use:**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

**Memory Issues:**
```bash
# Reduce chunk size and retrieval count in .env
CHUNK_SIZE=500
RETRIEVAL_K=3
```

## Security Considerations

### API Key Security

- **NEVER** commit `.env` file to git
- **NEVER** share your API key publicly
- Use environment variables in production
- Rotate keys periodically

### PDF Document Security

- PDF files may contain sensitive financial data
- Consider adding `data/*.pdf` to `.gitignore` if needed
- Ensure proper access controls on the server

### Access Control

This application has NO authentication by default.

For production:
- Implement authentication (Streamlit Cloud, OAuth, etc.)
- Use reverse proxy with authentication
- Restrict network access
- Consider containerization (Docker)

## Cost Estimation

### OpenAI API Costs (Approximate)

**One-time Setup:**
- Embedding generation: $0.10 - $0.50 (depends on PDF size)

**Per Session:**
- Average query: $0.01 - $0.05
- 20 questions: ~$0.20 - $1.00

**Monthly (100 sessions):**
- Estimated: $20 - $100 (depends on usage)

**Cost Optimization:**
- Use `gpt-4-turbo` instead of `gpt-4` (50% cheaper)
- Use `gpt-3.5-turbo` for testing (90% cheaper)
- Cache vector store (avoid re-embedding)
- Reduce `RETRIEVAL_K` to minimize context

## Support

For issues:
1. Run `python test_setup.py` to diagnose
2. Check logs in terminal
3. Review README.md troubleshooting section
4. Verify Python version (3.9+)
5. Ensure all dependencies are installed

## License

Provided as-is for client use. All rights reserved.

---

**Ready to Deploy?**

1. ✅ Python 3.9+ installed
2. ✅ Dependencies installed (`pip install -r requirements.txt`)
3. ✅ API key configured (`.env` file)
4. ✅ PDF files in `data/` directory
5. ✅ Run `streamlit run app.py`

You're all set! 🚀
