# Mini AI Ticket Classifier

A lightweight prototype built with Python, Streamlit, and Pydantic to orchestrate open-source LLMs (via Ollama) to automatically transform messy, human-written support tickets into strict, validated JSON formats.

## Features
- **Local AI Engine**: Runs fully locally with zero external API fees using Ollama.
- **Data Guardrails**: Integrates strict JSON formatting constraints verified via structural Pydantic validation rules.
- **Intuitive GUI Interface**: Fast batch processing UI created using Streamlit.
- **Single Command Orchestration**: Runs everywhere via a unified multi-container Docker assembly.


## Technical Design Decisions & Production Roadmaps

1. Ollama Integration: Selected because it bridges code with open weights using OpenAI-compatible API standards, permitting instant local testing.

2. Pydantic Guard: Large Language Models are probabilistic and frequently hallucinate variations or markdown elements. Pydantic ensures the web-app catches and flags schema anomalies before processing downstream.

3. Streamlit UI: Allows prototyping UI flows in native Python syntax with rapid turnaround time.

## Prerequisites
Ensure your host machine has the following tools set up:
- **Docker** and **Docker Compose**

---

## How to run

### Step 1: Clone the repo and navigate to the project folder

```bash
cd mini-ticket-classifier
```

### Step 2: Launch the Docker Container Stack
EIn the project root folder directory, execute the following command to boot the background services:

```bash
docker compose up -d
```

This initiates two decoupled infrastructure nodes: ticket-classifier-ui (running the Streamlit app on port 8501) and ollama-engine (running the local LLM runtime on port 11434).

## Step 3: Download the Open-Source Model Parameters
Because LLM weights are several gigabytes in size, the underlying Ollama instance boots up empty by default. Instruct it to download and pull its core weights (e.g., llama3, mistral, or phi3) by running this inside your terminal:

```bash
docker exec -it ollama-engine ollama run llama3
```

Once the download hits 100% and displays a success prompt, you can safely exit the terminal instance by typing ```/exit``` in that terminal interface.

### Step 4: Access the GUI Application Dashboard
Open your preferred web browser and navigate to:
http://localhost:8501

From the interactive dashboard UI, you can:
1. Select individual items from the 5 preloaded sample tickets and classify them. 
2. Execute a Batch Run to analyze and output all five tickets at the same time. 
3. Type out and analyze completely custom support incidents using the manual text box input area.

## Future Improvements with More Time
- JSON Mode Forcing: Leverage structured output features provided by underlying runner architectures (e.g., Ollama/llama.cpp's format: "json" option) to constrain inference token paths natively instead of relying on post-generation corrections.

- Asynchronous Processing Tasks: Re-architect pipeline queries utilizing python asyncio or worker networks like Celery to process large volumes of text concurrently without freezing UI loops.

- Vector Embeddings (RAG): Connect historical enterprise ticketing resolutions into context windows using similarity search to improve recommended_action logic correctness.

## Technologies Used
- Python 3.11: Core programming runtime environment.
- Streamlit: A rapid python framework used to build the simplistic interactive Graphical User Interface (GUI).
- Ollama Engine: Orchestrates local, open-weights LLMs (such as llama3 or mistral) without calling external third-party cloud APIs.
- Pydantic v2: Handles technical payload structural validation, guaranteeing that output matches required schema constraints.
- Docker & Docker Compose: Wraps the entire ecosystem into decoupled, predictable network nodes that launch identically on any system.

## Required JSON Output Schema
Every ticket evaluated by the system is programmatically forced to match and satisfy this precise format

```JSON
{
  "category": "string",
  "priority": "low | medium | high | critical",
  "summary": "string",
  "recommended_action": "string"
}
```
Note: If a model generates missing properties or returns a priority outside the allowed array, the validation module intercepts the error, flags it, and safely notifies the user inside the interface.

## Project structure

The project is modularly isolated into logical layers separating configuration, prompt engineering, sample datasets, and runtime evaluation logic:

```text
mini-ticket-classifier/
│
├── src/
│   ├── __init__.py
│   ├── config.py         # App configuration parameters & constants
│   ├── prompt.py         # System & structural prompt engineering layouts
│   ├── tickets.py        # Complete list of 5 mock support tickets 
│   └── validator.py      # Pydantic schema guardrails and exception handlers
│
├── app.py                # Simplistic Streamlit GUI script 
├── Dockerfile            # Container definition for the web-app interface
├── docker-compose.yml    # Multi-container orchestration stack (App + LLM)
├── requirements.txt      # Third-party Python dependencies
└── README.md             # Project documentation and guide
```