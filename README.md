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
* **MCP Server**: FastMCP (for METAR, TAF, NOAA retrieval)
* **Data Sources**: airportsdata (for ICAO validation and resolving city names to a proper ICAO code)
