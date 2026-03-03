# ADR-001: Chosen Streamlit for Demo Application Framework

## Status
Accepted

## Context
We needed a Python-based framework to build a comprehensive reference application documenting
Qlik Cloud's AI/ML capabilities. The application must support rich content (tables, diagrams,
code examples), interactive navigation, and be easy to deploy and maintain.

**Options considered:**
1. **Streamlit** — Python-native web framework for data apps
2. **Dash (Plotly)** — Python framework for analytical web applications
3. **Flask + Jinja2** — General-purpose Python web framework with templates
4. **Static site generator (MkDocs/Sphinx)** — Documentation-focused tools

## Decision
Chosen **Streamlit** as the application framework.

## Rationale
- **Python-native**: Entire app is a single Python file — no HTML/CSS/JS required for core functionality
- **Rich components**: Built-in support for tables, tabs, expanders, columns, code blocks, and markdown
- **Fast iteration**: Hot-reload during development; changes reflected immediately
- **Qlik ecosystem alignment**: Streamlit is commonly used in the data analytics community, aligning with the target audience (people analytics teams)
- **Low maintenance**: Single `app.py` file with no complex build pipeline
- **Deployment flexibility**: Can be deployed on Streamlit Cloud, Docker, or any Python environment

## Trade-offs Accepted
- **Limited customization**: Streamlit's component model is less flexible than Dash or custom Flask apps
- **No server-side state persistence**: Session state resets on page refresh (acceptable for a reference app)
- **Mermaid diagram rendering**: Requires `streamlit-mermaid` package or falls back to code blocks (acceptable trade-off vs. pre-rendered images)

## Consequences
- All content is authored in Python using Streamlit API calls
- Navigation uses sidebar radio buttons with section/subsection pattern
- Custom CSS injected via `st.markdown()` for styling executive summaries and cards
- Diagrams rendered as Mermaid code blocks (viewable in Mermaid-compatible viewers)
