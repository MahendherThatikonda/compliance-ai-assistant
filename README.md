# Compliance AI Assistant — Foley's NZ

A RAG (Retrieval-Augmented Generation) application that helps 
plumbers, electricians, and gas-fitters instantly find compliance answers from 
official AS/NZS standards and New Zealand Building Code (NZBC) regulations.

## Overview

Tradies in NZ are required to work to AS/NZS standards, but navigating 27+ 
official documents totalling thousands of pages is time-consuming and error-prone. 
This assistant lets a tradie ask a plain-English question and get a precise, 
cited answer — with a direct link to the exact source page.

## Features

- **27 AS/NZS Standards** — 3,843 pages of official compliance documents ingested
- **Version-Aware Retrieval** — Correctly routes queries to current, superseded, 
  or specific-year document versions based on the question
- **Exact Source Citations** — Every answer links directly to the source PDF page
- **Dual Source Separation** — Clearly distinguishes AS/NZS primary requirements 
  from NZBC secondary sources
- **Pinecone Vector Search** — Fast semantic retrieval with metadata filtering
- **Strict Grounding** — LLM is prompted to answer only from retrieved documents, 
  never from general knowledge

## Tech Stack

| Component | Technology |
|---|---|
| Vector Database | Pinecone |
| Embeddings | OpenAI Embeddings |
| LLM | GPT-4.1-mini (OpenAI) |
| RAG Framework | LangChain |
| PDF Processing | PyMuPDF |
| Interface | Jupyter Notebooks |
| Testing | pytest (tests/) |

## Project Structure

compliance-ai-assistant/
├── notebooks/          # Exploratory and demo notebooks
├── src/
│   └── rag_pinecone/   # Core RAG pipeline
│       ├── ingest.py   # PDF ingestion and chunking
│       ├── retriever.py# Pinecone retrieval with metadata filtering
│       └── pipeline.py # End-to-end RAG chain
├── tests/              # Unit and integration tests
├── requirements.txt
└── .gitignore

## How It Works

1. **Ingestion** — AS/NZS PDFs are extracted, chunked, and stored in Pinecone 
   with page-level metadata (document version, standard number, page number)
2. **Query** — User asks a plain-English compliance question
3. **Retrieval** — Version-aware metadata filtering fetches the most relevant 
   chunks from the correct document version
4. **Generation** — LLM generates a structured answer strictly from retrieved 
   chunks, separating AS/NZS requirements
