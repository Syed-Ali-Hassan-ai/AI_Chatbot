# Quick Start Guide - CFO Chatbot

Get up and running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Your API Key

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace `your_api_key_here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```

   **Get an API key**: https://platform.openai.com/api-keys

## Step 3: Add Your PDF Documents

Place these files in the `data/` directory:
- `data/assignment.pdf` - Your Global Financial Architecture document
- `data/diagram.pdf` - Your architecture diagram

**Important**: Use these exact filenames.

## Step 4: Run the Application

```bash
streamlit run app.py
```

The browser will open automatically at `http://localhost:8501`

## Step 5: Start Asking Questions!

Try these example questions:
- "How does cash flow from Korea to the US?"
- "How do we avoid PE risk in France?"
- "Why was Korea chosen as the R&D center?"
- "Explain the transfer pricing strategy"

## Troubleshooting

**Error: "OPENAI_API_KEY not found"**
- Make sure you created the `.env` file (copy from `.env.example`)
- Check that you replaced the placeholder with your actual API key
- Restart the Streamlit app

**Error: "PDF not found"**
- Verify files are in `data/` directory
- Check filenames: `assignment.pdf` and `diagram.pdf` (exact names)
- Make sure files aren't corrupted

**Need help?**
- See the full README.md for detailed instructions
- Check that you're using Python 3.9 or higher: `python --version`

## That's It!

You should now have a fully functional CFO chatbot. The first run will take 30-60 seconds to process the PDFs and create embeddings. Subsequent runs will be instant.

Enjoy! 🚀
