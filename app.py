"""
CFO Chatbot - Streamlit Application
A RAG-based chatbot that acts as CFO for a global financial architecture.
"""

# Fix for OpenMP Error #15 - Must be set before any library imports
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import streamlit as st
from typing import List, Dict
import sys

from config import config
from rag_engine import create_rag_engine
from prompts import GREETING_MESSAGE, FALLBACK_RESPONSE, check_if_out_of_scope


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None

    if 'initialized' not in st.session_state:
        st.session_state.initialized = False


def display_config_errors(errors: List[str]):
    """Display configuration errors in the UI."""
    st.error("### Configuration Issues Detected")

    for error in errors:
        st.error(error)

    st.info("""
    **Setup Instructions:**

    1. **Set your OpenAI API Key:**
       - Create a `.env` file in the project root
       - Add: `OPENAI_API_KEY=your_actual_api_key_here`

    2. **Add source PDF files to the `data/` directory:**
       - `data/assignment.pdf` - Global Financial Architecture Assignment
       - `data/diagram.pdf` - Architecture Diagram

    3. **Restart the application**

    See README.md for detailed setup instructions.
    """)


def initialize_rag_engine():
    """Initialize the RAG engine with progress indication."""
    try:
        with st.spinner("🔧 Initializing CFO Bot..."):
            rag_engine = create_rag_engine()
            status = rag_engine.initialize()

            # Display initialization status
            st.success(status)
            st.session_state.rag_engine = rag_engine
            st.session_state.initialized = True

            # Add greeting message
            st.session_state.messages.append({
                "role": "assistant",
                "content": GREETING_MESSAGE
            })

            return True

    except FileNotFoundError as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Please ensure PDF files are in the data/ directory. See README.md for details.")
        return False

    except Exception as e:
        st.error(f"❌ Initialization Error: {str(e)}")
        st.info("Please check your configuration and try again.")
        return False


def display_message(role: str, content: str, sources: List[Dict] = None):
    """Display a chat message with optional sources."""
    with st.chat_message(role):
        st.markdown(content)

        # Display sources if available
        if sources and len(sources) > 0:
            with st.expander("📚 View Sources", expanded=False):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"""
                    **Source {i}:** {source['source']} (Page {source['page']})
                    > {source['content']}
                    """)


def handle_user_input(user_question: str):
    """Process user input and generate response."""
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # Check if question is obviously out of scope
    if check_if_out_of_scope(user_question):
        response = {
            'answer': FALLBACK_RESPONSE,
            'sources': []
        }
    else:
        # Get response from RAG engine
        with st.spinner("🤔 Analyzing..."):
            try:
                response = st.session_state.rag_engine.ask(user_question)
            except Exception as e:
                response = {
                    'answer': f"I apologize, but I encountered an error processing your question: {str(e)}",
                    'sources': []
                }

    # Add assistant response to chat
    st.session_state.messages.append({
        "role": "assistant",
        "content": response['answer'],
        "sources": response.get('sources', [])
    })


def display_sidebar():
    """Display sidebar with instructions and controls."""
    with st.sidebar:
        st.header("ℹ️ About CFO Bot")

        st.markdown("""
        This CFO can answer questions about:

        **Financial Instruments & Flows:**
        - R&D service fees, royalties, loans, dividends
        - Cash movement between entities
        - Contractual structures

        **Tax & Compliance:**
        - Transfer pricing strategies
        - PE (Permanent Establishment) risk mitigation
        - Tax audit defense mechanisms
        - Documentation requirements

        **Operational Mechanics:**
        - Cost-plus models
        - Loss utilization strategies
        - Entity roles and relationships
        - Profit repatriation

        **Entity Structure:**
        - 🇺🇸 US Parent (IP Holder)
        - 🇰🇷 Korea Sub (R&D Center)
        - 🇱🇺 Luxembourg Sub (EU HQ)
        - 🇫🇷 France Sub (Sales Support)
        """)

        st.divider()

        st.subheader("💡 Example Questions")
        examples = [
            "Why was Korea chosen as the R&D center?",
            "How does cash flow from Korea to US?",
            "How do we mitigate PE risk in France?",
            "Explain the transfer pricing documentation",
            "What happens when Luxembourg becomes profitable?",
            "How are shareholder loans structured?"
        ]

        for example in examples:
            if st.button(example, key=f"example_{hash(example)}", use_container_width=True):
                # Add question to session state to be processed
                st.session_state.next_question = example

        st.divider()

        # Clear conversation button
        if st.button("🔄 Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.rag_engine:
                st.session_state.rag_engine.reset_conversation()
            st.session_state.messages.append({
                "role": "assistant",
                "content": GREETING_MESSAGE
            })
            st.rerun()

        st.divider()

        # Configuration info
        with st.expander("⚙️ Configuration"):
            st.caption(f"**Model:** {config.OPENAI_MODEL}")
            st.caption(f"**Temperature:** {config.OPENAI_TEMPERATURE}")
            st.caption(f"**Retrieval K:** {config.RETRIEVAL_K}")


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    initialize_session_state()

    # Display header
    st.title(config.APP_TITLE)
    st.caption(config.APP_SUBTITLE)

    # Validate configuration
    is_valid, errors = config.validate()

    if not is_valid:
        display_config_errors(errors)
        return

    # Initialize RAG engine if not already done
    if not st.session_state.initialized:
        success = initialize_rag_engine()
        if not success:
            return

    # Display sidebar
    display_sidebar()

    # Display chat messages
    for message in st.session_state.messages:
        display_message(
            role=message["role"],
            content=message["content"],
            sources=message.get("sources")
        )

    # Handle example question from sidebar
    if 'next_question' in st.session_state:
        question = st.session_state.next_question
        del st.session_state.next_question
        handle_user_input(question)
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Ask me about the financial architecture..."):
        handle_user_input(prompt)
        st.rerun()


if __name__ == "__main__":
    main()
