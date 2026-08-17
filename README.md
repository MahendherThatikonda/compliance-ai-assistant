# AI-Powered Plumbing Compliance Assistant

An AI-powered Retrieval-Augmented Generation (RAG) application designed to help plumbers quickly find compliance information from AS/NZS plumbing standards.

🔗 **Live Application:** https://compliance-ai-assistant-1.onrender.com

## Overview

The application allows users to ask plumbing compliance questions in natural language.

It retrieves relevant information from indexed AS/NZS standards and uses an LLM to generate an answer based on the retrieved content.

The application also displays the source documents used to generate an answer.

If sufficient information cannot be found in the available standards, the assistant responds with:

> Not enough information.

rather than generating an unsupported answer.

## Features

- Natural-language plumbing compliance questions
- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- Source document attribution
- Guardrail for insufficient information
- Example compliance questions
- User feedback functionality
- Responsive Angular chat interface
- Production deployment

## Architecture

User
↓
Angular Frontend
↓
FastAPI REST API
↓
RAG Pipeline
↓
Pinecone Vector Database
↓
Relevant Standard Documents
↓
OpenAI
↓
Answer + Sources

## Technology Stack

### Frontend
- Angular
- TypeScript
- HTML
- CSS

### Backend
- Python
- FastAPI
- Uvicorn

### AI / RAG
- OpenAI
- Embeddings
- Pinecone
- Retrieval-Augmented Generation (RAG)

### Deployment
- Render
- GitHub

## How It Works

1. The user submits a plumbing compliance question.
2. The Angular application sends the question to the FastAPI backend.
3. The backend searches the Pinecone vector index for relevant document chunks.
4. Relevant context is supplied to the language model.
5. The generated answer is returned to the frontend.
6. Source document names are displayed with the answer when supporting information is available.

## Example Question

**Question**

What are the requirements for gully traps?

The application retrieves the relevant requirements from the indexed plumbing standards and generates an answer with the corresponding source document.

## Running Locally

### Backend

Install the Python dependencies:

    pip install -r requirements.txt

Start the FastAPI server:

    uvicorn app:app --reload

### Frontend

Navigate to the frontend:

    cd frontend

Install dependencies:

    npm install

Start Angular:

    ng serve

Then open:

    http://localhost:4200

## Environment Variables

The backend requires environment variables such as:

    OPENAI_API_KEY
    PINECONE_API_KEY
    PINECONE_INDEX_NAME
    EMBEDDING_MODEL
    EMBEDDING_DIM

API keys and secrets are not stored in the repository.

## Author

**Mahendher Thatikonda**

Master of Applied Data Science  
University of Canterbury

Software Engineer specialising in C#, .NET, Python, Angular and AI-powered applications.
