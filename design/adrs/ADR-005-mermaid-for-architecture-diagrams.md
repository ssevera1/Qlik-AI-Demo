# ADR-005: Chosen Mermaid.js for Architecture Diagrams Over Excalidraw

## Status
Accepted

## Context
The design documentation requires clear, editable diagrams that map data flows, latency
requirements, and component interactions across the Qlik Cloud AI/ML ecosystem.

**Options considered:**
1. **Mermaid.js** — Text-based diagramming language rendered in Markdown
2. **Excalidraw** — Hand-drawn style visual diagramming tool
3. **draw.io / diagrams.net** — GUI-based diagramming with XML storage
4. **PlantUML** — Text-based UML diagramming

## Decision
Chosen **Mermaid.js** for all C4 model diagrams and architecture documentation.

## Rationale
- **Version control friendly**: Diagrams are plain text — diffs are meaningful in Git
- **Markdown native**: Renders directly in GitHub, GitLab, Notion, and most documentation platforms
- **Streamlit compatible**: Can be rendered via `streamlit-mermaid` package or displayed as code blocks
- **C4 model support**: Mermaid supports `graph`, `sequenceDiagram`, `classDiagram`, and `flowchart` — sufficient for all C4 levels
- **No external tooling**: No need for separate diagram editor — authors edit text alongside code
- **Wide ecosystem**: Supported by VS Code, JetBrains, GitHub, Obsidian, and most modern development tools

## Trade-offs Accepted
- **Visual fidelity**: Mermaid diagrams are less visually polished than Excalidraw or draw.io — acceptable for technical documentation
- **Layout control**: Limited control over node positioning compared to GUI tools — Mermaid's auto-layout is "good enough" for most diagrams
- **Complex diagrams**: Very large diagrams with many nodes can become hard to read in text form — mitigated by splitting into multiple focused diagrams (one per C4 level)
- **No hand-drawn aesthetic**: Unlike Excalidraw, Mermaid produces clean geometric shapes — this is appropriate for technical architecture docs

## Consequences
- All diagrams stored as `.md` files in `design/diagrams/`
- C4 levels split across four files: `c4-context.md`, `c4-container.md`, `c4-component.md`, `c4-code.md`
- Diagrams are embedded in the Streamlit app as code blocks (rendered by Mermaid-compatible viewers)
- ADRs reference diagrams by file path
