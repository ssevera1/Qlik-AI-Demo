# C4 Model — Level 2: Container Diagram

Shows the major containers (services/applications) within the Qlik Cloud AI/ML ecosystem.

```mermaid
graph TB
    subgraph "Users"
        USER[HR Analyst / Manager]
        ADMIN[Tenant Admin]
        EXT_AI[External AI Assistant<br/>Claude Desktop / Cursor]
    end

    subgraph "Qlik Cloud Platform"
        subgraph "Analytics Layer"
            QS[Qlik Sense<br/>---<br/>Interactive dashboards,<br/>sheets, visualizations<br/>---<br/>Web Browser]
            QA[Qlik Answers<br/>---<br/>Agentic conversational AI<br/>Structured + unstructured data<br/>---<br/>Side panel in Qlik Cloud]
            IA[Insight Advisor<br/>---<br/>NL search + chat analytics<br/>Augmented analytics<br/>---<br/>Legacy, replaced by Qlik Answers]
        end

        subgraph "AI/ML Engine"
            QP[Qlik Predict<br/>---<br/>AutoML platform<br/>Classification, Regression,<br/>Time Series<br/>---<br/>No-code ML]
            QAE[Qlik Analytics Engine<br/>---<br/>Associative engine<br/>Governed calculations<br/>---<br/>In-memory]
            DA[Discovery Agent<br/>---<br/>Anomaly monitoring<br/>Proactive insights<br/>---<br/>Planned]
        end

        subgraph "Integration Layer"
            AC[Analytic Connections<br/>---<br/>SSE-based connectors<br/>8 LLM providers<br/>---<br/>Chart expressions + load scripts]
            AA[Application Automations<br/>---<br/>No-code workflows<br/>OpenAI + API Key connectors<br/>---<br/>Qlik Automate]
            MCP[MCP Server<br/>---<br/>Model Context Protocol<br/>Engine + tool + agent access<br/>---<br/>GA Feb 2026]
        end

        subgraph "Data Foundation"
            DM[Data Model<br/>---<br/>QVD files, app data<br/>Employee datasets<br/>---<br/>Qlik Cloud storage]
            KB[Knowledge Bases<br/>---<br/>Vectorized document stores<br/>PDF, DOCX, HTML<br/>---<br/>RAG retrieval]
            DP[Data Products<br/>---<br/>Curated governed datasets<br/>Quality signals<br/>---<br/>Planned]
        end
    end

    subgraph "External Services"
        OAI[OpenAI API]
        BED[Amazon Bedrock<br/>Claude, Titan, Llama]
        HF[Hugging Face API]
        HRIS[HRIS Data Source]
    end

    USER -->|Browse| QS
    USER -->|Ask questions| QA
    ADMIN -->|Configure| QS
    EXT_AI -->|MCP protocol| MCP

    QA --> QAE
    QA --> KB
    QS --> AC
    QS --> AA
    QP --> DM
    QAE --> DM

    AC --> OAI
    AC --> BED
    AC --> HF
    AA --> OAI
    MCP --> QAE

    HRIS --> DM
```

## Container Responsibilities

| Container | Technology | Responsibility |
|-----------|-----------|---------------|
| Qlik Sense | Web application | Interactive dashboards, visualizations, user interaction |
| Qlik Answers | Agentic AI service | Conversational analytics combining structured + unstructured data |
| Qlik Predict | AutoML platform | Model training, evaluation, deployment, predictions |
| Qlik Analytics Engine | In-memory engine | Governed calculations, associative data model |
| Discovery Agent | AI monitoring service | Continuous anomaly detection and proactive alerting |
| Analytic Connections | SSE connectors | Bridge between Qlik expressions and external LLMs |
| Application Automations | Workflow engine | No-code automation with external service integration |
| MCP Server | Protocol server | Exposes Qlik to third-party AI assistants |
| Knowledge Bases | Vector store | Document indexing and RAG retrieval |
| Data Products | Governed datasets | Curated data with quality signals |

## Data Flows

| Flow | Source | Target | Protocol | Latency |
|------|--------|--------|----------|---------|
| User query | Browser | Qlik Answers | HTTPS | <2s (target) |
| Analytical calculation | Qlik Answers | Analytics Engine | Internal | <500ms |
| Document retrieval | Qlik Answers | Knowledge Base | Internal | <1s |
| LLM chart expression | Analytics Connection | OpenAI/Bedrock | REST API | 2-10s |
| Automation workflow | Qlik Automate | External APIs | REST API | Variable |
| MCP request | External AI | MCP Server | MCP/HTTPS | 1-5s |
| Batch prediction | Qlik Predict | Data Model | Internal | Minutes |
| Real-time prediction | API client | Qlik Predict | REST API | <1s |
