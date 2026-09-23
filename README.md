# VFR-Flight-Weather-Assistant

This project comprises an intelligent, locally operated LLM-based flight weather assistant supporting private pilots in pre- and in-flight decision-making. It renders current and forecast aerodrome flight weather conditions relevant for aviators applying visual flight rules (VFR). The combination of deterministic business logic flows and LLM language generation balances  

## Description

## Architecture & Stack
* **Conversational AI:** Rasa Pro (CALM, Flows, Enterprise Search Policy)
* **LLM & Embeddings:** OpenAI (text-embedding-3-large, Modellgruppen)
* **Knowledge base (RAG):** FAISS Vector Store (./docs mit VFR-Regularien)
* **Backend & Schnittstellen**: Python, Uvicorn, Socket.IO
* **Containerisierung**: Docker & Docker Compose (für MCP-Dienste)
* **Datenquellen**: airportsdata für ICAO-Validierung
