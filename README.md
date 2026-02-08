# 🚢 Marine Risk AI - 360° External Risk Insight

**Agentic AI system for ocean marine insurance underwriting with <60 second turnaround**

## 🎯 Business Problem

Ships lose **$50,000+ per day** sitting in port waiting for insurance approval. Manual underwriting takes hours or days. This AI system provides comprehensive risk assessment in **under 60 seconds** with full transparency.

## ✨ Features

- ⚡ **Sub-60 second risk assessment** - Massive time savings vs traditional underwriting
- 🤖 **6 specialist AI agents** - Sanctions, Vessel, News, Weather, Route, Historical analysis
- 🔍 **Web scraping + mock data fallback** - Real-world data sources with reliable fallbacks
- 📊 **Complete transparency** - Full reasoning chains, data sources, confidence scores
- 📈 **Historical trend analysis** - Learn from 47+ past applications
- 🎨 **Professional red & white UI** - Clean, intuitive dashboard
- 🔒 **100% local** - No API keys needed, runs on Ollama
- 🛡️ **5-layer hallucination prevention** - Cross-validation, structured outputs, reasoning chains

## 🏗️ Architecture

```
REACT FRONTEND (Vite + TailwindCSS + Recharts)
  ↕ REST API + WebSocket
PYTHON BACKEND (FastAPI + LangChain + LangGraph)
  ↕ 
OLLAMA (qwen2.5:3b - Local LLM)
  ↕ 
TOOLS (Web Scrapers + Mock Data Fallback)
  ↕
POSTGRESQL + REDIS
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (required)
- **Ollama** installed locally ([Download here](https://ollama.ai))
- **8GB+ RAM** recommended
- **Git** for cloning

### Installation

**1. Install Ollama model:**

```bash
ollama pull qwen2.5:3b
```

**2. Clone and start the application:**

```bash
git clone https://github.com/navya-glitch/marine-risk-ai.git
cd marine-risk-ai
docker-compose up --build
```

Wait for all services to start (2-3 minutes). You'll see:
- ✅ PostgreSQL ready
- ✅ Redis ready
- ✅ Backend API running on port 8000
- ✅ Frontend running on port 3000

**3. Access the application:**

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

## 📖 Usage Guide

### Basic Workflow

1. **Open the dashboard** at http://localhost:3000

2. **Enter vessel details:**
   - Vessel Name: `MV Neptune Star`
   - IMO Number: `IMO9547821` (format: IMO + 7 digits)
   - Owner Company: `Neptune Maritime Corp`
   - Country of Registry: Select from dropdown
   - Departure Port: `Rotterdam`
   - Destination Port: `Shanghai`
   - Cargo Type: `Container`

3. **Click "🔍 Analyze Risk"**

4. **View comprehensive analysis** in <60 seconds:
   - Overall risk score (0-100)
   - Decision recommendation (Accept/Conditional/Manual Review)
   - 6 risk categories with detailed breakdowns
   - Interactive charts (Radar, Bar, Pie)
   - AI recommendations and mitigation options
   - Complete timeline and reasoning

5. **Explore the Event Tab:**
   - **Timeline:** Chronological event log
   - **Categories:** Detailed risk analysis
   - **Agent Reasoning:** Complete AI thought process (ReAct pattern)
   - **Evidence:** Data sources with reliability scores
   - **Historical Trends:** Pattern analysis from 47+ applications

### Sample Test Data

Try these pre-configured vessels from mock data:

| Vessel Name | IMO Number | Owner | Risk Level |
|-------------|------------|-------|------------|
| MV Neptune Star | IMO9547821 | Neptune Maritime Corp | Low |
| Atlantic Voyager | IMO9123456 | Atlantic Shipping Ltd | Medium |
| Pacific Princess | IMO9234567 | Pacific Oil Transport | Low |

## 🧠 How It Works

### AI Agent Workflow

1. **Entity Extractor** - Extracts and validates vessel details with confidence scores
2. **Sanctions Agent** - Checks OFAC/EU/UN sanctions databases
3. **Vessel Agent** - Verifies vessel in registry, calculates age risk
4. **News Agent** - Scrapes maritime news, analyzes sentiment
5. **Weather Agent** - Assesses seasonal risks and delay probability
6. **Route Agent** - Evaluates piracy and geopolitical risks
7. **Historical Agent** - Finds similar past applications, calculates patterns
8. **Orchestrator** - Coordinates all agents, calculates final risk score

### Risk Scoring Formula

```
Overall Risk = (Regulatory × 15%) + (Reputation × 20%) + (Route × 30%) + 
               (Weather × 15%) + (Vessel × 10%) + (Cargo × 10%)
```

**Decision Logic:**
- Score < 40: **Accept** (low risk)
- Score 40-70: **Accept with conditions** (moderate risk)
- Score > 70: **Manual review** (high risk)

### 5-Layer Hallucination Prevention

1. **Source Verification** - Every data point includes URL, timestamp, checksum
2. **Cross-Reference Validation** - IMO/owner verified across 2+ sources
3. **Structured Output** - Pydantic models, no free-form critical data
4. **Reasoning Chain** - Complete ReAct thought process logged
5. **Human-in-Loop Flags** - Auto-flag if confidence <85%, mismatches detected, sanctions found, vessel age >20 years

## 📊 Components

### Backend Agents (`backend/agents/`)

- `orchestrator.py` - Main coordinator (LangGraph state machine)
- `entity_extractor.py` - NER for vessel/owner/route extraction
- `sanctions_agent.py` - OFAC/EU sanctions checker
- `vessel_agent.py` - Equasis registry scraper + verification
- `news_agent.py` - Maritime news scraper + sentiment analysis
- `weather_agent.py` - Seasonal weather risk assessment
- `route_agent.py` - Piracy + geopolitical risk analysis
- `historical_agent.py` - Pattern matching from 47+ applications

### Backend Tools (`backend/tools/`)

- `scrapers.py` - Async web scraping with fallback to mock data
- `validators.py` - Cross-reference validation, IMO format checking
- `calculators.py` - Risk scoring algorithms with transparency
- `explainers.py` - Human-readable explanations for AI decisions

### Frontend Components (`frontend/src/components/`)

- `Dashboard.jsx` - Main container with API integration
- `InputForm.jsx` - Vessel input form with validation
- `RiskScore.jsx` - Large score card with breakdown
- `CategoryBreakdown.jsx` - 6 risk category cards
- `Charts.jsx` - Recharts (Radar, Bar, Pie)
- `Recommendations.jsx` - AI decision panel
- `EventTab.jsx` - 5 sub-tabs (Timeline, Categories, Reasoning, Evidence, Trends)

## 🔧 Development

### Running Backend Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on http://localhost:3000

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
DATABASE_URL=postgresql://marineuser:marinepass@localhost:5432/marine_risk
REDIS_URL=redis://localhost:6379
```

## 📁 Project Structure

```
marine-risk-ai/
├── backend/
│   ├── agents/              # 7 AI agents
│   ├── tools/               # Scrapers, validators, calculators
│   ├── database/            # Models, mock data, connection
│   ├── api/                 # FastAPI app, routes, WebSocket
│   ├── config.py            # Configuration
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.jsx          # Main app
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Styles
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite config
│   ├── tailwind.config.js   # TailwindCSS config
│   └── Dockerfile
├── docker-compose.yml       # Multi-container orchestration
├── .env.example             # Environment template
└── README.md
```

## 🐛 Troubleshooting

### Ollama Connection Error

**Problem:** Backend shows "Ollama not connected"

**Solution:**
```bash
# Check Ollama is running
ollama list

# Pull model if missing
ollama pull qwen2.5:3b

# For Docker on Mac/Windows, ensure host.docker.internal is accessible
```

### Port Already in Use

**Problem:** Error: "Address already in use"

**Solution:**
```bash
# Check what's using the port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Stop Docker and restart
docker-compose down
docker-compose up
```

### Database Connection Error

**Problem:** Backend can't connect to PostgreSQL

**Solution:**
```bash
# Restart database service
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Slow Performance

**Problem:** Analysis takes >60 seconds

**Solution:**
- Ensure Ollama model is downloaded: `ollama pull qwen2.5:3b`
- Check system resources (8GB+ RAM recommended)
- Verify Redis is running for caching: `docker-compose ps`

## 🧪 Testing

### API Testing

Use the built-in Swagger UI at http://localhost:8000/docs

Or with curl:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "vessel_name": "MV Neptune Star",
    "imo_number": "IMO9547821",
    "owner": "Neptune Maritime Corp",
    "country_of_registry": "Panama",
    "departure_port": "Rotterdam",
    "destination_port": "Shanghai",
    "cargo_type": "Container"
  }'
```

### Health Check

```bash
curl http://localhost:8000/api/health
```

## 🎨 UI Theme

**Color Scheme:**
- Primary Red: `#DC2626`, `#EF4444`
- White Background: `#FFFFFF`
- Dark Gray: `#1F2937`
- Light Gray: `#F3F4F6`
- Success Green: `#10B981`
- Warning Amber: `#F59E0B`

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💡 Future Enhancements

- [ ] Real-time web scraping (currently uses mock fallback)
- [ ] Integration with real Equasis API
- [ ] Integration with live sanctions databases
- [ ] Historical data persistence to database
- [ ] User authentication and multi-tenancy
- [ ] Export reports to PDF
- [ ] Email notifications for high-risk cases
- [ ] Advanced analytics dashboard
- [ ] Mobile app

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at http://localhost:8000/docs

## ⚠️ Disclaimer

This is a demonstration system using mock data and simplified risk models. **Not intended for production insurance underwriting without proper validation, compliance review, and real data sources.**

---

**Built with ❤️ for the marine insurance industry**

*Solving real business problems: Ships losing $50K/day in port waiting for insurance approval*
