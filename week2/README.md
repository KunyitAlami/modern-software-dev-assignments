# Week 2 — Action Item Extractor

This project is a minimal FastAPI + SQLite web application that converts free-form notes into structured action items.

It supports both:

- **Heuristic-based extraction**
- **LLM-powered extraction using Ollama**

Users can paste meeting notes into the frontend, extract tasks, save notes, and view stored action items.

---

## Features

- Extract action items from raw notes
- Save notes into a SQLite database
- Store extracted action items linked to notes
- Mark action items as done
- LLM-powered extraction using Ollama (`llama3.1:8b`)
- Simple HTML frontend with buttons:
    - Extract
    - Extract LLM
    - List Notes

---

## Tech Stack

- **FastAPI** (backend API)
- **SQLite** (local database)
- **Ollama** (LLM inference)
- **Pytest** (unit testing)
- Minimal HTML + JavaScript frontend

---

## Setup Instructions

### 1. Activate Environment

```powershell
conda activate cs146s
```

### 2. Install Dependencies

`poetry install`

### 3. Ensure Ollama is Installed and Running

`ollama list`
