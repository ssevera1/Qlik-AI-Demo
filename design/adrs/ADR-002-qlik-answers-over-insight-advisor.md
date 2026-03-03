# ADR-002: Recommend Qlik Answers (Agentic) Over Insight Advisor for New Deployments

## Status
Accepted

## Context
Qlik Cloud now offers two overlapping AI-powered analytics interfaces:
1. **Insight Advisor** — The established NL search and chat analytics tool with full business logic support
2. **Qlik Answers (Agentic)** — The new unified conversational interface combining structured and unstructured data with multi-step agentic reasoning (GA Feb 2026)

Enabling Qlik Answers is a **tenant-wide change** that hides Insight Advisor. Organizations must choose one path.

## Decision
Recommend **Qlik Answers (Agentic)** for new deployments and provide a migration path guide for existing Insight Advisor users.

## Rationale
- **Official direction**: Qlik's official stance is that Qlik Answers replaces Insight Advisor
- **Superior capabilities**: Agentic framework, multi-step reasoning, combined structured + unstructured data, MCP server integration
- **Future investment**: All new AI features (Discovery Agent, Data Products, Productivity Agents) are built on the Qlik Answers foundation
- **Embeddable**: Full embeddable agentic experiences for external applications
- **Ecosystem integration**: MCP Server enables third-party AI assistants (Claude, ChatGPT)

## Trade-offs Accepted
- **Loss of business logic features**: Packages, Hierarchies, Behaviors, and Calendar periods tabs are removed; only Synonyms retained
- **Cross-region data processing required**: Data must temporarily leave tenant region for processing — regulatory concern for some organizations
- **Migration complexity**: Existing analyses relying on hidden business logic tabs cannot be modified post-migration
- **Regional limitations**: Europe (London) only supports the legacy experience
- **Cannot run both simultaneously**: Tenant-wide switch — no gradual migration per-app

## Consequences
- Application documents both systems with clear migration guidance
- Requirements section prominently highlights the cross-region processing prerequisite
- Fallback architecture (Part 3) provides external LLM integration for gaps in Qlik Answers capabilities
- Organizations in regulated industries should evaluate cross-region processing implications before enabling
