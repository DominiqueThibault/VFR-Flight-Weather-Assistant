# VFR-Flight-Weather-Assistant

## Description
The programme runs an intelligent local LLM-based flight weather agent configured to retrieve, translate and output METAR, TAF and NOAA data to plain and concise English language. As such it is built to support private pilots with pre- and in-flight decision-making by rendering relevant real-time flight weather information. Retrieval Augmented Generation (RAG) allows querying the Rasa data base for VMC minima, regulations and international air rule definitions. 

## Architecture & Stack
The agent is based on Rasa Pro (CALM) - balancing deterministic business logic flows & custom actions with LLM reasoning and response generation, Ollama/OpenAI and Enterprise Search (FAISS-RAG) for VFR rules. The entire process is managed by a multi-stack Docker container environment comprising 1) Rasa core logic, 2) LLM inference, 3) MCP server.

* **Conversational AI:** Rasa Pro (CALM, Flows, Custom Actions, Enterprise Search Policy)
* **LLM & Embedding:** OpenAI (gpt-5.1-2025-11-13/ text-embedding-3-large), Ollama (Llama 3.2) for edge mode operations
* **RAG**: FAISS vector store
* **MCP Server**: FastMCP
* **Backend / endpoints:** Python, Uvicorn, Socket.IO
* **API**: https://aviationweather.gov/api/data
* **Containerizing:** Docker & Docker Compose
* **Python libraries**: airportsdata (for ICAO validation & parsing), metar (for METAR parsing)

## Project Structure

├── actions/               # Rasa Custom Actions (z. B. airportsdata Integration)
├── data/                  # Rasa Flows, Patterns, Rules & Training-Stories
├── docs/                  # VFR Regulations, FAQs & Texts for FAISS-RAG
├── domain/                # Stores Memorie Slots, Responses, and Actions
├── mcp_servers/           # Docker-compatible MCP Server (weather_mcp)
├── sub-agent/             # Rasa ReAct Sub-Agent Configurations (prompts, connections, LLM model-groups)
├── .env.example/          # Contains OpenAI API Key and Rasa Licence Key 
├── Dockerfile.rasa/       # Manages Rasa Core Container 
├── config.yml             # Rasa Configurations (Policies, FlowPolicy, EnterpriseSearch)
├── credentials.yml        # Channels (e.g. Socket.IO config)
├── endpoints.yml          # Endpoints & LLM-/Embeddings Model-groups
├── requirements.txt       # Central Python Dependencies
└── docker-compose.yml     # Container Orchestration


## Installation & Setup

### Prerequisites
* **Python** (Version 3.11.9 or higher recommended; 3.14 requires Rasa Pro 3.19+)
* **Rasa Pro** (Version 3.18.1 or higher recommended)
* **Docker** (Version 29.8.0) & **Docker Compose** (for container service and weather MCP server)
* Valid **OpenAI API Key**
* Valid **Rasa License Key**

### Clone Repository
```bash
git clone [https://github.com/DominiqueThibault/Regression-Function-Mapping-/edit/main/README.md]
cd VFR-Flight-Weather-Assistant
```
### Create & Activate Virtual Environment
```bash
python -m venv venv
python3.11 -m venv .venv && source .venv/bin/activate
```
### Install Dependencies
```bash
pip install rasa-pro==3.18.1
pip install --upgrade pip
pip install -r requirements.txt
```
### Configurating Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
RASA_LICENSE=your_rasa_license_here

### Run the Programme
```bash
docker compose up --build
```
Make sure only vfr_mcp_server is running in detached mode to avoid port access failures.

```bash
docker compose up -d vfr_mcp_server
docker compose run --rm --service-ports rasa rasa shell --debug
```

## Model Training & Testing
For training run:
```bash
docker compose exec vfr_rasa_core rasa train
```

For testing with the Rasa Inspector run:
```bash
docker compose run --rm --service-ports vfr_rasa_core rasa inspect
```

## Author
Dominique Thibault
