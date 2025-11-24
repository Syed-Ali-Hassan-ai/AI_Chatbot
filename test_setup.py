#!/usr/bin/env python3
"""
Setup Validation Script for CFO Chatbot
Run this to verify your installation is correct.
"""

import sys
from pathlib import Path
import os


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required")
        return False
    print("✅ Python version OK")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'streamlit',
        'openai',
        'langchain',
        'langchain_community',
        'langchain_openai',
        'PyPDF2',
        'faiss',
        'dotenv',
        'tiktoken'
    ]

    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'PyPDF2':
                __import__('PyPDF2')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)

    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("✅ All dependencies installed")
    return True


def check_env_file():
    """Check if .env file exists and has API key."""
    env_path = Path('.env')

    if not env_path.exists():
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then edit .env and add your OpenAI API key")
        return False

    print("✅ .env file exists")

    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY', '')

    if not api_key:
        print("❌ OPENAI_API_KEY not set in .env file")
        return False

    if api_key == 'your_api_key_here':
        print("❌ OPENAI_API_KEY is still set to placeholder value")
        print("   Edit .env and add your actual API key")
        return False

    if not api_key.startswith('sk-'):
        print("⚠️  OPENAI_API_KEY doesn't look like a valid OpenAI key")
        print("   OpenAI keys usually start with 'sk-'")
        return False

    print(f"✅ API key configured (starts with {api_key[:10]}...)")
    return True


def check_pdf_files():
    """Check if PDF files exist."""
    data_dir = Path('data')

    if not data_dir.exists():
        print("❌ data/ directory not found")
        return False

    print("✅ data/ directory exists")

    required_pdfs = ['assignment.pdf', 'diagram.pdf']
    missing = []

    for pdf_file in required_pdfs:
        pdf_path = data_dir / pdf_file
        if not pdf_path.exists():
            print(f"❌ {pdf_file} not found in data/ directory")
            missing.append(pdf_file)
        else:
            size = pdf_path.stat().st_size / 1024  # KB
            print(f"✅ {pdf_file} found ({size:.1f} KB)")

    if missing:
        print(f"\n❌ Missing PDF files: {', '.join(missing)}")
        print("   Place your PDF files in the data/ directory")
        return False

    return True


def check_imports():
    """Test if main modules can be imported."""
    try:
        import config
        print("✅ config.py imports successfully")
    except Exception as e:
        print(f"❌ Error importing config.py: {e}")
        return False

    try:
        import prompts
        print("✅ prompts.py imports successfully")
    except Exception as e:
        print(f"❌ Error importing prompts.py: {e}")
        return False

    try:
        import rag_engine
        print("✅ rag_engine.py imports successfully")
    except Exception as e:
        print(f"❌ Error importing rag_engine.py: {e}")
        return False

    try:
        import app
        print("✅ app.py imports successfully")
    except Exception as e:
        print(f"❌ Error importing app.py: {e}")
        return False

    return True


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("CFO Chatbot - Setup Validation")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("PDF Files", check_pdf_files),
        ("Module Imports", check_imports),
    ]

    results = []

    for name, check_func in checks:
        print(f"\n--- Checking {name} ---")
        result = check_func()
        results.append((name, result))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False

    print()

    if all_passed:
        print("🎉 All checks passed! You're ready to run the application.")
        print("\nTo start the chatbot, run:")
        print("  streamlit run app.py")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nSee README.md or QUICKSTART.md for detailed setup instructions.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
