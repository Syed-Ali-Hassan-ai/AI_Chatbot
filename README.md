# CFO Bot - Global Financial Architecture

A production-ready Streamlit-based RAG chatbot that acts as the Chief Financial Officer (CFO) for a multinational corporate group. The bot provides expert guidance on financial instruments, tax optimization, compliance strategies, and operational mechanics based strictly on provided source documents.

## 🎯 Overview

This CFO chatbot uses Retrieval Augmented Generation (RAG) to answer questions about a global financial architecture spanning:
- 🇺🇸 **US Parent** - IP holder, loss-making (pre-BEP)
- 🇰🇷 **Korea Sub** - R&D center with cash surplus
- 🇱🇺 **Luxembourg Sub** - EU Regional HQ, currently loss-making
- 🇫🇷 **France Sub** - Sales support, zero self-generated revenue

## ✨ Key Features

- **Strict Ground Truth Adherence**: Only answers based on provided architecture documents
- **RAG-Powered**: Uses OpenAI embeddings and FAISS for semantic search
- **CFO Persona**: Professional, authoritative responses with citations
- **Session Management**: Clean conversation state, resets on page refresh
- **Source Citations**: References specific documents and pages
- **Error Handling**: Graceful handling of out-of-scope questions

## 📋 What the CFO Can Explain

### Financial Instruments & Flows
- R&D service fees, royalties, loans, and dividends
- Cash flow mechanisms between entities
- Contractual structures and legal relationships

### Tax & Compliance
- Transfer pricing strategies and documentation
- PE (Permanent Establishment) risk mitigation
- Tax audit defense mechanisms
- Loss utilization strategies

### Operational Mechanics
- Cost-plus models for service entities
- Profit repatriation strategies
- Entity roles and responsibilities
- Liquidity management

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Source PDF documents (see below)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd AI_Chatbot
   ```

2. **Create a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your OpenAI API key
   # Example:
   # OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
   ```

5. **Add source PDF files**

   Place your PDF documents in the `data/` directory:
   - `data/assignment.pdf` - Global Financial Architecture Assignment document
   - `data/diagram.pdf` - Architecture diagram with entity relationships

   **Important**: The chatbot requires these exact filenames. If your PDFs have different names, rename them accordingly.

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Open your browser**

   The application will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
AI_Chatbot/
├── app.py                 # Main Streamlit application
├── rag_engine.py          # RAG implementation and document processing
├── prompts.py             # System prompts and CFO persona
├── config.py              # Configuration and API key management
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
└── data/                  # Source documents directory
    ├── assignment.pdf     # (You need to add this)
    └── diagram.pdf        # (You need to add this)
```

## 💬 Usage Guide

### Starting a Conversation

1. Launch the application with `streamlit run app.py`
2. Wait for the initialization message (processes PDFs on first run)
3. Type your question in the chat input at the bottom
4. View the CFO's response with source citations

### Example Questions

**Financial Instruments:**
- "Why was Korea chosen as the R&D center?"
- "How do dividends flow from Korea to the US?"
- "Explain the rationale for R&D service fees vs. royalties"
- "How do loan agreements work between entities?"

**Tax Audit Defense:**
- "How does the structure avoid PE risk in France?"
- "How is transfer pricing compliance ensured globally?"
- "What documentation supports inter-company charges?"
- "How would you defend Korea→US cash flows in an audit?"

**Operational Mechanics:**
- "How does cash flow from Korea (surplus) to US (deficit)?"
- "What happens when Luxembourg becomes profitable?"
- "How are shareholder loans structured?"
- "Explain the cost-plus model for France"

### Viewing Sources

Click on "📚 View Sources" below any response to see:
- Which document the information came from
- The relevant page number
- A snippet of the source text

### Clearing Conversation

Click the "🔄 Clear Conversation" button in the sidebar to reset the chat and start fresh.

## ⚙️ Configuration Options

Edit the `.env` file to customize:

```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional (defaults shown)
OPENAI_MODEL=gpt-4-turbo          # or gpt-4, gpt-4o
OPENAI_TEMPERATURE=0.1            # Lower = more focused
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# RAG settings
CHUNK_SIZE=1000                   # Document chunk size
CHUNK_OVERLAP=200                 # Overlap between chunks
RETRIEVAL_K=5                     # Number of chunks to retrieve
```

## 🔧 Technical Details

### Tech Stack
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4/GPT-4 Turbo
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **PDF Processing**: PyPDF2 with fallback to pdfplumber
- **Framework**: LangChain for RAG orchestration

### How It Works

1. **Document Processing** (first run only):
   - Loads PDF files from `data/` directory
   - Extracts text and splits into semantic chunks
   - Generates embeddings using OpenAI
   - Stores vectors in FAISS for fast retrieval

2. **Question Answering**:
   - User asks a question
   - System retrieves top-K relevant document chunks
   - Injects context into prompt with CFO persona
   - GPT-4 generates grounded response
   - Sources are cited with page numbers

3. **Session Management**:
   - Conversation stored in Streamlit session state
   - Memory cleared on page refresh (no persistence)
   - Each session is independent

### Vector Store Caching

The first run processes PDFs and creates embeddings (~30-60 seconds). Subsequent runs load the pre-built vector store instantly. To rebuild:
```bash
# Delete the cache
rm -rf vector_store/

# Restart the app
streamlit run app.py
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure `.env` file exists in the project root
- Check that `OPENAI_API_KEY` is set (not the placeholder value)
- Restart the Streamlit app after editing `.env`

### "PDF not found" errors
- Verify PDF files are in `data/` directory
- Check filenames: must be `assignment.pdf` and `diagram.pdf`
- Ensure files aren't corrupted (try opening them manually)

### PDF extraction issues
- Some PDFs with complex layouts may not extract properly
- Try using `pdfplumber` instead of `PyPDF2` (code handles both)
- Consider using OCR for scanned PDFs (requires tesseract)

### "Rate limit exceeded" from OpenAI
- You've hit your OpenAI API usage limit
- Check your billing at platform.openai.com
- Consider reducing `RETRIEVAL_K` in `.env`

### Slow responses
- First run is slower (processing PDFs)
- Subsequent runs use cached vectors
- Consider using `gpt-3.5-turbo` for faster (but less accurate) responses

### Out of memory errors
- Reduce `CHUNK_SIZE` in `.env` (e.g., to 500)
- Reduce `RETRIEVAL_K` (e.g., to 3)
- Use `text-embedding-ada-002` instead of `text-embedding-3-small`

## 🔒 Security Notes

- **Never commit `.env` file** (contains API key)
- `.env` is in `.gitignore` by default
- API key is loaded at runtime, not hardcoded
- Consider using environment variables in production

## 📊 Performance & Costs

### Token Usage (Approximate)
- **Embedding generation**: ~2,000-5,000 tokens per PDF (one-time)
- **Per query**: 1,000-3,000 tokens depending on context
- **Estimated cost**: $0.01-0.05 per conversation

### Optimization Tips
1. Use `gpt-4-turbo` instead of `gpt-4` (cheaper, faster)
2. Reduce `RETRIEVAL_K` to minimize context size
3. Use `text-embedding-3-small` (cheaper than ada-002)
4. Increase `CHUNK_SIZE` to reduce total chunks

## 🧪 Testing Checklist

Before delivering to client:
- [ ] PDFs load successfully without errors
- [ ] Chat interface is responsive
- [ ] Responses cite specific entities and sources
- [ ] Out-of-scope questions are handled gracefully
- [ ] API key is configurable via `.env`
- [ ] Conversation resets on page refresh
- [ ] Source citations appear correctly
- [ ] Error messages are user-friendly
- [ ] README instructions are clear

## 📝 Development Notes

### Adding New Features
The codebase is modular:
- `config.py` - Add new settings
- `prompts.py` - Modify CFO behavior
- `rag_engine.py` - Change retrieval logic
- `app.py` - Update UI components

### Customizing the CFO Persona
Edit `SYSTEM_PROMPT` in `prompts.py` to change:
- Tone and formality
- Response structure
- Citation requirements
- Domain expertise

### Using Different LLMs
Modify `config.py`:
```python
OPENAI_MODEL = "gpt-3.5-turbo"  # Faster, cheaper
OPENAI_MODEL = "gpt-4o"          # Latest model
```

## 🤝 Support

For issues or questions:
1. Check this README's troubleshooting section
2. Verify all setup steps were completed
3. Check the Streamlit error messages in the UI
4. Review logs in the terminal where you ran `streamlit run app.py`

## 📄 License

This project is provided as-is for client use. All rights reserved.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [LangChain](https://www.langchain.com/) - LLM orchestration
- [OpenAI](https://openai.com/) - GPT-4 and embeddings
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search

---

**Version**: 1.0.0
**Last Updated**: 2025-11-24
**Python**: 3.9+
**Status**: Production-Ready ✅
