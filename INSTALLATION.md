# Installation Guide - macOS with Python 3.11

This guide provides step-by-step instructions for setting up the CFO Chatbot on a fresh macOS system with Python 3.11.

## Prerequisites

### 1. Python 3.11
Verify Python version:
```bash
python3 --version  # Should show Python 3.11.x
```

If you don't have Python 3.11, install it via Homebrew:
```bash
brew install python@3.11
```

### 2. System Dependencies (macOS)
```bash
# Install Xcode Command Line Tools (if not already installed)
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Update Homebrew
brew update
```

## Installation Steps

### Step 1: Create Virtual Environment
**IMPORTANT**: Always use a virtual environment to avoid conflicts with system packages.

```bash
# Navigate to project directory
cd /path/to/AI_Chatbot

# Create virtual environment with Python 3.11
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify Python version in venv
python --version  # Should show Python 3.11.x
```

### Step 2: Upgrade pip and setuptools
```bash
# Upgrade pip to latest version
pip install --upgrade pip setuptools wheel
```

### Step 3: Install Dependencies
```bash
# Install from requirements.txt
pip install -r requirements.txt
```

**If you encounter errors**, try installing in stages:

```bash
# Stage 1: Core dependencies
pip install certifi charset-normalizer idna requests urllib3
pip install python-dotenv

# Stage 2: Scientific computing
pip install numpy==1.26.4
pip install pandas==2.2.3

# Stage 3: PDF processing
pip install pypdf==5.1.0
pip install pdfplumber==0.11.4
pip install Pillow==11.0.0

# Stage 4: OpenAI and utilities
pip install openai==1.57.4
pip install tiktoken==0.8.0

# Stage 5: Vector store
pip install faiss-cpu==1.9.0.post1

# Stage 6: Streamlit
pip install streamlit==1.41.1

# Stage 7: LangChain (in order)
pip install langchain-core==0.3.28
pip install langchain==0.3.14
pip install langchain-community==0.3.13
pip install langchain-openai==0.2.14
```

### Step 4: Verify Installation
```bash
# Test imports
python -c "import streamlit; print(f'Streamlit: {streamlit.__version__}')"
python -c "import langchain; print(f'LangChain: {langchain.__version__}')"
python -c "import openai; print(f'OpenAI: {openai.__version__}')"
python -c "import faiss; print('FAISS: OK')"
python -c "import pypdf; print('PyPDF: OK')"
```

All imports should succeed without errors.

### Step 5: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

Set in `.env`:
```
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4-turbo
OPENAI_TEMPERATURE=0.1
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=5
```

### Step 6: Add PDF Documents
```bash
# Create data directory if it doesn't exist
mkdir -p data

# Add your PDF files
cp /path/to/your/assignment.pdf data/
cp /path/to/your/diagram.pdf data/
```

### Step 7: Run the Application
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run Streamlit app
streamlit run app.py
```

The app should open in your browser at `http://localhost:8501`

## Common Issues and Solutions

### Issue 1: "No module named 'X'"
**Solution**: The module wasn't installed properly.
```bash
pip install <module-name> --force-reinstall
```

### Issue 2: FAISS Installation Fails
**Solution**: FAISS requires specific numpy version.
```bash
pip uninstall faiss-cpu numpy
pip install numpy==1.26.4
pip install faiss-cpu==1.9.0.post1
```

### Issue 3: LangChain Import Errors
**Solution**: Install LangChain packages in correct order.
```bash
pip uninstall langchain langchain-core langchain-community langchain-openai -y
pip install langchain-core==0.3.28
pip install langchain==0.3.14
pip install langchain-community==0.3.13
pip install langchain-openai==0.2.14
```

### Issue 4: SSL Certificate Errors
**Solution**: Update certificates.
```bash
pip install --upgrade certifi
# For macOS, also run:
/Applications/Python\ 3.11/Install\ Certificates.command
```

### Issue 5: Pydantic Validation Errors
**Solution**: Ensure compatible pydantic version.
```bash
pip install pydantic==2.10.3 pydantic-core==2.27.2
```

### Issue 6: Streamlit Command Not Found
**Solution**: Virtual environment not activated or streamlit not installed.
```bash
source venv/bin/activate
pip install streamlit==1.41.1
```

### Issue 7: OpenMP Library Error (on some Mac systems)
The code already includes a fix in `app.py`:
```python
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
```
This is set before any library imports to prevent OpenMP conflicts.

## Testing the Installation

Run the test script to verify everything is working:
```bash
python test_setup.py
```

This will check:
- Python version
- All required packages
- OpenAI API key
- PDF files
- Import compatibility

## Development Tips

### Freezing Dependencies
If you need to regenerate requirements.txt from your working environment:
```bash
pip freeze > requirements-frozen.txt
```

### Checking for Updates
```bash
pip list --outdated
```

### Clean Reinstall
If you need to start fresh:
```bash
# Deactivate and remove virtual environment
deactivate
rm -rf venv

# Remove cached files
rm -rf vector_store
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Start over from Step 1
```

## Performance Optimization

### For Faster Startup
After first run, the vector store is cached in `vector_store/` directory. This significantly speeds up subsequent launches.

### For Lower Memory Usage
Reduce these values in `.env`:
```
CHUNK_SIZE=800
RETRIEVAL_K=3
```

## Support

If you continue to experience issues:
1. Check Python version: `python --version`
2. Check virtual environment is active: `which python`
3. List installed packages: `pip list`
4. Check for conflicting packages: `pip check`

For specific error messages, search the error in the LangChain, Streamlit, or FAISS documentation.
