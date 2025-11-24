"""
RAG Engine for CFO Chatbot.
Handles PDF processing, embedding generation, vector storage, and retrieval.
"""

import os
from typing import List, Dict, Tuple
from pathlib import Path
import pickle

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import Document

from config import config
from prompts import SYSTEM_PROMPT, CONTEXT_PROMPT_TEMPLATE


class RAGEngine:
    """
    RAG Engine for processing documents and answering questions.
    """

    def __init__(self):
        """Initialize the RAG engine."""
        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.qa_chain = None
        self.memory = None

    def load_and_process_pdfs(self) -> List[Document]:
        """
        Load and process PDF documents.
        Returns list of Document objects.
        """
        documents = []

        for pdf_path in config.get_pdf_paths():
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF not found: {pdf_path}")

            # Load PDF
            loader = PyPDFLoader(str(pdf_path))
            pdf_documents = loader.load()

            # Add metadata to identify source
            source_name = pdf_path.stem
            for doc in pdf_documents:
                doc.metadata['source'] = source_name
                doc.metadata['file'] = pdf_path.name

            documents.extend(pdf_documents)

        return documents

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks for processing.
        Uses semantic chunking to preserve context.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            keep_separator=True
        )

        chunks = text_splitter.split_documents(documents)

        # Add chunk metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = i

        return chunks

    def create_vector_store(self, chunks: List[Document]) -> FAISS:
        """
        Create FAISS vector store from document chunks.
        """
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model=config.OPENAI_EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )

        # Create vector store
        vector_store = FAISS.from_documents(chunks, self.embeddings)

        return vector_store

    def save_vector_store(self):
        """Save vector store to disk for faster loading."""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")

        config.VECTOR_STORE_PATH.mkdir(exist_ok=True)
        self.vector_store.save_local(str(config.VECTOR_STORE_PATH))

    def load_vector_store(self) -> bool:
        """
        Load vector store from disk if it exists.
        Returns True if successful, False otherwise.
        """
        if not config.VECTOR_STORE_PATH.exists():
            return False

        try:
            # Initialize embeddings first
            self.embeddings = OpenAIEmbeddings(
                model=config.OPENAI_EMBEDDING_MODEL,
                openai_api_key=config.OPENAI_API_KEY
            )

            # Load vector store
            self.vector_store = FAISS.load_local(
                str(config.VECTOR_STORE_PATH),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False

    def initialize(self, force_rebuild: bool = False) -> str:
        """
        Initialize the RAG engine.
        Args:
            force_rebuild: If True, rebuild vector store even if it exists
        Returns:
            Status message
        """
        # Try to load existing vector store
        if not force_rebuild and self.load_vector_store():
            status = "✓ Loaded existing vector store"
        else:
            # Process PDFs and create new vector store
            status = "Processing PDFs..."
            documents = self.load_and_process_pdfs()
            status += f"\n✓ Loaded {len(documents)} pages from PDFs"

            chunks = self.chunk_documents(documents)
            status += f"\n✓ Created {len(chunks)} document chunks"

            self.vector_store = self.create_vector_store(chunks)
            status += "\n✓ Created vector embeddings"

            self.save_vector_store()
            status += "\n✓ Saved vector store for future use"

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=config.OPENAI_MODEL,
            temperature=config.OPENAI_TEMPERATURE,
            openai_api_key=config.OPENAI_API_KEY
        )

        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        # Create QA chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": config.RETRIEVAL_K}
            ),
            memory=self.memory,
            return_source_documents=True,
            verbose=False,
            combine_docs_chain_kwargs={
                "prompt": PromptTemplate(
                    template=SYSTEM_PROMPT + "\n\n" + CONTEXT_PROMPT_TEMPLATE,
                    input_variables=["context", "question"]
                )
            }
        )

        status += "\n✓ CFO Bot ready!"
        return status

    def ask(self, question: str) -> Dict:
        """
        Ask a question and get an answer with sources.
        Returns dict with 'answer' and 'sources'.
        """
        if self.qa_chain is None:
            raise ValueError("RAG engine not initialized. Call initialize() first.")

        # Get response from chain
        response = self.qa_chain({"question": question})

        # Extract answer and sources
        answer = response['answer']
        source_documents = response.get('source_documents', [])

        # Format sources
        sources = []
        seen_sources = set()
        for doc in source_documents:
            source_name = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'N/A')
            source_key = f"{source_name}_p{page}"

            if source_key not in seen_sources:
                sources.append({
                    'source': source_name,
                    'page': page,
                    'content': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
                seen_sources.add(source_key)

        return {
            'answer': answer,
            'sources': sources
        }

    def reset_conversation(self):
        """Reset conversation memory."""
        if self.memory:
            self.memory.clear()

    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        if self.memory is None:
            return []

        history = []
        for message in self.memory.chat_memory.messages:
            history.append({
                'type': message.type,
                'content': message.content
            })
        return history


def create_rag_engine() -> RAGEngine:
    """
    Factory function to create and initialize RAG engine.
    """
    engine = RAGEngine()
    return engine
