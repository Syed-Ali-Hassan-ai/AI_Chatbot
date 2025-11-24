# Source Documents Directory

This directory should contain the PDF source documents that the CFO chatbot uses as its knowledge base.

## Required Files

Place the following PDF files in this directory:

1. **assignment.pdf** - Global Financial Architecture Assignment document
   - Contains entity profiles, objectives, and deliverables
   - Details the roles of US Parent, Korea Sub, Luxembourg Sub, and France Sub

2. **diagram.pdf** - Master Architecture Diagram
   - Visual representation of the financial structure
   - Shows financial instruments (yellow boxes)
   - Shows tax audit defense mechanisms (green boxes)
   - Shows entity details (purple boxes)
   - Shows Luxembourg profit generation (cyan box)
   - Shows directional flows (green arrows)

## File Naming

**IMPORTANT**: The files must be named exactly as shown above:
- `assignment.pdf` (lowercase, no spaces)
- `diagram.pdf` (lowercase, no spaces)

If your source files have different names, please rename them to match.

## Obtaining the Files

These PDF files should be provided by the client or project manager. They contain the specific global financial architecture that the CFO bot will reference.

## Privacy Note

PDF files in this directory are included in `.gitignore` by default (depending on your configuration). If these contain sensitive information, ensure they are not committed to version control.

## Verification

To verify your PDFs are correctly placed:

1. Check that files exist:
   ```bash
   ls -la
   ```

   You should see:
   - `assignment.pdf`
   - `diagram.pdf`

2. Start the application:
   ```bash
   streamlit run ../app.py
   ```

3. The app will indicate if PDFs are found or missing

## Troubleshooting

**"PDF not found" error?**
- Ensure files are in this directory (`data/`)
- Check exact filenames (case-sensitive on Linux/Mac)
- Verify files aren't corrupted (can you open them?)

**PDF won't extract text?**
- Some PDFs may be scanned images
- Try opening the PDF - is the text selectable?
- Consider OCR if needed (see main README.md)
