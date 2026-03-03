"""
Qlik Cloud AI/ML Capabilities Demo Application
================================================
A comprehensive Streamlit application documenting Qlik Cloud's AI and ML
features including Qlik Answers (structured data), Qlik Predict, Application
Automations with external LLM integration, and the broader AI ecosystem.

All content is Qlik Cloud (SaaS) focused — no Qlik Sense on-premises content.
"""

import streamlit as st
from streamlit_mermaid import st_mermaid

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Qlik Cloud AI/ML Capabilities",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .exec-summary {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e0e0;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #00c853;
        margin-bottom: 1.5rem;
    }
    .exec-summary h3 { color: #00e676; margin-top: 0; }
    .exec-summary li { margin-bottom: 0.4rem; }
    .comparison-better { color: #00c853; font-weight: bold; }
    .comparison-worse { color: #ff5252; font-weight: bold; }
    .section-divider {
        border: 0;
        height: 3px;
        background: linear-gradient(to right, #00c853, #0f3460, #00c853);
        margin: 2rem 0;
    }
    .req-box {
        background: #1e1e2f;
        color: #e0e0e0;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #333;
        margin-bottom: 0.75rem;
    }
    .demo-placeholder {
        background: #f0f2f6;
        border: 2px dashed #aaa;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        color: #666;
        margin: 1rem 0;
    }
    .architecture-box {
        background: #0d1117;
        color: #c9d1d9;
        padding: 1.2rem;
        border-radius: 8px;
        font-family: monospace;
        white-space: pre;
        overflow-x: auto;
        margin: 1rem 0;
        border: 1px solid #30363d;
    }
    .use-case-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #0f3460;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to Section",
    [
        "Home",
        "Part 1: Qlik Answers (Structured Data)",
        "Part 2: Qlik Predict (ML)",
        "Part 3: Application Automations & LLM",
        "Part 4: Qlik Cloud AI/ML Ecosystem",
    ],
)

# Sub-navigation
if section == "Part 1: Qlik Answers (Structured Data)":
    subsection = st.sidebar.radio(
        "Sub-section",
        [
            "1.1 Executive Summary",
            "1.2 Latest Capability: Structured Data",
            "1.3 Requirements & Permissions",
            "1.4 Comparison: Structured vs Unstructured",
            "1.5 Comparison: Qlik Answers vs Insight Advisor",
            "1.6 Demo",
        ],
    )
elif section == "Part 2: Qlik Predict (ML)":
    subsection = st.sidebar.radio(
        "Sub-section",
        [
            "2.1 Executive Summary",
            "2.2 How Qlik Predict Works",
            "2.3 ML Algorithms & Models",
            "2.4 HR Use Cases",
            "2.5 People Analytics Ideation",
            "2.6 Demo",
        ],
    )
elif section == "Part 3: Application Automations & LLM":
    subsection = st.sidebar.radio(
        "Sub-section",
        [
            "3.1 Executive Summary",
            "3.2 Application Automations Overview",
            "3.3 Integrating External LLMs",
            "3.4 Analytic Connections (Dynamic Updates)",
            "3.5 Fallback Architecture",
            "3.6 Demo",
        ],
    )
elif section == "Part 4: Qlik Cloud AI/ML Ecosystem":
    subsection = st.sidebar.radio(
        "Sub-section",
        [
            "4.1 Executive Summary",
            "4.2 Current AI/ML Features",
            "4.3 Planned / Upcoming Features",
            "4.4 Qlik Staige Platform",
        ],
    )
else:
    subsection = None


# =========================================================================
#  HELPER: render executive summary
# =========================================================================
def exec_summary(title: str, bullets: list[str]):
    items = "".join(f"<li>{b}</li>" for b in bullets)
    st.markdown(
        f'<div class="exec-summary"><h3>{title}</h3><ul>{items}</ul></div>',
        unsafe_allow_html=True,
    )


def section_divider():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


def demo_placeholder(label: str, link: str = ""):
    link_html = f'<br><a href="{link}" target="_blank">Watch Official Demo &rarr;</a>' if link else ""
    st.markdown(
        f'<div class="demo-placeholder"><strong>{label}</strong><br>'
        f'Screenshots and animated GIFs would be embedded here from live Qlik Cloud environment.'
        f'{link_html}</div>',
        unsafe_allow_html=True,
    )


def mermaid_diagram(code: str):
    """Render a Mermaid diagram using the bundled streamlit-mermaid component."""
    st_mermaid(code, height="auto")


# =========================================================================
#  HOME
# =========================================================================
if section == "Home":
    st.title("Qlik Cloud AI/ML Capabilities")
    st.subheader("A Comprehensive Reference for People Analytics Teams")

    exec_summary("Application Overview", [
        "Covers <b>Qlik Answers</b> (agentic analytics with structured + unstructured data) — GA Feb 2026",
        "Documents <b>Qlik Predict</b> (AutoML) with HR-specific use cases for turnover, promotions, and lateral moves",
        "Explains <b>Application Automations</b> for integrating external LLMs (OpenAI, Claude, etc.) into Qlik apps",
        "Maps the full <b>Qlik Cloud AI/ML ecosystem</b> including planned features like Discovery Agent and MCP Server",
        "All content is <b>Qlik Cloud only</b> — no on-premises Qlik Sense Enterprise content",
    ])

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Quick Links")
        st.markdown("""
        - [Qlik Answers Product Page](https://www.qlik.com/us/products/qlik-answers)
        - [Qlik Predict Documentation](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/home-automl.htm)
        - [Qlik Automate Product Page](https://www.qlik.com/us/products/qlik-automate)
        - [Qlik Cloud Help](https://help.qlik.com/en-US/cloud-services/)
        - [Qlik Developer Portal](https://qlik.dev/)
        """)
    with col2:
        st.markdown("### Timeline of Key Announcements")
        st.markdown("""
        | Date | Milestone |
        |------|-----------|
        | 2024 | Qlik Answers launched (unstructured data only) |
        | May 2025 | Agentic analytics vision announced at Qlik Connect |
        | Oct 2025 | Multivariate Time Series GA in Qlik Predict |
        | Dec 2025 | Agentic Qlik Answers private preview |
        | Feb 2026 | Qlik Answers agentic GA + MCP Server GA |
        """)

    section_divider()

    st.markdown("### Architecture Overview")
    mermaid_diagram("""graph TB
    subgraph "Qlik Cloud Platform"
        QA[Qlik Answers<br/>Agentic Analytics]
        QP[Qlik Predict<br/>AutoML]
        AA[Application Automations<br/>Qlik Automate]
        AC[Analytic Connections<br/>SSE Connectors]
        MCP[MCP Server<br/>Third-Party AI]
        DA[Discovery Agent<br/>Anomaly Detection]
    end

    subgraph "Data Sources"
        SD[Structured Data<br/>Qlik Apps]
        UD[Unstructured Data<br/>PDFs, DOCX, HTML]
        EXT[External APIs<br/>HRIS, ERP]
    end

    subgraph "External AI/LLMs"
        OAI[OpenAI GPT]
        CL[Anthropic Claude]
        HF[Hugging Face]
        BED[Amazon Bedrock]
    end

    SD --> QA
    UD --> QA
    SD --> QP
    EXT --> AA
    AA --> OAI
    AA --> CL
    AC --> OAI
    AC --> CL
    AC --> HF
    AC --> BED
    MCP --> CL
    QA --> DA""")


# =========================================================================
#  PART 1: QLIK ANSWERS (STRUCTURED DATA)
# =========================================================================
elif section == "Part 1: Qlik Answers (Structured Data)":

    st.title("Part 1: Qlik Answers — Agentic Analytics with Structured Data")

    # ----- 1.1 Executive Summary -----
    if subsection == "1.1 Executive Summary":
        exec_summary("Executive Summary — Qlik Answers Structured Data", [
            "<b>What:</b> Qlik Answers now supports <b>structured data</b> from Qlik analytic applications alongside unstructured documents (PDFs, DOCX, HTML), powered by an agentic AI framework and the Qlik Analytics Engine.",
            "<b>When:</b> General Availability as of <b>February 10, 2026</b>. Private preview began December 2025.",
            "<b>Impact:</b> Qlik Answers <b>replaces Insight Advisor and Insight Advisor Chat</b> in enabled tenants — this is a tenant-wide change.",
            "<b>Key Requirement:</b> Tenant admins must <b>opt in to cross-region data processing</b> to enable the agentic experience.",
            "<b>New Capabilities:</b> Multi-step agentic reasoning, visual + narrative responses, MCP Server for third-party AI assistants (Claude, ChatGPT), Discovery Agent for anomaly detection.",
        ])

        st.info("""
        **Sources:**
        - [Qlik GA Press Release (Feb 2026)](https://www.businesswire.com/news/home/20260210837577/en/Qlik-Brings-Agentic-Analytics-to-General-Availability-and-Launches-MCP-Server-for-Third-Party-Assistants)
        - [Qlik Answers — Qlik Cloud Help](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/Qlik-Answers.htm)
        - [Qlik Agentic AI Vision Blog](https://www.qlik.com/blog/a-vision-for-the-future-qliks-new-agentic-ai-experience)
        """)

    # ----- 1.2 Latest Capability -----
    elif subsection == "1.2 Latest Capability: Structured Data":
        st.header("Latest Capability: Structured Data in Qlik Answers")

        st.markdown("""
        ### What Changed

        Qlik Answers evolved from a **document-only Q&A chatbot** (2024) into a full **agentic analytics platform**
        that works across both structured application data and unstructured documents.

        The agentic experience is delivered through **Qlik Answers** as the unified conversational interface,
        powered by:

        - **Qlik Analytics Engine** — performs governed, context-preserving calculations on structured app data
        - **Specialized AI Agents** — handle multi-step reasoning, planning, and orchestration
        - **RAG (Retrieval Augmented Generation)** — retrieves relevant passages from curated knowledge bases
        - **LLM Reasoning** — synthesizes insights into rich narrative and visual responses with citations
        """)

        st.markdown("### Key Components")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            #### Qlik Answers (Core)
            - Unified conversational interface
            - Structured + unstructured data
            - Always-on side panel
            - Citations and reasoning explanations
            - Embeddable in external apps
            """)
        with col2:
            st.markdown("""
            #### Discovery Agent
            - Continuously monitors key measures
            - Surfaces anomalies and shifts
            - Proactive alerting
            - Planned rollout shortly after GA
            """)
        with col3:
            st.markdown("""
            #### MCP Server
            - Exposes Qlik at engine, tool, and agent levels
            - Third-party AI assistants (Claude, ChatGPT)
            - Secure access to governed data
            - Generally available Feb 2026
            """)

        section_divider()

        st.markdown("### How Structured Data Works in Qlik Answers")
        mermaid_diagram("""sequenceDiagram
    participant User
    participant QA as Qlik Answers
    participant Agent as AI Agent
    participant QAE as Qlik Analytics Engine
    participant KB as Knowledge Base (RAG)
    participant LLM as LLM

    User->>QA: Ask analytical question
    QA->>Agent: Route to appropriate agent
    Agent->>QAE: Execute calculations on app data
    QAE-->>Agent: Structured results
    Agent->>KB: Retrieve relevant documents
    KB-->>Agent: Document passages + citations
    Agent->>LLM: Synthesize structured + unstructured
    LLM-->>Agent: Rich narrative + reasoning
    Agent-->>QA: Response with visuals + citations
    QA-->>User: Display narrative, charts, sheets""")

        st.markdown("""
        ### Structured Data Preparation

        To use structured data with Qlik Answers, application owners must:

        1. **Prepare the Qlik Sense app** — ensure the data model is clean, with proper field names and associations
        2. **Add the app as a data source** in the Qlik Answers assistant configuration
        3. **Combine with knowledge bases** (optional) — adding unstructured documents provides richer context
        4. **Define synonyms** — the Synonyms vocabulary tab remains available to help Qlik Answers interpret field names

        > **Note:** Business logic features like Packages, Hierarchies, Behaviors, and Calendar periods are
        > **not available** in the agentic experience (these were Insight Advisor features).
        """)

    # ----- 1.3 Requirements & Permissions -----
    elif subsection == "1.3 Requirements & Permissions":
        st.header("Requirements & Permissions for Tenant Administrators")

        st.error("""
        **Critical:** Enabling Qlik Answers agentic experience is a **tenant-wide change** that replaces
        Insight Advisor and Insight Advisor Chat. This cannot be done per-app or per-user — it affects
        the entire tenant.
        """)

        st.markdown("### Step 1: Enable Cross-Region Data Processing")
        st.markdown("""
        <div class="req-box">
        <b>Path:</b> Administration activity center → Settings → Tenant → AI features in Qlik<br><br>
        <b>Action:</b> Toggle <b>"Enable cross-region data processing"</b> to ON<br><br>
        <b>Confirmation:</b> Check the authorization checkbox confirming you are authorized, then click <b>Confirm → Submit</b><br><br>
        <b>What it does:</b> Allows Qlik Cloud to temporarily send data to AWS regions where AI processing
        services are hosted (currently AWS US East). Data is processed and results returned — data is not stored
        in the remote region.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Step 2: Configure Permissions")
        st.markdown("""
        <div class="req-box">
        <b>Path:</b> Administration → Manage users → Permissions → Custom roles<br><br>
        Once cross-region processing is enabled, these permissions default to <b>"Not allowed"</b>
        and must be explicitly granted:
        </div>
        """, unsafe_allow_html=True)

        perm_data = {
            "Permission": [
                "Data analysis",
                "Qlik product help",
                "Qlik MCP server access",
                "Manage assistants",
                "Manage knowledge bases",
                "Index knowledge bases",
                "Search knowledge bases",
            ],
            "Description": [
                "Analyze data with Qlik Answers (core analytics capability)",
                "Access documentation via Qlik Answers",
                "Allow third-party AI assistants to connect via MCP",
                "Create and manage Qlik Answers assistants",
                "Create, manage, index, and search knowledge bases",
                "Trigger indexing of knowledge bases",
                "Access knowledge bases when asking questions",
            ],
            "Default": [
                "Not allowed",
                "Not allowed",
                "Not allowed",
                "Not allowed",
                "Not allowed",
                "Not allowed",
                "Not allowed",
            ],
            "Category": [
                "Tenant-level",
                "Tenant-level",
                "Tenant-level",
                "Custom Role",
                "Custom Role",
                "Custom Role",
                "Custom Role",
            ],
        }
        st.table(perm_data)

        st.markdown("### Step 3: Configure Space-Level Access")
        st.markdown("Users need minimum space access across these areas:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            #### Shared Spaces
            | Space | Required Permissions |
            |-------|---------------------|
            | Assistant space | Can view + Can consume data |
            | Knowledge base space | Can consume data |
            | Data source spaces | Can consume data |
            """)
        with col2:
            st.markdown("""
            #### Managed Spaces
            | Space | Required Permissions |
            |-------|---------------------|
            | Assistant space | Has restricted view + Can consume data |
            | Knowledge base space | Has restricted view + Can consume data |
            | Data source spaces | Can consume data |
            """)

        section_divider()

        st.markdown("### Step 4: Prerequisite — Disable Legacy Data Analysis")
        st.warning("""
        **Before enabling cross-region processing**, ensure the **"Data analysis"** permission
        (under Insight Advisor) is set to **"Not allowed"** in User Default settings and any custom
        roles that contain this permission.
        """)

        st.markdown("### Regional Availability")
        regions = {
            "Region": [
                "US East (N. Virginia)",
                "Europe (Frankfurt)",
                "Europe (Ireland)",
                "Asia Pacific (Mumbai)",
                "Asia Pacific (Singapore)",
                "Asia Pacific (Sydney)",
                "Asia Pacific (Tokyo)",
                "Europe (London)",
            ],
            "Agentic Experience": ["Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No (legacy only)"],
        }
        st.table(regions)

        st.markdown("### Operational Limits")
        st.markdown("""
        | Limit | Value |
        |-------|-------|
        | Max file size | 50 MiB |
        | Concurrent documents per data source | 10 |
        | Searches per minute per subscription | 50 |
        | Assistant questions per minute | 20 |
        | Monthly question quota | Resets each month (does not carry over) |
        | Indexed page size | ~2,000 characters of text data |
        """)

        st.markdown("""
        **Sources:**
        - [Enabling Cross-Region Data Processing](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Admin/cross-region-data-processing.htm)
        - [Qlik Answers Access and Permissions](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/qlik-answers-permissions.htm)
        - [Deploying and Administering Qlik Answers](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/administering-qlik-answers.htm)
        """)

    # ----- 1.4 Comparison: Structured vs Unstructured -----
    elif subsection == "1.4 Comparison: Structured vs Unstructured":
        st.header("Comparison: Agentic (Structured + Unstructured) vs Previous Version (Unstructured Only)")

        comparison = {
            "Aspect": [
                "Data Sources",
                "Architecture",
                "Analytics Engine",
                "Output Format",
                "Reasoning",
                "Combined Insights",
                "Cross-Region Processing",
                "Trust & Transparency",
                "Context Awareness",
                "Embedding",
                "MCP Integration",
                "Business Logic",
            ],
            "Previous Qlik Answers (2024)": [
                "Unstructured only (PDF, DOCX, TXT, HTML)",
                "RAG (Retrieval Augmented Generation)",
                "None — document Q&A only",
                "Text-based answers with document citations",
                "Single-step document retrieval",
                "N/A (documents only)",
                "Optional (can stay in-region)",
                "Citations for document sources",
                "Standalone chat",
                "Basic",
                "Not available",
                "N/A",
            ],
            "Agentic Qlik Answers (Feb 2026)": [
                "Structured (Qlik apps) AND unstructured (documents)",
                "Agentic framework + RAG + Qlik Analytics Engine",
                "Full Qlik Analytics Engine calculations",
                "Rich narrative AND visual responses (sheets, charts)",
                "Multi-step agentic reasoning across data + documents",
                "Combines analytical insights with document context + LLM knowledge",
                "Required (must opt in)",
                "Citations + explanations of reasoning + governed calculations",
                "Always-on side panel with context awareness",
                "Embeddable agentic experiences for external apps",
                "Qlik MCP Server for third-party AI assistants",
                "Synonyms only (Packages, Hierarchies, Behaviors removed)",
            ],
        }
        st.table(comparison)

        section_divider()

        st.markdown("### Key Takeaways")
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            **Advantages of the New Agentic Version:**
            - Deep analytical capabilities via Qlik Analytics Engine
            - Multi-step reasoning instead of simple document retrieval
            - Visual + narrative responses
            - MCP opens Qlik to external AI ecosystem
            - Combined structured + unstructured insights
            """)
        with col2:
            st.warning("""
            **Trade-offs to Consider:**
            - Cross-region data processing is mandatory
            - Loss of some business logic features (Packages, Hierarchies, etc.)
            - Cannot run alongside Insight Advisor on same tenant
            - Requires careful migration planning for existing analyses
            """)

    # ----- 1.5 Comparison: vs Insight Advisor -----
    elif subsection == "1.5 Comparison: Qlik Answers vs Insight Advisor":
        st.header("Comparison: Qlik Answers (Agentic) vs Insight Advisor")

        st.error("""
        **Qlik Answers REPLACES Insight Advisor** in tenants where the agentic experience is enabled.
        Insight Advisor and Insight Advisor Chat options and settings are **hidden tenant-wide**.
        """)

        ia_comparison = {
            "Aspect": [
                "Scope",
                "Interface",
                "Analytics Approach",
                "AI Architecture",
                "Business Logic Support",
                "Data Sources",
                "Output",
                "MCP / External Access",
                "Contextual Side Panel",
                "Embedding",
                "Status",
            ],
            "Insight Advisor": [
                "Structured data within Qlik Sense apps only",
                "Search-based + chat-based within apps",
                "Generates suggested visualizations from NL queries",
                "Augmented analytics with some GenAI narrative",
                "Full: Packages, Hierarchies, Behaviors, Calendar periods, Vocabulary",
                "Only Qlik Sense app data models",
                "Visualizations and NL narratives within app context",
                "Not available",
                "No",
                "Limited",
                "Being replaced by Qlik Answers",
            ],
            "Qlik Answers (Agentic)": [
                "Structured app data AND unstructured documents",
                "Unified conversational agentic interface across platform",
                "Deep agentic multi-step exploration with sheets/charts/artifacts",
                "Full agentic framework with specialized agents + LLM + Qlik Engine",
                "Synonyms only (Packages, Hierarchies, Behaviors, Calendar periods removed)",
                "Qlik app data + knowledge bases of unstructured documents",
                "Rich narrative + visuals + citations + reasoning explanations",
                "MCP Server enables third-party AI assistants",
                "Yes — always-on side panel with context awareness",
                "Full embeddable agentic experiences",
                "Generally Available (Feb 2026)",
            ],
        }
        st.table(ia_comparison)

        section_divider()

        st.markdown("### Does Qlik Answers Supersede Insight Advisor?")

        st.markdown("""
        **Yes.** Based on Qlik's official documentation:

        > *"Qlik Answers replaces Insight Advisor and Insight Advisor Chat in tenants enabled
        > for Qlik Answers."*

        **Specifically:**
        - Insight Advisor and Insight Advisor Chat options are **hidden tenant-wide** for applications
        - Users are directed to **use Qlik Answers** to explore data and create sheets/charts
        - Certain **business logic tabs are removed** (Packages, Hierarchies, Behaviors, Calendar periods)
        - Once enabled, you **cannot edit configurations** in the hidden tabs
        - This is a **tenant-wide change** — cannot run both simultaneously

        **However, it is not a forced migration.** Tenants that do not opt in to cross-region data
        processing continue to have Insight Advisor. The legacy Qlik Answers experience (unstructured
        only, in-region) also remains available.
        """)

        st.warning("""
        **Migration Warning:** If you have existing analyses that rely on business logic settings
        (custom Behaviors, Hierarchies, Calendar periods), you will **not be able to modify** these
        after enabling Qlik Answers. Plan your migration carefully.
        """)

    # ----- 1.6 Demo -----
    elif subsection == "1.6 Demo":
        st.header("Demo: Qlik Answers Agentic Analytics")

        demo_placeholder(
            "Qlik Answers — Structured Data Q&A Demo",
            "https://www.qlik.com/us/products/qlik-answers"
        )

        st.markdown("### Demo Walkthrough")
        st.markdown("""
        1. **Open Qlik Answers** from the always-on side panel in Qlik Cloud
        2. **Ask a structured data question**: *"What were the top 5 departments by turnover rate last quarter?"*
        3. **Observe**: Qlik Answers routes to the AI agent, which queries the Qlik Analytics Engine
        4. **Review the response**: Narrative summary + auto-generated chart + citations
        5. **Follow up**: *"How does that compare to the same quarter last year?"* — multi-step reasoning
        6. **Combine data types**: *"What does our employee handbook say about retention programs?"* — switches to unstructured data via knowledge base
        """)

        demo_placeholder(
            "Qlik MCP Server — Claude Desktop Integration Demo",
            "https://community.qlik.com/t5/Integration-Extension-APIs/Qlik-Cloud-Development-with-Claude-Desktop-and-MCP-Servers-Video/td-p/2535891"
        )

        st.markdown("""
        **Official Resources:**
        - [Qlik Answers Product Page](https://www.qlik.com/us/products/qlik-answers)
        - [Qlik Agentic AI Experience Blog](https://www.qlik.com/blog/a-vision-for-the-future-qliks-new-agentic-ai-experience)
        - [Qlik MCP Community Video](https://community.qlik.com/t5/Integration-Extension-APIs/Qlik-Cloud-Development-with-Claude-Desktop-and-MCP-Servers-Video/td-p/2535891)
        """)


# =========================================================================
#  PART 2: QLIK PREDICT (ML)
# =========================================================================
elif section == "Part 2: Qlik Predict (ML)":

    st.title("Part 2: Qlik Predict — Automated Machine Learning")

    # ----- 2.1 Executive Summary -----
    if subsection == "2.1 Executive Summary":
        exec_summary("Executive Summary — Qlik Predict", [
            "<b>What:</b> Qlik Predict (formerly Qlik AutoML) is a <b>no-code automated machine learning</b> platform embedded in Qlik Cloud Analytics for building, training, and deploying predictive models.",
            "<b>Capabilities:</b> Binary/multiclass classification, regression, and <b>multivariate time series forecasting</b> (GA Oct 2025) with GPU-accelerated deep learning.",
            "<b>Explainability:</b> Built-in <b>SHAP-based explainability</b> shows which features drive predictions at both global and row levels.",
            "<b>Deployment:</b> Three methods — batch predictions, real-time API, and Qlik Predict analytics connector for in-app integration.",
            "<b>HR Applications:</b> Ideal for predicting employee turnover, promotions, lateral movements, absenteeism, compensation equity, and workforce demand forecasting.",
        ])

    # ----- 2.2 How Qlik Predict Works -----
    elif subsection == "2.2 How Qlik Predict Works":
        st.header("How Qlik Predict Works")

        st.markdown("### End-to-End Workflow")
        mermaid_diagram("""graph LR
    A[1. Data Loading<br/>CSV, QVD, XLSX] --> B[2. Experiment Creation<br/>Select target column]
    B --> C[3. Automated Training<br/>Multiple algorithms]
    C --> D[4. Model Evaluation<br/>SHAP explainability]
    D --> E[5. Deployment<br/>Model approval]
    E --> F[6. Predictions<br/>Batch / Real-time / Connector]
    F --> G[7. Visualization<br/>Qlik Sense dashboards]""")

        st.markdown("""
        ### Step-by-Step Process

        **1. Data Loading & Profiling**
        - Upload structured, tabular datasets (CSV, QVD, XLSX)
        - System automatically analyzes and preprocesses data
        - Displays statistics and insights about each column

        **2. Experiment Creation**
        - Select a target column (the outcome to predict)
        - Qlik Predict auto-detects the problem type:
          - **Binary classification** — target has 2 unique values
          - **Multiclass classification** — target has 3-10 string values
          - **Regression** — numerical target
          - **Time series** — temporal forecasting with covariates

        **3. Automated Model Training**
        - Multiple algorithms train simultaneously
        - Intelligent model optimization handles:
          - Feature selection (per model)
          - Feature transformations (Yeo-Johnson, binning)
          - Anomaly detection (down-weights outliers)
          - Class balancing (oversampling when imbalance > 95:5)
          - Gradual training data scaling

        **4. Model Evaluation & Scoring**
        - Models ranked by performance metrics
        - SHAP-based explainability charts generated
        - Feature importance visualization

        **5. Deployment**
        - Deploy best model to ML deployment environment
        - Model approval step for governance
        - Model versioning and swapping supported

        **6. Prediction & Visualization**
        - Generate batch predictions on new data
        - Real-time predictions via API (300 req/min)
        - Qlik Predict analytics connector (200K rows/request)
        - Load results into Qlik Sense apps for interactive dashboards
        """)

        st.markdown("### Deployment Architecture")
        mermaid_diagram("""graph TB
    subgraph "Qlik Cloud"
        EXP[Experiment<br/>Train Models] --> DEP[ML Deployment<br/>Approved Model]
        DEP --> BATCH[Batch Predictions<br/>Scheduled / Manual]
        DEP --> RT[Real-Time API<br/>REST Endpoint]
        DEP --> CON[Analytics Connector<br/>In-App Load Script]
    end

    BATCH --> QS[Qlik Sense App<br/>Dashboard]
    RT --> QS
    CON --> QS
    RT --> EXT[External Applications<br/>Custom Integrations]

    subgraph "Automation"
        QS --> AUTO[Qlik Automate<br/>Trigger Actions]
        AUTO --> ALERT[Alerts & Notifications]
        AUTO --> WB[Write-Back to Sources]
    end""")

        st.markdown("""
        **Key Constraints:**
        - Max 500 columns per dataset
        - API rate limit: 300 requests/minute
        - Analytics connector: 200,000 rows per request (batched in 2,000 row chunks)
        - Not available on Qlik Cloud Government
        - Available in Premium and Enterprise tiers
        """)

    # ----- 2.3 ML Algorithms -----
    elif subsection == "2.3 ML Algorithms & Models":
        st.header("ML Algorithms & Models")

        tab1, tab2, tab3 = st.tabs(["Classification", "Regression", "Time Series"])

        with tab1:
            st.markdown("### Classification Algorithms (Binary & Multiclass)")
            class_data = {
                "Algorithm": [
                    "Logistic Regression",
                    "Lasso Regression",
                    "Elastic Net Regression",
                    "Gaussian Naive Bayes",
                    "Random Forest",
                    "XGBoost",
                    "LightGBM",
                    "CatBoost",
                ],
                "Category": [
                    "Linear", "Linear", "Linear", "Probabilistic",
                    "Ensemble", "Ensemble", "Ensemble", "Ensemble",
                ],
                "Strengths": [
                    "Good at extrapolating, interpretable",
                    "Feature selection via L1 regularization",
                    "Combines L1 + L2 regularization",
                    "Handles non-linear patterns",
                    "Non-linear trends, variable interactions",
                    "Strong non-linear pattern recognition",
                    "Fast training on large datasets",
                    "Native categorical feature handling",
                ],
            }
            st.table(class_data)

        with tab2:
            st.markdown("### Regression Algorithms")
            reg_data = {
                "Algorithm": [
                    "Linear Regression",
                    "SGD Regression",
                    "Random Forest Regression",
                    "XGBoost Regression",
                    "LightGBM Regression",
                    "CatBoost Regression",
                ],
                "Category": [
                    "Linear", "Linear", "Ensemble", "Ensemble", "Ensemble", "Ensemble",
                ],
                "Strengths": [
                    "Extrapolation, linear trends",
                    "Scalable to large datasets",
                    "Non-linear trend detection",
                    "High accuracy for complex patterns",
                    "Fast, memory-efficient",
                    "Native categorical feature handling",
                ],
            }
            st.table(reg_data)

        with tab3:
            st.markdown("### Time Series Algorithms (Deep Learning, GPU-Accelerated)")
            st.info("Multivariate Time Series forecasting reached GA in October 2025.")
            ts_data = {
                "Algorithm": ["DeepAR", "TSMixer", "TiDE"],
                "Type": [
                    "Deep learning / probabilistic",
                    "Transformer-inspired",
                    "Deep learning encoder",
                ],
                "Best For": [
                    "Retail, supply chain; probabilistic forecasting",
                    "Balances accuracy and speed",
                    "Long-term dependencies in large datasets",
                ],
            }
            st.table(ts_data)

        section_divider()
        st.markdown("### Model Category Trade-offs")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **Linear Models**
            - Good at extrapolating
            - Interpretable
            - Struggle with non-linear patterns
            """)
        with col2:
            st.markdown("""
            **Ensemble Models**
            - Non-linear patterns
            - Variable interactions
            - Poor at extrapolating beyond training range
            """)
        with col3:
            st.markdown("""
            **Time Series Models**
            - Multivariate targets
            - Covariate support
            - Require GPU resources
            """)

    # ----- 2.4 HR Use Cases -----
    elif subsection == "2.4 HR Use Cases":
        st.header("HR Use Cases for Qlik Predict")

        tab1, tab2, tab3 = st.tabs([
            "Employee Turnover",
            "Promotion Prediction",
            "Lateral Movement",
        ])

        with tab1:
            st.markdown("### Predicting Employee Turnover / Attrition")
            st.markdown("""
            **Problem Type:** Binary Classification (Stayed vs. Left)

            **Training Data Features:**
            """)
            features = {
                "Feature Category": [
                    "Demographics", "Job Details", "Performance", "Engagement",
                    "Compensation", "Work Patterns", "Development", "Manager",
                ],
                "Example Fields": [
                    "Age, tenure, commute distance, education level",
                    "Department, role, job level, years in current role",
                    "Performance rating (last 3 years), project outcomes",
                    "Engagement survey scores, satisfaction index, eNPS",
                    "Base salary, bonus %, last raise %, salary band position",
                    "Overtime hours, remote work frequency, PTO usage",
                    "Training completions, certifications, mentoring participation",
                    "Manager tenure, manager span of control, manager change count",
                ],
            }
            st.table(features)

            st.markdown("""
            **Implementation Steps:**
            1. Prepare historical employee dataset with known attrition outcomes
            2. Set target column to attrition flag (Yes/No)
            3. Qlik Predict trains XGBoost, Random Forest, LightGBM, CatBoost, Logistic Regression, etc.
            4. Review SHAP values to understand top attrition drivers
            5. Deploy model and generate risk scores for current employees
            6. Build Qlik Sense dashboard with flight risk indicators by department, team, tenure band
            7. Set up Qlik Automate alerts when high-value employees are flagged at-risk

            **Intervention Strategies (Informed by Predictions):**
            - Career development conversations for employees with high "years since promotion" SHAP values
            - Workload rebalancing for employees where "overtime hours" is a top driver
            - Compensation adjustments where "salary band position" drives risk
            - Lateral move offers — one organization reduced attrition to zero for 6 months by offering
              lateral moves to 40% of at-risk employees
            """)

        with tab2:
            st.markdown("### Predicting Promotions")
            st.markdown("""
            **Problem Type:** Binary Classification (Promoted vs. Not Promoted)
            or Multiclass Classification (Promotion Level)

            **Key Features:**
            - Performance ratings over multiple review cycles
            - Training completion rates and skill assessments
            - Tenure in current role vs. organizational average
            - Project outcomes and 360-degree feedback scores
            - Education level and professional certifications
            - Cross-functional project participation

            **Value:**
            - Identifies high-potential employees for succession planning
            - Ensures equitable promotion practices across demographics
            - Predicts which employees are ready for advancement
            - Reduces bias by surfacing data-driven readiness indicators
            """)

        with tab3:
            st.markdown("### Predicting Lateral Movements")
            st.markdown("""
            **Problem Type:** Multiclass Classification or Regression

            **Modeling Approach:**
            Use historical data with Markov-style transitions to predict employee movement patterns
            including voluntary/involuntary turnover, retirements, and internal mobility.

            **Key Features:**
            - Current role tenure and breadth of experience
            - Cross-functional project participation
            - Expressed career interests (from development plans)
            - Internal application history
            - Skill adjacency mapping
            - Peer network analysis

            **Use Cases:**
            - Identify employees who would benefit from a role change before they become disengaged
            - Map internal talent pools to open positions
            - Predict which departments will have internal transfer demand
            - Build "career path probability" visualizations for employees
            """)

    # ----- 2.5 People Analytics Ideation -----
    elif subsection == "2.5 People Analytics Ideation":
        st.header("People Analytics Use Cases — Ideation")

        st.markdown("Beyond turnover, promotions, and lateral moves, here are additional use cases "
                     "a people analytics team can deploy with Qlik Predict:")

        use_cases = [
            {
                "name": "Flight Risk Scoring (60-90 day window)",
                "type": "Binary Classification",
                "desc": "Score each employee's probability of leaving within a specific window, enabling targeted retention interventions. Unlike general attrition models, this is time-bounded for actionability.",
            },
            {
                "name": "Absenteeism Prediction",
                "type": "Regression / Classification",
                "desc": "Predict employees likely to have high absenteeism. Correlate with engagement data, health benefits usage, workload metrics, and seasonal patterns.",
            },
            {
                "name": "Employee Engagement Forecasting",
                "type": "Regression",
                "desc": "Predict future engagement scores based on survey trends, manager changes, workload shifts, and organizational restructuring impacts.",
            },
            {
                "name": "Recruitment Success Prediction",
                "type": "Binary Classification",
                "desc": "Predict which candidates will be successful hires (tenure > 1 year + performance rating > 3) based on application data, interview scores, and source channel.",
            },
            {
                "name": "Time-to-Hire Forecasting",
                "type": "Time Series (MVTS)",
                "desc": "Predict how long open positions will take to fill based on role type, market conditions, location, seniority level, and historical hiring patterns.",
            },
            {
                "name": "Compensation Equity Analysis",
                "type": "Regression",
                "desc": "Predict expected salary based on role, experience, performance, location to identify pay inequities across gender, ethnicity, and other protected classes.",
            },
            {
                "name": "Training ROI Prediction",
                "type": "Regression",
                "desc": "Predict performance improvement from specific training programs to optimize L&D investment. Which programs yield the highest performance uplift?",
            },
            {
                "name": "Workforce Demand Forecasting",
                "type": "Time Series (MVTS)",
                "desc": "Use multivariate time series to forecast headcount needs across departments, factoring in seasonality, growth targets, attrition rates, and market conditions.",
            },
            {
                "name": "Succession Planning",
                "type": "Classification",
                "desc": "Identify employees with potential for leadership based on career trajectories, competencies, skill development velocity, and leadership assessment scores.",
            },
            {
                "name": "Internal Mobility Optimization",
                "type": "Multiclass Classification",
                "desc": "Predict optimal internal moves for employees based on skills, interests, performance history, and organizational needs. Match talent supply to demand.",
            },
            {
                "name": "Diversity & Inclusion Risk",
                "type": "Classification",
                "desc": "Identify departments at risk of diversity gaps based on hiring patterns, attrition by demographic, and promotion rate disparities.",
            },
            {
                "name": "New Hire Onboarding Success",
                "type": "Binary Classification",
                "desc": "Predict which new hires will reach full productivity within expected timeframes based on onboarding completion, buddy assignment, early check-in sentiment, and role complexity.",
            },
            {
                "name": "Benefits Utilization Prediction",
                "type": "Regression",
                "desc": "Predict healthcare and benefits costs per employee segment for better budget forecasting and benefits plan design.",
            },
            {
                "name": "Team Performance Forecasting",
                "type": "Regression",
                "desc": "Predict team-level performance outcomes based on team composition, diversity of skills, manager effectiveness, and workload distribution.",
            },
        ]

        for uc in use_cases:
            st.markdown(
                f'<div class="use-case-card">'
                f'<strong>{uc["name"]}</strong> — <em>{uc["type"]}</em><br>'
                f'{uc["desc"]}</div>',
                unsafe_allow_html=True,
            )

    # ----- 2.6 Demo -----
    elif subsection == "2.6 Demo":
        st.header("Demo: Qlik Predict")

        demo_placeholder(
            "Qlik Predict — Experiment Creation & Model Training",
            "https://techfieldday.com/video/qlik-self-service-ai-demo/"
        )

        st.markdown("### Demo Walkthrough: Employee Attrition Prediction")
        st.markdown("""
        1. **Upload Data**: Load `Employee_Attrition_Training.csv` with historical outcomes
        2. **Create Experiment**: Select `Attrition` as target column → auto-detected as Binary Classification
        3. **Review Models**: Qlik Predict trains 8 algorithms — XGBoost typically wins for tabular HR data
        4. **SHAP Analysis**: See that "YearsInCurrentRole", "OverTime", and "MonthlyIncome" are top drivers
        5. **Deploy Model**: Approve the best model for production
        6. **Generate Predictions**: Run batch predictions on current workforce
        7. **Visualize**: Load into Qlik Sense app with flight risk dashboard
        """)

        demo_placeholder(
            "Qlik Predict — SHAP Explainability Dashboard in Qlik Sense",
            "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/tutorial-machine-learning.htm"
        )

        demo_placeholder(
            "Qlik Predict — Real-Time What-If Scenario (Promotion Impact on Attrition)",
            "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/creating-real-time-predictions.htm"
        )

        st.markdown("""
        **Official Resources:**
        - [Qlik Predict Tutorial](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/tutorial-machine-learning.htm)
        - [Request a Qlik Predict Demo](https://www.qlik.com/us/contact-us/demo-request-predict)
        - [Tech Field Day Demo Video (June 2024)](https://techfieldday.com/video/qlik-self-service-ai-demo/)
        - [Community Sample Data](https://community.qlik.com/t5/Qlik-Predict/Qlik-AutoML-on-Qlik-Cloud-sample-data/td-p/1966212)
        - [Multivariate Time Series Blog](https://www.datavoyagers.net/post/beyond-the-event-horizon-multivariate-time-series-with-qlik-predict)
        """)


# =========================================================================
#  PART 3: APPLICATION AUTOMATIONS & LLM INTEGRATION
# =========================================================================
elif section == "Part 3: Application Automations & LLM":

    st.title("Part 3: Application Automations & External LLM Integration")

    # ----- 3.1 Executive Summary -----
    if subsection == "3.1 Executive Summary":
        exec_summary("Executive Summary — Application Automations & External LLMs", [
            "<b>What:</b> Qlik Application Automations (Qlik Automate) is a <b>no-code workflow automation platform</b> built into Qlik Cloud, enabling integration with external LLMs via REST API calls.",
            "<b>LLM Connectors:</b> Native OpenAI connector + generic API Key connector (for Claude, Cohere, custom endpoints) + <b>8 native analytic connections</b> (OpenAI, Azure OpenAI, Anthropic via Bedrock, Hugging Face, etc.).",
            "<b>Dynamic Updates:</b> Analytic connections in chart expressions respond to user selections in real-time — changing a selection triggers a new LLM call and updates the visualization.",
            "<b>Embedding:</b> Two patterns — <b>button-triggered automations</b> (workflow) and <b>analytic connection chart expressions</b> (inline real-time AI).",
            "<b>Fallback Strategy:</b> When Qlik Answers' structured data capabilities are insufficient, external LLMs provide free-form narratives, sentiment analysis, code generation, and custom domain reasoning directly within Qlik apps.",
        ])

    # ----- 3.2 Application Automations Overview -----
    elif subsection == "3.2 Application Automations Overview":
        st.header("Qlik Application Automations (Qlik Automate)")

        st.markdown("""
        Qlik Application Automations are a **no-code workflow automation platform** (iPaaS) built into
        Qlik Cloud. They enable users to build automated workflows between Qlik Cloud and external
        SaaS applications without writing code.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Core Capabilities
            - **Visual drag-and-drop builder** — blocks for data processing and logic control
            - **On-demand triggers** — manual or from Qlik Sense buttons
            - **Webhook triggers** — activate from external events
            - **Scheduled automations** — execute at specific times
            - **Pre-built connectors** — Salesforce, Teams, Slack, GitHub, ServiceNow, OpenAI, Hugging Face, etc.
            """)
        with col2:
            st.markdown("""
            ### Block Types
            - **Data blocks** — process data (API calls, transforms, read from Qlik app)
            - **Logic blocks** — control flow (conditions, loops, error handling)

            ### Integration with Qlik Sense
            - Triggered from **button actions** in Qlik Sense sheets
            - Can pass current user **selections** via temporary bookmarks
            - Results can be **written back** to apps or sent to external systems
            """)

        mermaid_diagram("""graph LR
    subgraph "Triggers"
        BTN[Button in Qlik Sense]
        WH[Webhook]
        SCH[Scheduled]
    end

    subgraph "Automation Workflow"
        T[Trigger] --> D1[Get Selections]
        D1 --> D2[Process Data]
        D2 --> L1{Condition}
        L1 -->|Yes| D3[Call External API]
        L1 -->|No| D4[Log & Skip]
        D3 --> D5[Process Response]
    end

    subgraph "Outputs"
        D5 --> WB[Write-Back to Qlik]
        D5 --> SL[Send to Slack/Teams]
        D5 --> EM[Send Email]
    end

    BTN --> T
    WH --> T
    SCH --> T""")

    # ----- 3.3 Integrating External LLMs -----
    elif subsection == "3.3 Integrating External LLMs":
        st.header("Integrating External LLMs into Qlik Cloud")

        st.markdown("There are **three primary mechanisms** for calling external LLMs:")

        tab1, tab2, tab3 = st.tabs([
            "Native OpenAI Connector",
            "API Key Connector (Any LLM)",
            "Analytic Connections (In-App)",
        ])

        with tab1:
            st.markdown("""
            ### Native OpenAI Connector (Application Automation)

            Qlik provides a dedicated OpenAI connector with these blocks:

            | Block | Purpose |
            |-------|---------|
            | **List Models** | Returns available OpenAI models |
            | **Retrieve Model** | Returns details about a specific model |
            | **Create Completion** | Generates text using a specified model |
            | **Raw API Request** | Full control — any OpenAI endpoint |
            | **Raw API List Request** | GET request returning iterable results |

            The **Raw API Request** block enables calls to any OpenAI endpoint including
            Chat Completions with custom system prompts, temperature, etc.
            """)

        with tab2:
            st.markdown("""
            ### API Key Connector (Generic REST — Any LLM)

            For LLMs without a dedicated connector (Anthropic Claude direct, Cohere, custom endpoints):

            | Setting | Description |
            |---------|-------------|
            | **Base URL** | LLM provider API base (e.g., `https://api.anthropic.com`) |
            | **HTTP Method** | GET, POST, DELETE, PATCH, PUT |
            | **Headers** | JSON for auth headers (e.g., `x-api-key`, `Authorization: Bearer`) |
            | **Request Body** | JSON payload for the chat completion request |
            | **Query Parameters** | JSON object appended to the URL |

            **Example: Calling Anthropic Claude via API Key Connector**
            ```json
            {
              "Base URL": "https://api.anthropic.com/v1/messages",
              "Method": "POST",
              "Headers": {
                "x-api-key": "sk-ant-...",
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
              },
              "Body": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [
                  {"role": "user", "content": "Analyze this HR data: ..."}
                ]
              }
            }
            ```
            """)

        with tab3:
            st.markdown("""
            ### Analytic Connections (Native In-App Connectors)

            Qlik Cloud provides native analytics source connectors for direct use in
            **load scripts and chart expressions**:

            | Connector | LLM Provider | Auth Method |
            |-----------|-------------|-------------|
            | **OpenAI** | GPT models | API key |
            | **Azure OpenAI** | GPT via Azure | Azure API key + endpoint |
            | **Anthropic (Amazon Bedrock)** | Claude models | AWS Access Key + Secret |
            | **Amazon Bedrock - Converse API** | All Bedrock models | AWS credentials |
            | **Amazon Titan (Bedrock)** | Titan models | AWS credentials |
            | **Cohere (Amazon Bedrock)** | Cohere models | AWS credentials |
            | **Meta (Amazon Bedrock)** | Llama models | AWS credentials |
            | **Hugging Face** | Open-source models | HF API key |

            **Chart Expression Example:**
            ```
            if(count(distinct [EmployeeName]) = 1,
               endpoints.ScriptAggrStr(
                 '{"RequestType":"endpoint",
                   "endpoint":{
                     "connectionname":"OpenAI_HR_Analysis",
                     "column":"choices.message.content"
                   }
                 }',
                 'Analyze retention risk for: '
                 & [EmployeeName] & ' in ' & [Department]
                 & ' with tenure ' & [YearsAtCompany] & ' years'
               )
            )
            ```
            """)

    # ----- 3.4 Analytic Connections (Dynamic Updates) -----
    elif subsection == "3.4 Analytic Connections (Dynamic Updates)":
        st.header("Analytic Connections — Dynamic Updates with Selections")

        st.markdown("""
        ### How Analytic Connections React to User Selections

        Analytic connections in Qlik Cloud use the **Server-Side Extension (SSE) protocol**.
        When used in chart expressions, they respond dynamically to user selections:
        """)

        mermaid_diagram("""sequenceDiagram
    participant User
    participant QS as Qlik Sense App
    participant AE as Associative Engine
    participant SSE as Analytics Connector
    participant LLM as External LLM API

    User->>QS: Make selection (e.g., select employee)
    QS->>AE: Recalculate all expressions
    AE->>SSE: Send filtered data via SSE
    SSE->>LLM: REST API call with selected data
    LLM-->>SSE: AI-generated response
    SSE-->>AE: Return response text
    AE-->>QS: Update Text & Image object
    QS-->>User: Display LLM insight for selection

    Note over User,LLM: User clears selection, picks another →<br/>entire flow repeats automatically""")

        st.markdown("""
        ### Key Design Patterns

        **1. Gate LLM calls behind single selections (cost control)**
        ```
        if(count(distinct [FieldName]) = 1,
           endpoints.ScriptAggrStr(...),
           'Please select exactly one employee to see AI analysis.'
        )
        ```

        **2. Dynamic prompt construction from selections**
        ```
        'Analyze the following employee data: '
        & 'Name: ' & [EmployeeName]
        & ', Department: ' & [Department]
        & ', Tenure: ' & [YearsAtCompany]
        & ', Performance: ' & [PerformanceRating]
        & ', Flight Risk Score: ' & [PredictedAttritionProbability]
        ```

        **3. Use only in Text & Image chart objects** (not Tables)

        **4. Constraints:**
        - Max **25 rows per request**, batch size of 1 row
        - Rate limits depend on LLM provider
        - For Anthropic (Messages API via Bedrock), no special prompt syntax needed
        """)

        st.markdown("""
        ### Integration Pattern: Combining Qlik Predict + LLM Analysis

        A powerful pattern for people analytics:
        1. **Qlik Predict** generates attrition risk scores for all employees (batch)
        2. **Analytic Connection** calls an LLM when a user selects a specific at-risk employee
        3. The LLM receives the employee's data + risk score and generates:
           - Natural language explanation of the risk factors
           - Personalized retention recommendations
           - Suggested conversation starters for the manager
        """)

    # ----- 3.5 Fallback Architecture -----
    elif subsection == "3.5 Fallback Architecture":
        st.header("Fallback Architecture: When Qlik Answers Isn't Enough")

        st.markdown("""
        When Qlik Answers' structured data capabilities are insufficient for specific use cases,
        external LLM integration provides a powerful fallback:
        """)

        fallback_data = {
            "Limitation of Qlik Answers": [
                "Cannot generate free-form text narratives",
                "Cannot analyze unstructured text (complaints, reviews)",
                "Cannot perform cross-domain reasoning",
                "Limited to Qlik's predefined question patterns",
                "No custom model fine-tuning",
                "Cannot generate code or expressions dynamically",
            ],
            "Fallback via External LLM": [
                "Use OpenAI/Claude expressions for summaries and recommendations",
                "Send text to LLM for sentiment analysis, classification, summarization",
                "External LLMs combine Qlik data with general domain knowledge",
                "External LLMs handle open-ended, creative prompts",
                "Connect to fine-tuned models on Hugging Face or custom endpoints",
                "Use LLM to generate Qlik load scripts, set analysis expressions, etc.",
            ],
        }
        st.table(fallback_data)

        section_divider()

        st.markdown("### Recommended Fallback Decision Flow")
        mermaid_diagram("""graph TD
    START[User in Qlik Sense App] --> Q1{Standard analytics<br/>question?}
    Q1 -->|Yes| QA[Qlik Answers<br/>Agentic Analytics]
    Q1 -->|No| Q2{Need AI-generated<br/>narrative/analysis?}
    Q2 -->|Yes| AC[Analytic Connection<br/>Chart Expression]
    Q2 -->|No| Q3{Need multi-step<br/>workflow with AI?}
    Q3 -->|Yes| AUTO[Button → Application<br/>Automation]
    Q3 -->|No| Q4{Need to expose data<br/>to external AI?}
    Q4 -->|Yes| MCP_NODE[Qlik MCP Server]

    AC --> LLM1[OpenAI / Azure OpenAI /<br/>Anthropic Bedrock / Hugging Face]
    AUTO --> LLM2[OpenAI Connector /<br/>API Key Connector - any LLM]
    MCP_NODE --> LLM3[Claude Desktop /<br/>ChatGPT / Custom Agents]

    LLM1 --> OUT1[Display in Text & Image object]
    LLM2 --> OUT2[Write-back / Slack /<br/>Teams / Email]
    LLM3 --> OUT3[Insights in external<br/>AI assistant UI]""")

        st.markdown("""
        ### Design Principles for the Fallback Pattern

        1. **Gate LLM calls behind selections** — always use `if()` statements to prevent runaway API costs
        2. **Cache where possible** — use load-script-based LLM calls with QVD caching for repeated insights
        3. **Separate concerns** — Analytic Connections for display; Automations for workflows/write-back
        4. **API Key connector for non-standard LLMs** — any REST API is reachable
        5. **Amazon Bedrock Converse API** — recommended as the unified connector for multi-model Bedrock access
        """)

        st.markdown("""
        ### Integration Method Summary

        | Method | Providers | Trigger | Output | Best For |
        |--------|-----------|---------|--------|----------|
        | **Analytic Connection (Chart)** | OpenAI, Azure, Bedrock, HF | User selection | Text & Image object | Real-time inline AI |
        | **Analytic Connection (Load Script)** | Same | Data reload | Stored in data model | Batch pre-computation |
        | **Automation (OpenAI Connector)** | OpenAI | Button/webhook/schedule | Write-back, Slack, etc. | Multi-step OpenAI workflows |
        | **Automation (API Key Connector)** | Any REST API | Button/webhook/schedule | Write-back, Slack, etc. | Any LLM via HTTP |
        | **Qlik MCP Server** | Claude, ChatGPT, custom | External AI initiates | External AI UI | Exposing Qlik to external AI |
        """)

    # ----- 3.6 Demo -----
    elif subsection == "3.6 Demo":
        st.header("Demo: Application Automations & LLM Integration")

        demo_placeholder(
            "Analytic Connection — Selection-Driven LLM Response in Qlik Sense",
            "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/LoadData/ac-openai-tutorial-example-interactive.htm"
        )

        st.markdown("### Demo Walkthrough: LLM-Powered Employee Insight")
        st.markdown("""
        1. **Open Qlik Sense app** with employee data + flight risk scores from Qlik Predict
        2. **Select an employee** from the filter pane
        3. **Text & Image object** fires an analytic connection to OpenAI/Claude
        4. **Prompt sent**: "Analyze retention risk for [Employee] in [Dept] with [Risk Score]"
        5. **LLM response appears** inline in the dashboard: personalized risk narrative + recommendations
        6. **Change selection** to a different employee — response updates automatically
        """)

        demo_placeholder(
            "Application Automation — Button-Triggered LLM Workflow",
            "https://help.qlik.com/en-US/video/GBvy1WtF2B9Akf1e564dtv"
        )

        st.markdown("""
        **Official Resources:**
        - [Interactive OpenAI Example App](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/LoadData/ac-openai-tutorial-example-interactive.htm)
        - [OpenAI Analytics Connector Tutorial](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/LoadData/ac-openai-tutorial.htm)
        - [Anthropic (Bedrock) Connection Guide](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/LoadData/ac-bedrock-anthropic-use.htm)
        - [Application Automation Overview Video](https://help.qlik.com/en-US/video/GBvy1WtF2B9Akf1e564dtv)
        - [Automation Trigger Extension (GitHub)](https://github.com/rileymd88/automation-trigger)
        """)


# =========================================================================
#  PART 4: QLIK CLOUD AI/ML ECOSYSTEM
# =========================================================================
elif section == "Part 4: Qlik Cloud AI/ML Ecosystem":

    st.title("Part 4: Qlik Cloud AI/ML Ecosystem")

    # ----- 4.1 Executive Summary -----
    if subsection == "4.1 Executive Summary":
        exec_summary("Executive Summary — Qlik Cloud AI/ML Ecosystem", [
            "<b>Platform:</b> Qlik's AI strategy is branded under <b>Qlik Staige</b> — a unified platform spanning data integration, analytics, and AI across the data lifecycle.",
            "<b>GA Features (2025-2026):</b> Qlik Answers (agentic analytics), Qlik Predict (AutoML), MCP Server, Analytic Connections (8 LLM connectors), Application Automations, Augmented Analytics (Insight Advisor or Qlik Answers).",
            "<b>Upcoming:</b> Discovery Agent (anomaly detection), Data Products for Analytics, expanded MCP support for additional AI tools, agentic extensions across data pipelines and data quality.",
            "<b>Key Differentiator:</b> Qlik's AI capabilities are grounded in the <b>Qlik Associative Engine</b> — ensuring governed, context-preserving calculations rather than hallucinated responses.",
            "<b>Cloud Only:</b> All features described are Qlik Cloud (SaaS) — not available in Qlik Sense Enterprise on Windows.",
        ])

    # ----- 4.2 Current AI/ML Features -----
    elif subsection == "4.2 Current AI/ML Features":
        st.header("Current AI/ML Features in Qlik Cloud")

        features = [
            {
                "name": "Qlik Answers (Agentic Analytics)",
                "status": "GA (Feb 2026)",
                "desc": "Unified conversational AI interface combining structured data analytics (via Qlik Engine) with unstructured document Q&A (via RAG). Replaces Insight Advisor in enabled tenants.",
            },
            {
                "name": "Qlik Predict (AutoML)",
                "status": "GA",
                "desc": "No-code automated machine learning for classification, regression, and time series forecasting. SHAP explainability, model monitoring, and multiple deployment options.",
            },
            {
                "name": "Multivariate Time Series Forecasting",
                "status": "GA (Oct 2025)",
                "desc": "GPU-accelerated deep learning models (DeepAR, TSMixer, TiDE) for temporal forecasting with covariates. Part of Qlik Predict.",
            },
            {
                "name": "Qlik MCP Server",
                "status": "GA (Feb 2026)",
                "desc": "Model Context Protocol server exposing Qlik at engine, tool, and agent levels. Enables third-party AI assistants (Claude, ChatGPT) to access governed Qlik data.",
            },
            {
                "name": "Analytic Connections (LLM Connectors)",
                "status": "GA",
                "desc": "8 native connectors for OpenAI, Azure OpenAI, Anthropic (Bedrock), Amazon Bedrock Converse, Titan, Cohere, Meta Llama, and Hugging Face. Used in load scripts and chart expressions.",
            },
            {
                "name": "Application Automations (Qlik Automate)",
                "status": "GA",
                "desc": "No-code workflow automation platform with native OpenAI connector and generic API Key connector for any REST API. Triggered by buttons, webhooks, or schedules.",
            },
            {
                "name": "Insight Advisor (Augmented Analytics)",
                "status": "GA (being replaced by Qlik Answers)",
                "desc": "NL search and chat-based analytics within Qlik Sense apps. Full business logic support. Still available in tenants that haven't enabled Qlik Answers.",
            },
            {
                "name": "AI-Generated Narratives (Insight Advisor)",
                "status": "GA",
                "desc": "Auto-generated natural language summaries of charts and data patterns. Available within Insight Advisor analysis.",
            },
            {
                "name": "Key Driver Analysis",
                "status": "GA",
                "desc": "Automated identification of key drivers behind a target metric. Uses statistical analysis to surface which dimensions most influence outcomes.",
            },
            {
                "name": "Anomaly Detection (Insight Advisor)",
                "status": "GA",
                "desc": "Automatic detection of outliers and anomalies in time series data within Insight Advisor analysis.",
            },
            {
                "name": "Natural Language Processing (NLP)",
                "status": "GA",
                "desc": "Powers natural language question understanding in both Insight Advisor and Qlik Answers. Supports synonyms, field mappings, and query interpretation.",
            },
            {
                "name": "Write Table (Writeback)",
                "status": "GA (Oct 2025)",
                "desc": "Native writeback capability allowing users to edit data directly in Qlik Sense apps. Combined with Qlik Predict for actionable forecasting workflows.",
            },
        ]

        for f in features:
            with st.expander(f'{f["name"]} — {f["status"]}'):
                st.markdown(f["desc"])

        section_divider()

        st.markdown("### AI-Powered Data Quality & Governance (Qlik Talend Cloud)")

        dq_features = [
            {
                "name": "Qlik Trust Score for AI",
                "status": "GA (July 2025)",
                "desc": "Purpose-built scoring for AI-readiness of data. Dimensions include **Diversity** (reduces bias), **Timeliness** (data freshness), **Accuracy** (business rule validation), **Discoverability**, and **Usage**. Planned dimensions: Security and LLM Readiness. Supports historization to correlate shifts with model drift.",
            },
            {
                "name": "AI-Native Data Stewardship",
                "status": "Early Access (Fall 2025)",
                "desc": "Proactively detects and resolves data issues earlier in the lifecycle. Combines automated rules, human-in-the-loop workflows, and platform-wide governance.",
            },
            {
                "name": "Generative AI for Data Documentation",
                "status": "GA (Oct 2025)",
                "desc": "Auto-generates field-level descriptions for dataset fields based on column names and context. Reduces manual documentation burden.",
            },
            {
                "name": "Knowledge Mart Tasks",
                "status": "GA",
                "desc": "Automate transformation, vectorization, and loading of data into vector stores. Supports custom semantic search and RAG AI applications. Domain-specific collections with incremental refresh. Currently supported on Snowflake.",
            },
        ]

        for f in dq_features:
            with st.expander(f'{f["name"]} — {f["status"]}'):
                st.markdown(f["desc"])

        st.markdown("### AI-Assisted Development & Data Preparation")

        dev_features = [
            {
                "name": "Natural Language Expression Generator",
                "status": "GA",
                "desc": "Built into the expression editor. Type natural language descriptions to generate Qlik expressions. Supports field names, master items, aggregations, and filters.",
            },
            {
                "name": "AI-Assisted Script Generation",
                "status": "GA",
                "desc": "Generate Qlik load scripts through natural language prompts. Automated SQL code generation for faster model building.",
            },
            {
                "name": "Table Recipe",
                "status": "GA",
                "desc": "Streamlined, spreadsheet-like experience for preparing single-table datasets without scripting. 60+ visual functions for cleaning, converting, and formatting data. Real-time preview of changes.",
            },
            {
                "name": "Qlik Open Lakehouse",
                "status": "GA (Oct 2025)",
                "desc": "Iceberg-powered lakehouse architecture on AWS (S3 + EC2 spot instances). High-throughput ingestion into Apache Iceberg with continuous optimization. AI-augmented data pipelines for RAG, GenAI, and ML solutions.",
            },
        ]

        for f in dev_features:
            with st.expander(f'{f["name"]} — {f["status"]}'):
                st.markdown(f["desc"])

        st.markdown("""
        **Sources:**
        - [Qlik Trust Score for AI](https://www.qlik.com/us/news/company/press-room/press-releases/qlik-releases-trust-score-for-ai-in-qlik-talend-cloud)
        - [Knowledge Mart Help](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/DataIntegration/KnowledgeMart/Creating-knowledge-marts.htm)
        - [Qlik Open Lakehouse](https://community.qlik.com/t5/Release-Notes/Qlik-Cloud-Release-Notes-October-2025/ta-p/2532869)
        - [Qlik Announces Qlik Staige](https://www.qlik.com/us/news/company/press-room/press-releases/qlik-announces-qlik-staige)
        """)

    # ----- 4.3 Planned Features -----
    elif subsection == "4.3 Planned / Upcoming Features":
        st.header("Planned / Upcoming AI Features")

        st.markdown("""
        Based on Qlik's announcements and roadmap communications (as of March 2026):

        | Feature | Status | Description |
        |---------|--------|-------------|
        | **Discovery Agent** | Rolling out post-GA | Continuously monitors key measures and surfaces meaningful anomalies and shifts. Proactive alerting before issues escalate. |
        | **Data Products for Analytics** | Rolling out post-GA | Curated, governed datasets with stewardship and quality signals. Foundation for both human and AI analysis. |
        | **Productivity Agents** | In development | Embedded across all Qlik Cloud workflows — contextual help, developer support, and analytical assistance. |
        | **Expanded MCP Support** | Planned 2026 | Support for additional AI tools and assistants beyond Claude and ChatGPT throughout 2026. |
        | **Agentic Data Pipeline Agents** | Planned | AI agents for automating data integration, transformation, and quality workflows. |
        | **Agentic Data Quality Agents** | Planned | AI-powered data quality monitoring, anomaly detection, and remediation across data pipelines. |
        | **Agentic Stewardship Agents** | Planned | AI agents for data governance, cataloging, and stewardship automation. |
        | **GenAI Insight Advisor Narratives** | Private Preview | ChatGPT-like answers with human-sounding narrative powered by Amazon Bedrock LLM. |
        | **Trust Score: Security + LLM Readiness** | Planned | Additional dimensions for AI data readiness scoring. |
        | **AWS European Sovereign Cloud** | Planned 2026 | Qlik Cloud deployment on sovereign infrastructure ($1.5B European investment over 5 years). |
        | **Governed Writeback (SAP, Salesforce, Snowflake)** | Planned | Native writeback connectors to enterprise systems. |
        """)

        section_divider()

        st.markdown("### Full Feature Timeline")
        st.markdown("""
        | Feature | Status | Availability |
        |---------|--------|-------------|
        | Qlik Staige (portfolio) | GA | Available now |
        | Insight Advisor (NLP, search, chat) | GA | Available now |
        | Qlik Predict (AutoML) | GA | Available now |
        | GenAI Connectors (OpenAI, Bedrock, etc.) | GA | Available now |
        | Qlik Automate (decision triggers) | GA | Available now |
        | Qlik Answers (original, unstructured) | GA | Since July 2024 |
        | Qlik Trust Score for AI | GA | Since July 2025 |
        | Table Recipe | GA | Since mid-2025 |
        | Knowledge Mart Tasks | GA | Since mid-2025 |
        | Qlik Open Lakehouse | GA | Since October 2025 |
        | Multivariate Time Series | GA | Phased from summer 2025 |
        | Write Table (Writeback) | GA | October 2025 |
        | Qlik Answers (Agentic) | GA | February 2026 |
        | Qlik MCP Server | GA | February 2026 |
        | Discovery Agent | Planned | Post-Feb 2026 GA |
        | Data Products for Analytics | Planned | Post-Feb 2026 GA |
        | Productivity Agents | Planned | In development |
        """)

        st.markdown("""
        ### Qlik's Agentic Strategy

        Qlik's agentic strategy is designed to expand over time, with agents planned across:
        - Data pipelines
        - Data quality
        - Data stewardship
        - Analytics (currently via Qlik Answers + Discovery Agent)

        The MCP Server is the extensibility mechanism — allowing any MCP-compatible AI assistant
        to access Qlik's capabilities.
        """)

        st.markdown("### Strategic Partnerships & Recognition")
        st.markdown("""
        | Achievement | Details |
        |------------|---------|
        | **AWS Generative AI Competency** | Technical proficiency in leveraging Amazon Bedrock and SageMaker |
        | **AWS European Sovereign Cloud** | Launch partner; $1.5B European investment over 5 years |
        | **AWS Marketplace AI Category** | Qlik Cloud Analytics in AI Agents and Tools category |
        | **Gartner MQ: Analytics & BI** | Leader for 15th year (2025) |
        | **Gartner MQ: Data Quality** | Leader for 6th time (2025) |
        | **Qlik AI Specialist Certification** | New certification covering AI concepts, Qlik Predict, GenAI assistants |
        | **Kyndi Acquisition (2024)** | NLP, search, and generative AI capabilities |
        | **Upsolver Acquisition (2025)** | Real-time data processing capabilities |
        """)

        st.markdown("""
        **Sources:**
        - [AWS Generative AI Competency](https://www.qlik.com/us/news/company/press-room/press-releases/qlik-achieves-aws-generative-ai-competency)
        - [Qlik AI Specialist Certification](https://learning.qlik.com/student/page/2537679-qlik-ai-specialist-certification-exam)
        - [Qlik Brings Agentic Analytics to GA](https://www.businesswire.com/news/home/20260210837577/en/Qlik-Brings-Agentic-Analytics-to-General-Availability-and-Launches-MCP-Server-for-Third-Party-Assistants)
        """)

    # ----- 4.4 Qlik Staige -----
    elif subsection == "4.4 Qlik Staige Platform":
        st.header("Qlik Staige — Unified AI Platform")

        st.markdown("""
        **Qlik Staige** is Qlik's unified platform brand for AI capabilities across the data lifecycle.
        It encompasses all AI features within Qlik Cloud.
        """)

        mermaid_diagram("""graph TB
    subgraph "Qlik Staige Platform"
        subgraph "Data Integration AI"
            DI[Agentic Data Pipeline Agents]
            DQ[Data Quality AI]
            DS[Data Stewardship AI]
        end

        subgraph "Analytics AI"
            QA[Qlik Answers<br/>Agentic Analytics]
            QP[Qlik Predict<br/>AutoML]
            DA[Discovery Agent]
            IA[Insight Advisor<br/>Augmented Analytics]
        end

        subgraph "Extensibility"
            MCP[MCP Server]
            AC[Analytic Connections<br/>8 LLM Connectors]
            AA[Application Automations]
        end

        subgraph "Foundation"
            AE[Qlik Associative Engine]
            DP[Data Products for Analytics]
            GOV[AI Governance & Trust]
        end
    end

    AE --> QA
    AE --> IA
    DP --> QA
    DP --> DA
    GOV --> QA
    GOV --> QP
    GOV --> MCP""")

        st.markdown("""
        ### Key Principles of Qlik Staige

        1. **Grounded in Governed Data** — All AI responses are powered by the Qlik Associative Engine,
           ensuring calculations are governed and auditable, not hallucinated.

        2. **Transparent Reasoning** — Qlik Answers provides citations and explanations of how
           conclusions were reached, building trust in AI-generated insights.

        3. **No Data Science Required** — Qlik Predict's AutoML approach means analytics teams
           can build and deploy ML models without coding or data science expertise.

        4. **Open Ecosystem** — The MCP Server and Analytic Connections ensure Qlik is not a
           closed system but can integrate with the broader AI ecosystem.

        5. **Embedded, Not Bolted On** — AI is embedded directly into the analytics workflow
           (side panels, chart expressions, automations) rather than being a separate product.
        """)

        section_divider()

        st.markdown("### AI Governance Framework")
        st.markdown("""
        Qlik's AI governance approach spans the entire platform:

        | Governance Layer | Mechanism |
        |-----------------|-----------|
        | **Governed Calculations** | All analytical answers powered by Qlik Associative Engine, not raw LLM generation |
        | **Citations & Explainability** | Every AI answer traces back to original data sources |
        | **SHAP Model Explainability** | Feature importance at global and individual prediction levels |
        | **Data Lineage & Provenance** | Full tracking of data transformations and origins |
        | **Trust Score for AI** | Purpose-built data readiness scoring (Diversity, Timeliness, Accuracy) |
        | **Role-Based Access Controls** | Granular permissions on AI features and data products |
        | **Global AI Council** | External experts guiding product direction and responsible AI (formed Jan 2024) |
        | **Enterprise MLOps** | Version control, monitoring, retraining, lifecycle management |
        | **Data Products with Stewardship** | Quality signals for governed, reusable datasets |
        | **EU Data Sovereignty** | Support via AWS European Sovereign Cloud |
        """)

        st.markdown("""
        **Sources:**
        - [Qlik Agentic AI](https://www.qlik.com/us/agentic-ai)
        - [Qlik Cloud Analytics](https://www.qlik.com/us/products/qlik-cloud-analytics)
        - [Qlik Augmented Analytics](https://www.qlik.com/us/products/qlik-augmented-analytics)
        - [Qlik Predict](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/home-automl.htm)
        - [Qlik MCP Server](https://www.qlik.com/us/products/model-context-protocol)
        - [Qlik Why AI](https://www.qlik.com/us/why-qlik-for-ai)
        """)


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Sources & References**
- [Qlik Cloud Help](https://help.qlik.com/en-US/cloud-services/)
- [Qlik Developer Portal](https://qlik.dev/)
- [Qlik Community](https://community.qlik.com/)
- [Qlik Press Room](https://www.qlik.com/us/news/company/press-room/)
""")
st.sidebar.markdown("*Built with Streamlit — Qlik Cloud focused (no on-premises content)*")
