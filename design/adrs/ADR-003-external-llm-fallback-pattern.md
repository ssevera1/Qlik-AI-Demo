# ADR-003: External LLM Integration as Fallback When Qlik Answers Is Insufficient

## Status
Accepted

## Context
Qlik Answers provides structured data analytics via the Qlik Analytics Engine and unstructured
document Q&A via RAG. However, certain use cases require capabilities beyond what Qlik Answers
offers natively:

- Free-form narrative generation (personalized retention recommendations)
- Custom sentiment analysis on employee feedback text
- Cross-domain reasoning combining Qlik data with general knowledge
- Fine-tuned model access for domain-specific predictions
- Dynamic code/expression generation

## Decision
Implement a **tiered fallback architecture** using Qlik's native integration mechanisms:

1. **Analytic Connections** (chart expressions) — for real-time, selection-driven LLM responses inline in dashboards
2. **Application Automations** (button-triggered workflows) — for multi-step workflows, write-back, and cross-platform integration
3. **Qlik MCP Server** — for exposing Qlik data to external AI assistants

## Rationale
- **Native integration**: All three mechanisms are built into Qlik Cloud — no custom infrastructure required
- **Cost control**: Analytic connections use `if(count(distinct [Field]) = 1, ...)` gating to prevent runaway API costs
- **Separation of concerns**: Display needs (analytic connections) vs. workflow needs (automations) vs. external access (MCP)
- **Provider flexibility**: API Key connector supports any REST API — not locked into a single LLM provider
- **Governance preserved**: All data access still goes through Qlik's permission model

## Trade-offs Accepted
- **API costs**: External LLM calls incur per-token costs — must be managed via selection gating and caching
- **Latency**: LLM responses take 2-10 seconds — not suitable for high-frequency calculations
- **Rate limits**: 25 rows max per analytic connection request; 300 req/min for Qlik Predict API
- **Complexity**: Three integration patterns increase architectural complexity — team must understand when to use each
- **Text & Image only**: Analytic connection LLM responses can only display in Text & Image objects, not in tables or other chart types

## Alternatives Considered
- **Custom SSE plugin (on-premises only)**: Maximum flexibility but requires Python microservice infrastructure and is not available in Qlik Cloud
- **Qlik Open Lakehouse + custom ML**: Pre-compute all AI insights at data load time — eliminates real-time LLM calls but loses interactivity
- **Embedded iframe with external app**: Build a separate AI chat interface and embed via iframe — breaks the native Qlik experience

## Consequences
- Application documents all three fallback patterns with code examples and architecture diagrams
- HR-specific examples show how to combine Qlik Predict scores with LLM-generated narratives
- Cost control patterns (selection gating, QVD caching) are documented as best practices
- Amazon Bedrock Converse API recommended as the unified connector for multi-model access
