# 🚢 Marine Risk AI - Quick Reference Guide

## 🎯 What Is This?

An **AI-powered risk assessment system** for ocean marine insurance that replaces hours of manual work with **sub-60 second automated analysis**.

## 💰 Business Impact

- **Problem**: Ships lose $50,000+ per day waiting for insurance approval
- **Solution**: Automated AI assessment in <60 seconds
- **Savings**: $50K-$150K per ship, $5M-$15M annually (100 ships)

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│         React Frontend (Port 3000)                       │
│    Red & White Theme | 7 Components | Recharts          │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ REST API / WebSocket
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   BACKEND API                            │
│         FastAPI + Python (Port 8000)                     │
│     /api/analyze | /api/health | /ws/analyze            │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Orchestrates
                 ▼
┌─────────────────────────────────────────────────────────┐
│                 AI AGENT SYSTEM                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  ORCHESTRATOR (State Machine Coordinator)        │   │
│  └──────────┬───────────────────────────────────────┘   │
│             │                                            │
│     ┌───────┴───────┬───────┬───────┬───────┬───────┐  │
│     ▼               ▼       ▼       ▼       ▼       ▼  │
│  ┌──────┐  ┌──────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐  │
│  │Entity│  │Sanct-│  │News│  │Weat│  │Route│  │Hist│  │
│  │Extract│ │ions │  │Sent│  │her │  │Risk│  │orical│  │
│  └──────┘  └──────┘  └────┘  └────┘  └────┘  └────┘  │
│     │         │        │       │       │        │      │
│  ┌──▼─────────▼────────▼───────▼───────▼────────▼───┐ │
│  │          TOOLS & UTILITIES                        │ │
│  │  Scrapers | Validators | Calculators | Explainers│ │
│  └──────────────────────────────────────────────────┘ │
└─────────────────┬───────────────────────────────────────┘
                  │
          ┌───────┴────────┐
          ▼                ▼
    ┌──────────┐    ┌──────────┐
    │PostgreSQL│    │  Redis   │
    │ (History)│    │ (Cache)  │
    └──────────┘    └──────────┘
          ▲                
          │ Local LLM
          ▼
    ┌──────────┐
    │  Ollama  │
    │qwen2.5:3b│
    └──────────┘
```

## 🤖 AI Agent Workflow

```
User Input → Entity Extractor → Parallel Execution:
                                    ├─ Sanctions Check
                                    ├─ Vessel Verification
                                    ├─ News Analysis
                                    ├─ Weather Assessment
                                    ├─ Route Risk
                                    └─ Historical Patterns
                                         ↓
                                  Risk Calculation
                                         ↓
                                  Decision: Accept/Conditional/Review
```

## 📊 Risk Scoring Formula

```
Overall Risk = (Regulatory × 15%) + (Reputation × 20%) + 
               (Route × 30%) + (Weather × 15%) + 
               (Vessel × 10%) + (Cargo × 10%)

Decision Logic:
├─ 0-40:   Accept (Low Risk)         → Premium: +0-5%
├─ 40-70:  Accept with Conditions    → Premium: +5-20%
└─ 70-100: Manual Review (High Risk) → Premium: +20-30%
```

## 🚀 Quick Start (3 Steps)

```bash
# 1. Install Ollama model
ollama pull qwen2.5:3b

# 2. Start the system
cd marine-risk-ai
./start.sh

# 3. Open browser
open http://localhost:3000
```

## 📝 Sample Input

```yaml
Vessel Name: MV Neptune Star
IMO Number: IMO9547821
Owner: Neptune Maritime Corp
Registry: Panama
Route: Rotterdam → Shanghai
Cargo: Container
```

## 📈 Output Includes

1. **Overall Risk Score** (0-100) with color coding
2. **Decision** (Accept/Conditional/Manual Review)
3. **6 Risk Categories** with detailed breakdowns
4. **3 Interactive Charts** (Radar, Bar, Pie)
5. **AI Recommendations** with conditions
6. **Complete Timeline** of agent actions
7. **Data Sources** with reliability scores
8. **Historical Context** from 50+ applications

## 🛡️ Hallucination Prevention

```
Layer 1: Source Verification (URL, timestamp, checksum)
Layer 2: Cross-Reference (2+ sources)
Layer 3: Structured Output (Pydantic models)
Layer 4: Reasoning Chain (ReAct pattern)
Layer 5: Human-in-Loop (Auto-flag edge cases)
```

## 🎨 UI Components

```
┌─────────────────────────────────────────┐
│ 🚢 Agentic AI - Risk Insight            │ ← Header (Red)
├─────────────────────────────────────────┤
│ Input Form (7 fields + validation)      │ ← Form Section
├─────────────────────────────────────────┤
│ ┌────────────┐  ┌──────────────────┐   │
│ │ Risk Score │  │ Decision Badge   │   │ ← Score Card
│ │   45.2     │  │ Accept w/Cond    │   │
│ └────────────┘  └──────────────────┘   │
├─────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│ │Regul.│ │Reputa│ │Route │ │Weath.│   │ ← Categories
│ │ 20   │ │ 45   │ │ 65   │ │ 30   │   │
│ └──────┘ └──────┘ └──────┘ └──────┘   │
├─────────────────────────────────────────┤
│ ┌───────┐ ┌───────┐ ┌───────┐         │
│ │ Radar │ │  Bar  │ │  Pie  │         │ ← Charts
│ │Chart  │ │ Chart │ │ Chart │         │
│ └───────┘ └───────┘ └───────┘         │
├─────────────────────────────────────────┤
│ Recommendations Panel                   │ ← AI Insights
├─────────────────────────────────────────┤
│ [Timeline][Categories][Reasoning]...    │ ← Event Tabs
└─────────────────────────────────────────┘
```

## 📁 File Structure

```
marine-risk-ai/
├── 📖 README.md (370+ lines)
├── 📋 IMPLEMENTATION_SUMMARY.md
├── 🐳 docker-compose.yml
├── 🚀 start.sh
├── 🔧 .env.example
├── 🐍 backend/ (23 files)
│   ├── agents/ (8 agents)
│   ├── tools/ (4 utilities)
│   ├── database/ (models + mock data)
│   └── api/ (FastAPI + WebSocket)
└── ⚛️  frontend/ (16 files)
    ├── components/ (7 React components)
    ├── package.json
    └── tailwind.config.js
```

## 🔍 API Endpoints

```
GET  /                  → Welcome message
GET  /api/health        → System health check
POST /api/analyze       → Risk assessment (main)
GET  /api/historical    → Historical data
GET  /api/statistics    → System statistics
WS   /ws/analyze        → Real-time updates
GET  /docs              → Swagger UI
```

## ⚡ Performance

- **Target**: <60 seconds
- **Expected**: 10-30 seconds (local Ollama)
- **Parallel**: 6 agents concurrent
- **Caching**: Redis (sanctions: 24h, weather: 1h)

## 🔒 Security

- ✅ CodeQL Scan: 0 vulnerabilities
- ✅ Input validation (IMO format, required fields)
- ✅ SQL injection protection (ORM)
- ✅ CORS configured
- ✅ No hardcoded secrets

## 📊 Mock Data Included

- 50 Historical Applications
- 3 Claims Records
- 5 Vessel Registry Entries
- 5 Sanctioned Entities
- 6 Route Risk Areas
- 4 Weather Patterns

## 🎯 Key Features

✅ Sub-60 second analysis
✅ 8 AI agents with orchestration
✅ Complete transparency (ReAct reasoning)
✅ Interactive visualizations
✅ Historical pattern matching
✅ Real-time WebSocket updates
✅ Red & white professional theme
✅ Mobile responsive
✅ Docker containerized
✅ 100% local (no API keys)

## 🐛 Troubleshooting

```bash
# Ollama not connected
ollama list
ollama pull qwen2.5:3b

# Port already in use
docker-compose down
docker-compose up

# Database issues
docker-compose restart postgres

# View logs
docker-compose logs backend
docker-compose logs frontend
```

## 📞 Support

- 📖 Full docs: README.md
- 🔧 API docs: http://localhost:8000/docs
- 💬 Issues: GitHub Issues
- 📧 Test script: backend/test_backend.py

## ⚠️ Important Notes

1. **Demonstration System**: Uses mock data for scrapers
2. **Local LLM Required**: Ollama must be running
3. **Not Production-Ready**: Requires real data sources
4. **No Authentication**: Single-user demonstration
5. **Educational Purpose**: Reference implementation

## 🎓 Learning Points

- Agentic AI architecture
- LangGraph orchestration
- FastAPI async patterns
- React component design
- Docker multi-container apps
- Risk assessment algorithms
- Hallucination prevention
- Transparency in AI

## 📈 Next Steps

1. Deploy locally: `./start.sh`
2. Test with sample data
3. Explore all UI components
4. Review agent reasoning
5. Check API documentation
6. Examine source code
7. Consider production hardening

---

**Built for**: Marine insurance industry
**Solves**: $50K/day port delays
**Tech Stack**: React + FastAPI + Ollama + PostgreSQL + Redis
**Status**: ✅ Complete & Ready
