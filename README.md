# Qlik Cloud AI/ML Capabilities

A comprehensive reference application documenting Qlik Cloud's AI and ML features, built for people analytics teams evaluating Qlik Answers, Qlik Predict, and external LLM integration patterns.

**Qlik Cloud only** — no Qlik Sense on-premises content.

---

## Quick Start

### Windows

Double-click `run.bat` or run from terminal:

```
run.bat
```

### macOS / Linux

```bash
chmod +x run.sh
./run.sh
```

### Manual

```bash
pip install -r requirements.txt
streamlit run app.py --server.address 127.0.0.1 --server.headless true
```

The app opens at [http://localhost:8501](http://localhost:8501).

---

## What's Inside

### Part 1: Qlik Answers (Structured Data)

- Latest agentic analytics capability (GA Feb 2026)
- Structured + unstructured data via Qlik Analytics Engine and RAG
- Full admin requirements: cross-region processing, permissions, space access, regional availability, operational limits
- Comparison tables: new agentic version vs. previous unstructured-only version
- Comparison tables: Qlik Answers vs. Insight Advisor (and supersession details)

### Part 2: Qlik Predict (ML)

- End-to-end AutoML workflow with architecture diagrams
- All 17 algorithms: 8 classification, 6 regression, 3 deep learning time series
- HR use cases: employee turnover, promotion prediction, lateral movement
- 14 additional people analytics use cases (flight risk scoring, absenteeism, engagement forecasting, compensation equity, workforce demand, succession planning, and more)

### Part 3: Application Automations & External LLM Integration

- Qlik Automate overview (triggers, blocks, connectors)
- Three LLM integration methods: native OpenAI connector, API Key connector (any LLM), 8 analytic connections
- Dynamic selection-driven LLM responses via SSE protocol
- Fallback architecture with decision flow when Qlik Answers is insufficient
- Code examples for chart expressions and automation workflows

### Part 4: Qlik Cloud AI/ML Ecosystem

- 12+ current GA features with details
- Data quality features (Trust Score for AI, Knowledge Mart, AI stewardship)
- Development tools (NL expression generator, AI script generation, Table Recipe, Open Lakehouse)
- Full timeline of 17+ features with availability dates
- Strategic partnerships (AWS competencies, Gartner leadership)
- AI governance framework
- Qlik Staige platform architecture

---

## Optional Logo

Place a `logo.png` in the `logo/` directory and it will display at the top of every page. If no file is present, nothing is shown.

```
logo/
  logo.png
```

---

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher
├── run.sh                  # macOS/Linux launcher
├── .streamlit/
│   └── config.toml         # Streamlit config (theme, telemetry off, localhost)
├── logo/                   # Optional logo directory (add logo.png)
├── design/
│   ├── diagrams/           # C4 architecture diagrams (Mermaid)
│   │   ├── c4-context.md   # Level 1: System Context
│   │   ├── c4-container.md # Level 2: Containers
│   │   ├── c4-component.md # Level 3: Components
│   │   └── c4-code.md      # Level 4: Code-level patterns
│   └── adrs/               # Architecture Decision Records
│       ├── ADR-001-streamlit-for-demo-app.md
│       ├── ADR-002-qlik-answers-over-insight-advisor.md
│       ├── ADR-003-external-llm-fallback-pattern.md
│       ├── ADR-004-qlik-predict-for-hr-analytics.md
│       └── ADR-005-mermaid-for-architecture-diagrams.md
└── assets/
    ├── images/             # Screenshots and visual assets
    └── diagrams/           # Exported diagram images
```

---

## Privacy & Security

- **Localhost only** — bound to `127.0.0.1`, not discoverable on LAN
- **Zero telemetry** — Streamlit usage stats disabled via config and environment variable
- **No outbound connections** — the app makes no network calls at runtime
- **No external CDNs** — Mermaid.js is bundled locally in the `streamlit-mermaid` package
- **Only dependency** — `streamlit` (no HTTP client libraries, no analytics SDKs)
- URLs in the app are rendered as clickable links; they are only fetched if a user deliberately clicks them

---

## Requirements

- Python 3.9+
- Dependencies listed in `requirements.txt`:
  - `streamlit>=1.30.0`
  - `streamlit-mermaid>=0.3.0`

---

## Sources

All content is sourced from official Qlik documentation and press releases:

- [Qlik Cloud Help](https://help.qlik.com/en-US/cloud-services/)
- [Qlik Developer Portal](https://qlik.dev/)
- [Qlik Community](https://community.qlik.com/)
- [Qlik Press Room](https://www.qlik.com/us/news/company/press-room/)
- [Qlik Answers Product Page](https://www.qlik.com/us/products/qlik-answers)
- [Qlik Predict Documentation](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/home-automl.htm)
- [Qlik Automate Product Page](https://www.qlik.com/us/products/qlik-automate)
