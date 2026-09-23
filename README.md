# VFR-Flight-Weather-Assistant

## Description
This project comprises an intelligent, locally operated LLM-based flight weather assistant supporting private pilots in pre- and in-flight decision-making. It renders current and forecast airport weather conditions relevant for aviators applying visual flight rules (VFR). The combination of deterministic business logic flows and LLM language generation balances safe operation with nuanced natural language comprehension. Retrieval Augmented Generation (RAG) enables querying for VMC minima, safety regulations and general international Rules of Air definitions. 

**DISCLAIMER**: This assistant is created for **informational purposes only** and does not exercise any flight approval authority nor does it release the pilot-in-command from any obligations to check official flight weather sources or from the responsibility for decisions made.

## Architecture & Stack
The set-up is based on the Rasa CALM (Conversational AI with Language Models) system integrating business logic flows, custom actions and LLM reasoning for real-time METAR, TAF and NOAA retrieval, parsing and translation into plain and concise English language.
The entire process is managed by a multi-stack Docker container environment storing 1) the Rasa core logic, 2) the LLM inference, and 3) the MCP server.


* **Conversational AI:** Rasa Pro, 3.18.1 or higher recommended
* **LLM & Embeddings:** OpenAI (gpt-5.1-2025-11-13, text-embedding-3-large), Ollama (Llama 3.2)
* **Knowledge base (RAG):** FAISS (Facebook AI Similarity Search) vector store (./docs with ICAO international Rule of Air excerpts)
* **Backend & Endpoints**: Python (version 3.11.9 or higher recommended, 3.14x for Rasa pro 3.19x), Uvicorn, Socket.IO, REST 
* **Containerizing**: Docker (29.8.0) & Docker Compose (for multi-stack management)
* **MCP Server**: FastMCP (for METAR, TAF, NOAA retrieval) enabling tool call via https://aviationweather.gov API
* **Data Sources**: airportsdata (for ICAO validation and resolving city names to a proper ICAO code)

## Project Structure

├── actions/               # Rasa Custom Actions (e.g. airportsdata integration)
├── data/                  # Rasa Flows, Rules, Patterns & Training-Stories
├── docs/                  # VFR Regulations, FAQs & Texts for FAISS RAG
├── domain/                # Memory Slots, Responses, Actions 
├── mcp_server/            # Docker compatible MCP Server
├── sub-agents/            # Sub-Agent Configuration
├── .env.example           # Template for Environment File (API Keys, License Key, Tokens)
├── Dockerfile.rasa        # Defines Rasa Core Logic Container in Docker
├── config.yml             # Rasa Konfiguration (Policies, FlowPolicy, EnterpriseSearch)
├── credentials.yml        # Channels (e.g. Socket.IO, REST, and UI channels)
├── docker-compose.yml     # Container Orchestration
├── endpoints.yml          # Endpoints & LLM-/Embeddings
├── requirements.txt       # Central Python Dependencies (e.g. metar, fastmcp)

## Pre-conditions & Installation

### Clone Repository
```bash
git clone [https://github.com/DominiqueThibault/VFR-Flight-Weather-Assistant]
cd VFR-Flight-Weather-Assistant
```

### Create virtual environment
```bash
uv venv --python 3.11
# macOS/Linux:
source venv/bin/activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
```
### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### Configuration & Environment Variables
1. Request free Rasa license key here: https://rasa.com/rasa-pro-developer-edition-license-key-request
2. Get OpenAI API Key here: https://openai.com/de-DE/index/openai-api/
3. Create an .env file in your main directory that stores:
```bash
RASA_LICENSE_KEY=your_rasa_license_key_here
OPENAI_API_KEY=your_openai_api_key_here
```
### Execution & Start
1. Run Docker Environment:
```bash
docker compose up --build
docker compose ps 
```
2. Train the Model: The trained model is intentionally **not included in the repository** and needs to be generated locally.
```bash
docker compose exec vfr_rasa_core rasa train
```
4. Test the Model: This runs the Rasa Inspector, an in-browser testing & debugging panel with visualized logic & workflows.
```bash
docker compose down
docker compose up -d vfr_mcp_server
```

```bash
docker compose run --rm --service-ports vfr_rasa_core rasa inspect
```

5. Load your trained model and talk to your assistant on the command line.
```bash
rasa shell --debug
```

OR

6. Start a server with your trained model.
```bash
rasa run
```

## Limitations
* METAR/TAF/NOOA only
* No chitchat

## Future Improvements
*

## Author
Dominique Thibault
