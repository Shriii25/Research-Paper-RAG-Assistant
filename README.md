# Research Paper RAG Assistant

A Retrieval-Augmented Generation (RAG) application that enables users to upload research papers, build a semantic knowledge base, generate paper summaries, create literature reviews, and ask natural language questions across an entire research collection.

The system uses Sentence Transformers for embedding generation, FAISS for vector similarity search, and Google's Gemini API for summarization, literature review generation, and context-aware question answering.

## Features

- Upload and analyze multiple research papers (PDF)
- Build a semantic vector database using FAISS
- Generate structured summaries for individual papers
- Create collection-level summaries across all uploaded papers
- Automatically generate literature reviews from multiple papers
- Ask natural language questions and receive context-aware answers
- Display source citations for retrieved information
- Interactive web interface built with Streamlit

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- LangChain
- FAISS
- Sentence Transformers
- Hugging Face Embeddings
- PyPDF

## Architecture

PDF Upload → Text Extraction → Chunking → Embedding Generation → FAISS Vector Store → Retrieval → Gemini LLM → Response Generation

## Use Cases

- Literature survey and review generation
- Academic research assistance
- Research paper comparison and analysis
- Knowledge extraction from large collections of papers
- Rapid understanding of unfamiliar research domains
