"""
Configuration management for CFO Chatbot.
Handles API keys, file paths, and application settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the CFO Chatbot application."""

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    # File Paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    ASSIGNMENT_PDF = DATA_DIR / "assignment.pdf"
    DIAGRAM_PDF = DATA_DIR / "diagram.pdf"
    VECTOR_STORE_PATH = BASE_DIR / "vector_store"

    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "5"))  # Number of documents to retrieve

    # Application Settings
    APP_TITLE = "CFO Bot - Global Financial Architecture"
    APP_SUBTITLE = "Expert guidance on financial structure, tax optimization, and compliance"

    @classmethod
    def validate(cls):
        """
        Validate configuration settings.
        Returns tuple: (is_valid, error_messages)
        """
        errors = []

        # Check API key
        if not cls.OPENAI_API_KEY:
            errors.append("❌ OPENAI_API_KEY not found. Please set it in .env file.")
        elif cls.OPENAI_API_KEY == "your_api_key_here":
            errors.append("❌ OPENAI_API_KEY is set to placeholder value. Please use your actual API key.")

        # Check if data directory exists
        if not cls.DATA_DIR.exists():
            errors.append(f"❌ Data directory not found: {cls.DATA_DIR}")

        # Check if PDF files exist
        if not cls.ASSIGNMENT_PDF.exists():
            errors.append(f"❌ Assignment PDF not found: {cls.ASSIGNMENT_PDF}")
            errors.append("   Please add 'assignment.pdf' to the data/ directory")

        if not cls.DIAGRAM_PDF.exists():
            errors.append(f"❌ Diagram PDF not found: {cls.DIAGRAM_PDF}")
            errors.append("   Please add 'diagram.pdf' to the data/ directory")

        return len(errors) == 0, errors

    @classmethod
    def get_pdf_paths(cls):
        """Return list of PDF file paths to process."""
        return [cls.ASSIGNMENT_PDF, cls.DIAGRAM_PDF]


# Create a singleton instance
config = Config()
