# VFR-Flight-Weather-Assistant

## Description
This project comprises an intelligent, locally operated LLM-based flight weather assistant supporting private pilots in pre- and in-flight decision-making. It renders current and forecast airport weather conditions relevant for aviators applying visual flight rules (VFR). The combination of deterministic business logic flows and LLM language generation balances safe operation with nuanced natural language comprehension. Retrieval Augmented Generation (RAG) enables querying for VMC minima, safety regulations and general international rules of air definitions. 

**DISCLAIMER**: This assistant is created for **informational purposes only** and does not exercise any flight approval authority nor does it release the pilot-in-command from any obligations to check official flight weather sources or from the responsibility for decisions made.

## Architecture & Stack
The assistant is based on the Rasa CALM (Conversational AI with Language Models) system integrating business logic flows, custom actions and LLM reasoning for real-time METAR, TAF and NOAA retrieval, parsing and translation into plain and concise English language.
The entire process is managed by a multi-stack Docker container environment storing 1) the Rasa core logic, 2) the LLM inference, and 3) the MCP server.


* **Conversational AI:** Rasa Pro (CALM, Flows, Custom Actions, EnterpriseSearchPolicy)
* **LLM & Embeddings:** OpenAI (text-embedding-3-large, gpt-5.1-2025-11-13), Ollama (Llama 3.2)
* **Knowledge base (RAG):** FAISS (Facebook AI Similarity Search) Vector Store (./docs with ICAO international Rule of Air excerpts)
* **Backend & Endpoints**: Python, Uvicorn, Socket.IO
* **Containerisierung**: Docker & Docker Compose (für MCP-Dienste)
* **Datenquellen**: airportsdata für ICAO-Validierung
