# VFR-Flight-Weather-Assistant

## Description
This project was developed as part of the International University of Applied Sciences' seminar 'AI Use Case'.

The programme runs an LLM-based flight weather agent configured to retrieve, translate and output METAR, TAF and NOAA data into plain and concise English language. 

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
### Create & activate virtual environment
```bash
python -m venv venv
python3.11 -m venv .venv && source .venv/bin/activate
```
### Install dependencies
```bash
pip install rasa-pro==3.18.1
pip install --upgrade pip
pip install -r requirements.txt
```
### Install environment variables
OPENAI_API_KEY=your_openai_api_key_here
RASA_LICENSE=your_rasa_license_here

### Run the programme
```bash
docker compose up --build
docker compose up -d vfr_mcp_server
docker compose run --rm --service-ports rasa rasa shell --debug
```

## Model training & testing
For training run:
```bash
docker compose exec vfr_rasa_core rasa train
```

For testing with the Rasa Inspector run:
```bash
docker compose run --rm --service-ports vfr_rasa_core rasa inspect
```

## Technologies

## Author
