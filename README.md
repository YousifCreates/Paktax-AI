# 🏛️ PakTax AI — FBR Intelligent Tax Filing Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-1.2.x-green?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.1.0-lightgrey?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.6.3-orange?style=flat-square)
![GPU](https://img.shields.io/badge/GPU-CUDA%2012.1-76b900?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> An intelligent, multilingual AI assistant for Pakistani citizens to understand and navigate FBR (Federal Board of Revenue) income tax filing — powered by Retrieval-Augmented Generation (RAG) over official FBR documents.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Methodology](#-methodology)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [RAG Pipeline Explained](#-rag-pipeline-explained)
- [Document Corpus](#-document-corpus)
- [Hardware Requirements](#-hardware-requirements)
- [Developer Setup](#-developer-setup)

---

## 📖 Project Overview

**PakTax AI** is a Generative AI-powered chatbot that helps Pakistani citizens understand and file their income tax returns through an intelligent conversational interface. The assistant is built on a **Prompt Engineering + RAG (Retrieval-Augmented Generation)** architecture — meaning it does not rely on general AI knowledge but instead retrieves answers directly from official FBR legal documents.

The system supports **three languages simultaneously**:
- English
- Urdu (اردو)
- Roman Urdu (Romanized)

Users can ask questions like:
- *"What are the income tax slabs for salaried persons in 2024-25?"*
- *"Main salaried person hoon, mujhe kitna tax dena hoga?"*
- *"How do I file my return on IRIS?"*

And receive accurate, document-backed responses — not hallucinated guesses.

---

## 🎯 Problem Statement

Filing income tax in Pakistan is notoriously complex. Citizens face:

- Confusing legal language in FBR ordinances and acts
- Fragmented information across multiple documents and web pages
- Language barriers — most official documents are in English while the majority of taxpayers are Urdu speakers
- High cost of consulting tax professionals for basic queries
- Frequent policy changes with each Finance Act

**PakTax AI** addresses all of these by acting as an always-available, multilingual tax expert grounded in official FBR documents.

---

## 🔬 Methodology

### Approach: Option B — Prompt Engineering + RAG

This project deliberately chose **RAG over fine-tuning** for the following reasons:

| Factor | Fine-Tuning | RAG (Our Choice) |
|--------|------------|------------------|
| Training time | 6–10 hours on GPU | Not required |
| Data needed | 5,000+ labeled pairs | Raw PDFs/TXT files |
| Update process | Re-train entire model | Add new documents |
| Accuracy source | Model weights | Source documents |
| Hallucination risk | High | Low (grounded) |
| Cost | High (GPU compute) | Low (API calls only) |
| Time to deploy | Days | Hours |

The RAG approach is ideal here because:
1. FBR policies change every year with new Finance Acts
2. Accuracy must be grounded in legal documents, not AI memory
3. The deadline did not permit multi-day training runs
4. A well-prompted LLM with good retrieval outperforms a poorly fine-tuned model

### LLM Choice: GPT-4o-mini via OpenAI API

- Fast response times
- Strong multilingual understanding (English, Urdu, Roman Urdu)
- Cost-effective for demo and production use
- No GPU VRAM required (runs on OpenAI servers)

### Embedding Model: multilingual-e5-large

- Runs locally on NVIDIA RTX 3050 GPU
- Specifically trained for multilingual semantic search
- Handles cross-lingual retrieval (Urdu query → English document chunk)
- Uses `normalize_embeddings=True` for accurate cosine similarity

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│              Flask Web App (HTML + CSS + JS)                 │
│         English / Urdu / Roman Urdu Input Support            │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP POST /chat
┌──────────────────────────▼──────────────────────────────────┐
│                       FLASK BACKEND                          │
│                         app.py                               │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    LANGCHAIN QA CHAIN                         │
│                     qa_chain_openai.py                       │
│                                                              │
│   ┌─────────────────┐      ┌──────────────────────────┐     │
│   │   RETRIEVER     │      │      GPT-4o-mini          │     │
│   │  retriever.py   │─────▶│   (OpenAI API)            │     │
│   │                 │      │   System Prompt + Context  │     │
│   └────────┬────────┘      └──────────────────────────┘     │
│            │                                                  │
│   ┌────────▼────────┐                                        │
│   │    ChromaDB     │  ← Vector Store (local disk)           │
│   │  (chroma_db/)   │                                        │
│   └────────┬────────┘                                        │
│            │                                                  │
│   ┌────────▼────────┐                                        │
│   │ multilingual-e5 │  ← Embeddings on RTX 3050 GPU         │
│   │  (CUDA 12.1)    │                                        │
│   └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   FBR DOCUMENT CORPUS                         │
│                     data/fbr_docs/                           │
│   Income Tax Ordinance 2001 · Finance Acts · Tax Rules       │
│   Tax Slabs · Amendment Ordinances · Newsletters             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| LLM | GPT-4o-mini (OpenAI) | Answer generation |
| RAG Framework | LangChain 1.2.x | Pipeline orchestration |
| Vector Store | ChromaDB 0.6.3 | Document chunk storage |
| Embeddings | multilingual-e5-large | Semantic search |
| GPU Acceleration | CUDA 12.1 + PyTorch | Fast embedding on GPU |
| Backend | Flask 3.1.0 | REST API server |
| Frontend | HTML5 + CSS3 + Vanilla JS | Chat UI |
| Environment | Python 3.11 + Conda | Runtime |
| Document Loading | PyPDF + TextLoader | PDF and TXT ingestion |

---

## ✨ Key Features

- **Multilingual Support** — English, Urdu script, Roman Urdu, and code-switching
- **RAG-Grounded Answers** — All responses come from official FBR documents
- **GPU-Accelerated Embeddings** — Fast document search via local RTX 3050
- **Conversation Memory** — Remembers context across multiple questions
- **Modern Chat UI** — Dark theme with grid background, fully mobile responsive
- **Quick Start Chips** — Pre-built questions for first-time users
- **Table Rendering** — Tax slab tables rendered beautifully in chat
- **Strict Hallucination Guard** — System prompt prevents made-up tax figures
- **Zero Training Required** — No fine-tuning, deploy immediately after ingestion

---

## 📁 Project Structure

```
Paktax-AI/
├── app.py                      # Flask entry point & API routes
├── .env                        # API keys (not in repo)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── rag/
│   ├── __init__.py
│   ├── ingest.py               # Load PDFs → Chunk → Embed → ChromaDB
│   └── retriever.py            # Query ChromaDB → Return relevant chunks
│
├── chain/
│   ├── __init__.py
│   └── qa_chain_openai.py      # LangChain pipeline (Retriever + LLM)
│
├── data/
│   └── fbr_docs/               # FBR PDFs and TXT files (not in repo)
│       ├── IncomeTaxOrdinance2001.pdf
│       ├── FinanceAct2025.pdf
│       ├── TaxLawsAmendment2025.pdf
│       ├── IncomeTaxRules2002.pdf
│       ├── finance-act.txt
│       └── tax_slabs_2024_25.txt
│
├── templates/
│   └── index.html              # Chat UI template
│
└── static/
    ├── css/
    │   └── style.css           # Dark theme + grid background
    └── js/
        └── model.js            # Chat logic + API calls
```

---

## 🔄 RAG Pipeline Explained

### Phase 1 — One-Time Ingestion (`ingest.py`)

```
FBR PDFs + TXT Files
        ↓
Load with PyPDFLoader / TextLoader
        ↓
Split into 500-token chunks (100 token overlap)
        ↓
Embed with multilingual-e5-large on RTX 3050 GPU
        ↓
Store vectors in ChromaDB (local disk)
```

Run once:
```bash
PYTHONPATH=. python3 rag/ingest.py
```

### Phase 2 — Every User Query

```
User Question (any language)
        ↓
Embed question with same model (GPU)
        ↓
ChromaDB similarity search → Top 10 chunks
        ↓
LangChain builds prompt:
  [System Rules] + [FBR Chunks] + [Chat History] + [User Question]
        ↓
GPT-4o-mini generates answer
        ↓
Flask returns JSON → JS renders in chat UI
```

---

## 📚 Document Corpus

All documents sourced from [fbr.gov.pk](https://fbr.gov.pk):

| Document | Source |
|----------|--------|
| Income Tax Ordinance 2001 (Amended 2026) | FBR Acts/Ordinances |
| Finance Act 2025 | FBR Acts |
| Tax Laws (Amendment) Ordinance 2025 | FBR Ordinances |
| Income Tax Rules 2002 (Amended 2023) | FBR Rules |
| FBR Revenews Newsletter | FBR Publications |
| Tax Slabs 2024-25 (manual TXT) | First Schedule, Finance Act |

> **Note:** FBR PDF tables are image-based and not extractable by PyPDF. Critical tax slab data has been manually transcribed into `tax_slabs_2024_25.txt` for accurate retrieval.

---

## 💻 Hardware Requirements

| Component | Minimum | Used in This Project |
|-----------|---------|---------------------|
| GPU | Optional (CPU fallback) | NVIDIA RTX 3050 6GB |
| CUDA | 11.8+ | 12.1 |
| RAM | 8GB | 16GB+ recommended |
| Storage | 2GB | For ChromaDB + models |
| OS | Linux/Windows/Mac | Ubuntu 24 |

---

## 👨‍💻 Developer Setup

### Prerequisites

- Python 3.10 or above
- Anaconda or pip virtual environment
- NVIDIA GPU with CUDA (optional but recommended)
- OpenAI API key
- Git

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YousifCreates/Paktax-AI
cd Paktax-AI
```

---

### Step 2 — Create and Activate Environment

**Using Conda (Recommended):**
```bash
conda create -n paktax-ai python=3.11
conda activate paktax-ai
```

**Using venv:**
```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

---

### Step 3 — Install PyTorch with CUDA

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

> Skip this step if you have no GPU. The system will automatically fall back to CPU.

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5 — Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

Get your OpenAI API key from [platform.openai.com](https://platform.openai.com)

---

### Step 6 — Add FBR Documents

Download official FBR documents and place them in `data/fbr_docs/`:

| Document | Download From |
|----------|--------------|
| Income Tax Ordinance 2001 | fbr.gov.pk/acts-ordinance/rules |
| Finance Act 2025 | fbr.gov.pk/finance-act |
| Tax Laws Amendment 2025 | fbr.gov.pk/acts-ordinance/rules |
| Income Tax Rules 2002 | fbr.gov.pk/acts-ordinance/rules |

Also create `data/fbr_docs/tax_slabs_2024_25.txt` manually with current FBR tax slab data.

---

### Step 7 — Run Document Ingestion

```bash
PYTHONPATH=. python3 rag/ingest.py
```

Expected output:
```
Using device: cuda
=== PakTax AI — FBR Document Ingestion ===
Loading PDF: IncomeTaxOrdinance2001.pdf
...
Total chunks created: 8435
Embedding chunks and saving to ChromaDB...
Ingestion complete. ChromaDB is ready.
```

> This step takes ~50 minutes on first run (downloads embedding model ~2.2GB). Subsequent runs are faster.

---

### Step 8 — Run the Application

```bash
PYTHONPATH=. python3 app.py
```

Open your browser at:
```
http://localhost:5000
```

---

### Step 9 — Test the Pipeline (Optional)

```bash
# Test retriever only
PYTHONPATH=. python3 rag/retriever.py

# Test full QA chain
PYTHONPATH=. python3 -m chain.qa_chain_openai
```

---

## 🔑 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for GPT-4o-mini |
| `GOOGLE_API_KEY` | Optional | Google AI Studio key (alternative LLM) |

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.

---

<div align="center">
  <strong>YousifCreates | Muhammad Yousif Memon | AI Engineer | Freelancer</strong><br/>
  <sub>Powered by LangChain · ChromaDB · OpenAI · FBR Official Documents</sub>
</div>
