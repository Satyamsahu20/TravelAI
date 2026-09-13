# TravelAI — Multi-Agent AI Travel Planning System

TravelAI is a multi-agent travel planning application built with **LangGraph**, **Google Gemini**, and the **Model Context Protocol (MCP)**. A supervisor agent analyzes each request, routes it to the right specialist agents, and produces a complete, structured trip itinerary — with input guardrails and human-in-the-loop approval built into the flow.

## Features

- **Supervisor Agent** — parses the user's request, validates it against guardrails, decides which specialist agents are needed, and extracts trip constraints (destination, origin, duration, budget, preferences)
- **Specialist Agents**
  - `flight_agent` — airport and airline lookups via AeroDataBox
  - `hotel_agent` — accommodation research via Tavily search
  - `weather_agent` — current conditions and forecasts via OpenWeatherMap
  - `budget_agent` — cost breakdowns and estimates
  - `itinerary_agent` — combines all agent outputs into a day-by-day plan
- **Guardrails** — validates that incoming requests are legitimate travel planning queries before any agent work begins
- **Human-in-the-Loop** — presents the draft itinerary for approval/feedback before generating the final response
- **Persistent Memory** — conversation state is checkpointed to MySQL via LangGraph's checkpointer, so sessions can resume
- **Automatic Retry** — transient LLM errors (e.g. model overload) are retried automatically before failing
- **Streamlit Frontend** — simple, interactive UI for entering trip requests and viewing results

## Architecture

```
User Request
     │
     ▼
Supervisor Agent (guardrail check + agent routing)
     │
     ├──► Flight Agent (AeroDataBox MCP)
     ├──► Hotel Agent (Tavily MCP)
     ├──► Weather Agent (OpenWeather MCP)
     └──► Budget Agent
     │
     ▼
Itinerary Agent (combines all results)
     │
     ▼
Human Approval (review / request changes)
     │
     ▼
Final Response Agent
```

## Tech Stack

| Component | Technology |
|---|---|
| Orchestration | LangGraph |
| LLM | Google Gemini (`gemini-flash-latest`) |
| Tool Protocol | Model Context Protocol (MCP) |
| Flight Data | AeroDataBox (via RapidAPI) |
| Weather Data | OpenWeatherMap |
| Web Search | Tavily |
| Memory / Checkpointing | MySQL |
| Frontend | Streamlit |

## Project Structure

The codebase is organized into three clear layers: agent logic, shared infrastructure, and standalone tool servers.

```
TravelAI/
├── agents/                    # Agent definitions, one file per agent
│   ├── __init__.py
│   ├── supervisor.py           # Routes requests + input guardrail
│   ├── flight_agent.py
│   ├── hotel_agent.py
│   ├── weather_agent.py
│   ├── budget_agent.py
│   ├── itinerary_agent.py
│   ├── human_approval.py       # Human-in-the-loop interrupt
│   └── final_response.py
├── core/                      # Shared orchestration and infrastructure
│   ├── __init__.py
│   ├── state.py                 # TravelState schema
│   ├── llm_utils.py             # LLM call wrapper with retry logic
│   ├── mcp_client.py            # MCP server connections
│   └── graph.py                 # LangGraph state graph + MySQL checkpointer
├── mcp_servers/                # Standalone MCP tool servers
│   ├── flight_mcp_server.py      # AeroDataBox integration
│   └── weather_mcp_server.py     # OpenWeatherMap integration
├── config.py                   # Environment variables + LLM configuration
├── frontend.py                  # Streamlit UI
├── requirements.txt
├── .env                          # API keys and DB credentials (not committed)
└── .gitignore
```

## Prerequisites

- Python 3.11+
- MySQL Server 8.0.19+ (running locally or remotely)
- API keys for:
  - [Google AI Studio](https://ai.google.dev/) (Gemini)
  - [Tavily](https://tavily.com/)
  - [AeroDataBox on RapidAPI](https://rapidapi.com/aedbx-aedbx/api/aerodatabox)
  - [OpenWeatherMap](https://openweathermap.org/)

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd TravelAI
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL**
   ```sql
   CREATE DATABASE langgraph_memory;
   ```

5. **Configure environment variables**

   Create a `.env` file in the project root:
   ```dotenv
   GEMINI_API_KEY=your_gemini_key
   GEMINI_MODEL=gemini-flash-latest

   TAVILY_API_KEY=your_tavily_key
   AERODATABOX_API_KEY=your_aerodatabox_key
   OPENWEATHER_API_KEY=your_openweather_key

   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=langgraph_memory
   ```

   > MySQL credentials are stored as separate fields (not a single connection URL), so passwords containing special characters like `#` don't need URL-encoding.

6. **Set local paths in `core/mcp_client.py`**

   Update these two variables to match your machine:
   ```python
   VENV_PYTHON = r"C:\path\to\TravelAI\.venv\Scripts\python.exe"
   PROJECT_DIR = r"C:\path\to\TravelAI"
   ```

## Running the App

**Always run from the project root** — the `core` and `agents` imports are resolved relative to the working directory.

```bash
streamlit run frontend.py
```

This opens the app at `http://localhost:8501`. Enter a trip request (e.g. *"Plan a 5 day trip to Goa under 50,000 rupees"*) and the multi-agent pipeline will generate a draft itinerary for review and approval.

## Known Limitations

- Google Gemini's free tier is limited to 20 requests/day per model — a full trip plan uses several LLM calls, so this is easy to exhaust during testing.
- AeroDataBox's free RapidAPI tier has a monthly request cap; check current limits on your RapidAPI dashboard.
- This is a portfolio/learning project, not a production booking system — it does not process payments or make real reservations.

## License

This project is for educational and portfolio purposes.
