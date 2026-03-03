# C4 Model — Level 1: System Context Diagram

Shows how the Qlik Cloud AI/ML ecosystem interacts with external actors and systems.

```mermaid
graph TB
    subgraph "People Analytics Team"
        HRA[HR Analyst<br/>Uses Qlik Sense dashboards<br/>for flight risk, promotions, workforce planning]
        HRM[HR Manager<br/>Reviews AI-generated insights<br/>and acts on retention recommendations]
        TA[Tenant Admin<br/>Configures AI features,<br/>permissions, cross-region processing]
    end

    subgraph "Qlik Cloud Platform"
        QC[Qlik Cloud<br/>Analytics + AI/ML Platform<br/>---<br/>Qlik Answers, Qlik Predict,<br/>Automations, MCP Server]
    end

    subgraph "External Systems"
        HRIS[HRIS / HCM<br/>Workday, SAP SuccessFactors<br/>Employee data source]
        LLM[External LLM Providers<br/>OpenAI, Anthropic Claude,<br/>Hugging Face, Amazon Bedrock]
        COLLAB[Collaboration Tools<br/>Slack, Microsoft Teams,<br/>Email, ServiceNow]
        AI_ASST[Third-Party AI Assistants<br/>Claude Desktop, Cursor,<br/>ChatGPT via MCP]
    end

    HRA -->|Explores data, asks questions| QC
    HRM -->|Reviews dashboards & alerts| QC
    TA -->|Configures & governs| QC
    QC -->|Loads employee data| HRIS
    QC -->|Calls LLM APIs for<br/>chart expressions & automations| LLM
    QC -->|Sends alerts &<br/>automation outputs| COLLAB
    AI_ASST -->|Connects via MCP protocol| QC
```

## Key Relationships

| Actor/System | Interaction | Protocol |
|-------------|-------------|----------|
| HR Analyst | Explores Qlik Sense apps, asks Qlik Answers questions | HTTPS (browser) |
| HR Manager | Reviews dashboards, receives alerts | HTTPS, email, Slack |
| Tenant Admin | Configures cross-region processing, permissions, roles | Admin Console |
| HRIS | Source of employee data (CDC or batch) | REST API, ODBC, connectors |
| External LLMs | Called by analytic connections and automations | REST API |
| Collaboration Tools | Receive automation outputs (alerts, reports) | REST API, webhooks |
| Third-Party AI Assistants | Access Qlik via MCP Server | MCP protocol |
