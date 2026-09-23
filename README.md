# VFR-Flight-Weather-Assistant

## Description

This project comprises an intelligent, locally operated LLM-based flight weather assistant supporting private pilots in pre- and in-flight decision-making. It renders current and forecast airport weather conditions relevant for aviators applying visual flight rules (VFR). The combination of deterministic business logic flows and LLM language generation balances safe operation with nuanced natural language comprehension. Retrieval Augmented Generation (RAG) enables querying for VMC minima, safety regulations and general international rules of air definitions. 

DISCLAIMER: This assistant is created for **informational purposes only** and does not exercise any flight approval authority nor does it release the pilot-in-command from any obligations to check official sources or the responsibility for decisions made.

## Architecture & Stack

The assistant is based on the Rasa CALM (Conversational AI with Language Models) system integrating business logic flows, custom actions and LLM reasoning for real-time METAR, TAF and NOAA retrieval, parsing and translation into plain and concise English language.


* **Conversational AI:** Rasa Pro (CALM, Flows, Enterprise Search Policy)
* **LLM & Embeddings:** OpenAI (text-embedding-3-large, Modellgruppen)
* **Knowledge base (RAG):** FAISS Vector Store (./docs mit VFR-Regularien)
* **Backend & Schnittstellen**: Python, Uvicorn, Socket.IO
* **Containerisierung**: Docker & Docker Compose (für MCP-Dienste)
* **Datenquellen**: airportsdata für ICAO-Validierung
