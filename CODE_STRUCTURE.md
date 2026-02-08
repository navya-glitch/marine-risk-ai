# 📂 Code Structure Guide - Where to Find Everything

This document provides a complete map of all code files in the Marine Risk AI repository, making it easy to find and understand each component.

## 🗺️ Repository Overview

The repository is organized into three main sections:
1. **Backend** - Python FastAPI application with AI agents
2. **Frontend** - React application with TailwindCSS
3. **Infrastructure** - Docker, configuration, and documentation

---

## 🐍 BACKEND CODE (`/backend` directory)

### 📍 Entry Point
- **`backend/api/main.py`** (238 lines)
  - Main FastAPI application
  - REST API endpoints (`/api/analyze`, `/api/health`, etc.)
  - WebSocket endpoint for real-time updates
  - CORS configuration
  - **START HERE** to understand the API

### 🤖 AI Agents (`/backend/agents/`)

All AI agents that perform risk assessment:

1. **`orchestrator.py`** (219 lines) 
   - Main coordinator that runs all agents
   - State machine pattern
   - Aggregates results from all agents
   - **Core orchestration logic**

2. **`entity_extractor.py`** (73 lines)
   - Extracts entities from user input
   - Validates IMO number format
   - Provides confidence scores

3. **`sanctions_agent.py`** (51 lines)
   - Checks OFAC/EU sanctions lists
   - Cross-references owner and IMO number

4. **`vessel_agent.py`** (67 lines)
   - Verifies vessel in registry
   - Calculates vessel age risk
   - Cross-references with user input

5. **`news_agent.py`** (61 lines)
   - Scrapes maritime news
   - Analyzes sentiment
   - Checks historical claims

6. **`weather_agent.py`** (54 lines)
   - Analyzes seasonal weather patterns
   - Assesses delay probability

7. **`route_agent.py`** (58 lines)
   - Analyzes piracy and geopolitical risks
   - Evaluates route segments

8. **`historical_agent.py`** (99 lines)
   - Finds similar past applications
   - Calculates acceptance rates
   - Provides pattern-based recommendations

### 🛠️ Tools (`/backend/tools/`)

Utility functions used by agents:

1. **`scrapers.py`** (138 lines)
   - Async web scraping functions
   - Mock data fallback mechanisms
   - Redis caching integration
   - **Data collection logic**

2. **`validators.py`** (152 lines)
   - IMO format validation
   - Cross-reference validation
   - Data quality assessment
   - Manual review flag logic

3. **`calculators.py`** (246 lines)
   - Risk scoring algorithms
   - Category-specific calculations
   - Overall risk aggregation
   - **Core risk calculation math**

4. **`explainers.py`** (307 lines)
   - Human-readable explanations
   - Confidence score explanations
   - Recommendation generation
   - Business insights

### 🗄️ Database (`/backend/database/`)

1. **`models.py`** (38 lines)
   - SQLAlchemy models
   - Application and Claims tables

2. **`connection.py`** (18 lines)
   - Database connection setup
   - Session management

3. **`mock_data.py`** (274 lines)
   - 50 historical applications
   - Mock sanctions data
   - Mock vessel registry
   - Route and weather risk data
   - **All sample data**

### ⚙️ Configuration

- **`config.py`** (28 lines)
  - Environment variables
  - Risk weights and thresholds
  - Cache expiry settings

- **`requirements.txt`** (17 lines)
  - Python dependencies
  - All package versions

- **`test_backend.py`** (87 lines)
  - Backend test script
  - Validates all agents

---

## ⚛️ FRONTEND CODE (`/frontend` directory)

### 📍 Entry Points

- **`frontend/src/main.jsx`** (9 lines)
  - React application entry point
  - Renders root App component

- **`frontend/src/App.jsx`** (11 lines)
  - Main App component
  - Renders Dashboard

### 🎨 Components (`/frontend/src/components/`)

All React UI components:

1. **`Dashboard.jsx`** (80 lines)
   - Main container component
   - API integration
   - Loading and error states
   - **START HERE** for frontend

2. **`InputForm.jsx`** (235 lines)
   - 7-field vessel input form
   - IMO validation
   - Entity recognition badges
   - **User input interface**

3. **`RiskScore.jsx`** (110 lines)
   - Large risk score display
   - Color-coded by risk level
   - Expandable calculation breakdown

4. **`CategoryBreakdown.jsx`** (166 lines)
   - 6 risk category cards
   - Progress bars
   - Expandable details

5. **`Charts.jsx`** (94 lines)
   - Radar chart (multi-dimensional view)
   - Bar chart (historical comparison)
   - Pie chart (risk contribution)
   - **Uses Recharts library**

6. **`Recommendations.jsx`** (138 lines)
   - Primary decision display
   - Required conditions
   - Risk mitigation options
   - Business insights

7. **`EventTab.jsx`** (402 lines)
   - 5 sub-tabs:
     - Timeline (event log)
     - Categories (detailed analysis)
     - Agent Reasoning (ReAct pattern)
     - Evidence (data sources)
     - Historical Trends (patterns)
   - **Complete transparency view**

### 🎨 Styling

- **`frontend/src/index.css`** (35 lines)
  - Global styles
  - TailwindCSS imports
  - Custom scrollbar

### ⚙️ Configuration

- **`frontend/package.json`** (19 lines)
  - Dependencies (React, Recharts, Axios)
  - Build scripts

- **`frontend/vite.config.js`** (9 lines)
  - Vite configuration
  - Dev server settings

- **`frontend/tailwind.config.js`** (17 lines)
  - Brand colors (red theme)
  - Content paths

- **`frontend/postcss.config.js`** (6 lines)
  - PostCSS plugins

- **`frontend/index.html`** (11 lines)
  - HTML entry point

---

## 🐳 INFRASTRUCTURE

### Docker Configuration

- **`docker-compose.yml`** (47 lines)
  - 4 services: frontend, backend, postgres, redis
  - Port mappings
  - Volume mounts

- **`backend/Dockerfile`** (7 lines)
  - Python backend container

- **`frontend/Dockerfile`** (7 lines)
  - Node.js frontend container

### Scripts

- **`start.sh`** (42 lines)
  - Automated startup script
  - Dependency checks (Docker, Ollama)
  - Service orchestration

### Configuration

- **`.env.example`** (4 lines)
  - Environment variable template

- **`.gitignore`** (40 lines)
  - Files to exclude from git

---

## 📚 DOCUMENTATION

All documentation files in root directory:

1. **`README.md`** (370+ lines)
   - Complete setup guide
   - Usage instructions
   - Troubleshooting
   - **START HERE** for project overview

2. **`QUICK_REFERENCE.md`** (299 lines)
   - Architecture diagrams
   - Quick start guide
   - Component breakdown

3. **`IMPLEMENTATION_SUMMARY.md`** (353 lines)
   - Technical implementation details
   - Metrics and statistics
   - Quality assessment

4. **`PROJECT_COMPLETION_REPORT.md`** (448 lines)
   - Final completion status
   - All deliverables
   - Acceptance criteria

5. **`SECURITY_FIXES.md`** (250+ lines)
   - Vulnerability tracking
   - Patch details
   - Security status

---

## 🎯 How to Navigate by Use Case

### "I want to understand the risk calculation"
→ `backend/tools/calculators.py` (lines 1-246)

### "I want to see the AI agent logic"
→ `backend/agents/orchestrator.py` (main coordinator)
→ Individual agents in `backend/agents/`

### "I want to modify the UI"
→ `frontend/src/components/` (all React components)

### "I want to add a new API endpoint"
→ `backend/api/main.py`

### "I want to change the mock data"
→ `backend/database/mock_data.py`

### "I want to adjust risk weights"
→ `backend/config.py` (RISK_WEIGHTS)

### "I want to modify the color scheme"
→ `frontend/tailwind.config.js` (brand colors)

### "I want to see the deployment setup"
→ `docker-compose.yml` and `start.sh`

---

## 📊 Code Statistics

```
Total Files:              46
Total Lines:              ~8,000

Backend:
  - Python files:         23
  - Lines of code:        ~4,000
  - AI Agents:            8
  - Tools:                4

Frontend:
  - JavaScript/JSX:       16
  - Lines of code:        ~3,000
  - Components:           7

Infrastructure:
  - Config files:         6
  - Documentation:        5
```

---

## 🔍 Quick File Finder

### By Size (Largest files)
1. `frontend/src/components/EventTab.jsx` - 402 lines
2. `backend/tools/explainers.py` - 307 lines
3. `backend/database/mock_data.py` - 274 lines
4. `backend/tools/calculators.py` - 246 lines
5. `backend/api/main.py` - 238 lines

### By Importance (Most critical files)
1. `backend/agents/orchestrator.py` - Main workflow
2. `backend/api/main.py` - API endpoints
3. `backend/tools/calculators.py` - Risk scoring
4. `frontend/src/components/Dashboard.jsx` - UI entry
5. `docker-compose.yml` - Infrastructure

---

## 🌐 Online Code Viewing

You can view all code files on GitHub:

**Repository URL**: https://github.com/navya-glitch/marine-risk-ai

### Browse online:
- **Backend**: https://github.com/navya-glitch/marine-risk-ai/tree/main/backend
- **Frontend**: https://github.com/navya-glitch/marine-risk-ai/tree/main/frontend
- **All files**: https://github.com/navya-glitch/marine-risk-ai/tree/main

### Clone locally:
```bash
git clone https://github.com/navya-glitch/marine-risk-ai.git
cd marine-risk-ai
```

---

## 💡 Tips for Exploring the Code

1. **Start with documentation**: Read `README.md` first
2. **Understand the flow**: 
   - User Input → `InputForm.jsx`
   - API Call → `backend/api/main.py`
   - Orchestration → `backend/agents/orchestrator.py`
   - Risk Calculation → `backend/tools/calculators.py`
   - Display Results → React components
3. **Use your IDE**: Open in VS Code, PyCharm, or any editor with file tree
4. **Follow imports**: Python imports and React imports show dependencies
5. **Check the tests**: `backend/test_backend.py` shows how components work together

---

## 🚀 Next Steps

1. **Clone the repository** to your local machine
2. **Open in your IDE** (VS Code recommended)
3. **Start with** `README.md` for setup instructions
4. **Explore** using the file paths above
5. **Run the system** with `./start.sh` to see it in action

---

**Last Updated**: February 8, 2026  
**Total Code Files**: 46  
**All code is open source and available in the repository!**
