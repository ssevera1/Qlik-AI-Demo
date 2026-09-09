"""
PDF Export Module
=================
Generates a comprehensive PDF of all sections and subsections
using fpdf2. Pure Python — no external connections.
"""

from fpdf import FPDF
from pathlib import Path
import datetime


# -- Brand colors -----------------------------------------------------------
_RED = (238, 0, 17)       # #EE0011
_CREAM = (246, 240, 226)  # #F6F0E2
_WHITE = (255, 255, 255)
_BLACK = (0, 0, 0)
_MUTED = (85, 85, 85)     # #555555
_BORDER = (213, 207, 193) # #D5CFC1
_BLUE = (0, 137, 236)     # #0089EC
_GREEN = (0, 184, 69)     # #00B845
_SIDEBAR = (237, 231, 217)# #EDE7D9


class _QlikPDF(FPDF):
    """Custom PDF with branded header/footer."""

    def __init__(self, logo_path: Path | None = None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self._logo_path = logo_path
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        # Cream bar at top
        self.set_fill_color(*_CREAM)
        self.rect(0, 0, 210, 18, style="F")
        # Red accent line
        self.set_fill_color(*_RED)
        self.rect(0, 18, 210, 1, style="F")

        # Logo only on first page
        if self.page_no() == 1 and self._logo_path and self._logo_path.exists():
            self.image(str(self._logo_path), x=8, y=2, h=14)

        # Title
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*_BLACK)
        self.set_xy(0, 5)
        self.cell(200, 8, "Qlik Cloud AI/ML Capabilities", align="R")
        self.ln(16)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(136, 136, 136)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def _add_part_title(pdf: _QlikPDF, title: str):
    """Full-width red banner for a Part heading."""
    pdf.add_page()
    pdf.set_fill_color(*_RED)
    pdf.rect(10, pdf.get_y(), 190, 14, style="F")
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*_WHITE)
    pdf.cell(190, 14, f"  {title}", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*_BLACK)
    pdf.ln(6)


def _add_section_title(pdf: _QlikPDF, title: str):
    """Blue-accented section heading."""
    pdf.ln(4)
    pdf.set_fill_color(*_BLUE)
    pdf.rect(10, pdf.get_y(), 3, 8, style="F")
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*_BLACK)
    pdf.set_x(16)
    pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)


def _add_subsection(pdf: _QlikPDF, title: str):
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*_RED)
    pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*_BLACK)
    pdf.ln(1)


def _body(pdf: _QlikPDF, text: str):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*_BLACK)
    pdf.multi_cell(0, 5, text)
    pdf.ln(2)


def _bullet(pdf: _QlikPDF, text: str):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*_BLACK)
    pdf.set_x(14)
    pdf.multi_cell(186, 5, f"  -  {text}")


def _link(pdf: _QlikPDF, label: str, url: str):
    """Render a clickable link as a bullet item."""
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*_BLUE)
    pdf.set_x(14)
    pdf.cell(4, 5, "-  ")
    pdf.cell(0, 5, label, link=url, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*_BLACK)


def _links_section(pdf: _QlikPDF, title: str, links: list[tuple[str, str]]):
    """Render a sources/references block with clickable links."""
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*_MUTED)
    pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
    for label, url in links:
        _link(pdf, label, url)
    pdf.set_text_color(*_BLACK)
    pdf.ln(3)


def _table(pdf: _QlikPDF, headers: list[str], rows: list[list[str]],
           col_widths: list[int] | None = None):
    """Simple bordered table."""
    if col_widths is None:
        w = int(190 / len(headers))
        col_widths = [w] * len(headers)
        # give remainder to last col
        col_widths[-1] = 190 - w * (len(headers) - 1)

    # header row
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*_SIDEBAR)
    pdf.set_draw_color(*_BORDER)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, f" {h}", border=1, fill=True)
    pdf.ln()

    # data rows
    pdf.set_font("Helvetica", "", 8)
    pdf.set_fill_color(*_WHITE)
    for row in rows:
        max_h = 7
        # calculate row height
        for i, cell_text in enumerate(row):
            lines = pdf.multi_cell(col_widths[i], 5, f" {cell_text}",
                                   border=0, new_x="RIGHT", new_y="TOP",
                                   dry_run=True, output="LINES")
            h = max(7, len(lines) * 5)
            max_h = max(max_h, h)
        for i, cell_text in enumerate(row):
            x = pdf.get_x() if i > 0 else 10
            y = pdf.get_y()
            pdf.rect(x, y, col_widths[i], max_h, style="D")
            pdf.set_xy(x, y)
            pdf.multi_cell(col_widths[i], 5, f" {cell_text}", border=0,
                           new_x="RIGHT", new_y="TOP")
        pdf.ln(max_h)
    pdf.ln(3)


def _exec_box(pdf: _QlikPDF, title: str, bullets: list[str]):
    """Executive summary box."""
    y_start = pdf.get_y()
    pdf.set_fill_color(*_WHITE)
    pdf.set_draw_color(*_BORDER)

    # We'll draw the box after we know the height
    x0 = 10
    pdf.set_x(x0 + 5)

    # Title
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*_RED)
    pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*_BLACK)
    pdf.set_font("Helvetica", "", 9)

    for b in bullets:
        # strip HTML bold tags for PDF
        clean = b.replace("<b>", "").replace("</b>", "")
        pdf.set_x(x0 + 7)
        pdf.multi_cell(175, 5, f"-  {clean}")
        pdf.ln(1)

    y_end = pdf.get_y()
    # draw border
    pdf.set_draw_color(*_BORDER)
    pdf.rect(x0, y_start, 190, y_end - y_start + 2, style="D")
    # red left accent
    pdf.set_fill_color(*_RED)
    pdf.rect(x0, y_start, 2, y_end - y_start + 2, style="F")
    pdf.set_y(y_end + 4)


# ===========================================================================
#  Content builders — one per section
# ===========================================================================

def _build_home(pdf: _QlikPDF):
    _add_part_title(pdf, "Qlik Cloud AI/ML Capabilities")

    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*_MUTED)
    pdf.cell(0, 6, "A Comprehensive Reference for People Analytics Teams", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 5, "Created by Scott Severance", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*_BLACK)
    pdf.ln(4)

    _exec_box(pdf, "Application Overview", [
        "Covers Qlik Answers (agentic analytics with structured + unstructured data): GA Feb 2026, extended to a four-agent roster at Qlik Connect 2026",
        "Documents Qlik Predict (AutoML) with HR-specific use cases for turnover, promotions, and lateral moves, plus the new Predict Agent for natural-language model building",
        "Explains Application Automations for integrating external LLMs (OpenAI, Claude, etc.) into Qlik apps, including agent-triggered automation runs",
        "Maps the full Qlik Cloud AI/ML ecosystem: Discovery, Predict, Automate, and Analytics Agents, MCP Server (GA Feb 2026), and Agentic Data Engineering (GA July 2026)",
        "All content is Qlik Cloud only, with no on-premises Qlik Sense Enterprise content",
    ])

    _add_subsection(pdf, "Timeline of Key Announcements")
    _table(pdf, ["Date", "Milestone"], [
        ["2024", "Qlik Answers launched (unstructured data only)"],
        ["May 2025", "Agentic analytics vision announced at Qlik Connect"],
        ["Oct 2025", "Multivariate Time Series GA in Qlik Predict"],
        ["Dec 2025", "Agentic Qlik Answers private preview"],
        ["Feb 2026", "Qlik Answers agentic GA + MCP Server GA; Qlik Cloud Government - DoD launched"],
        ["Mar 2026", "Discovery Agent rolling out; Data Products for Analytics rolling out"],
        ["Apr 2026", "Qlik Connect 2026 (April 13-15, Kissimmee FL): Predict, Automate, and Analytics Agents announced; Semantic Layer for Data Products; Open Lakehouse streaming"],
        ["Jun 2026", "Automate Agent and Predict Agent available; Answers Fast Mode; Gartner A&BI Leader, 16th consecutive year"],
        ["Jul 2026", "Agentic Data Engineering GA; Qlik Predict inside Qlik Answers; Answers Review Portal; Answers-triggered Automate actions; conversation PDF export"],
        ["Sep 2026", "MCP tools for declarative pipelines (qlik_search, pipeline and connection introspection)"],
    ], [35, 155])

    _links_section(pdf, "Quick Links", [
        ("Qlik Answers Product Page", "https://www.qlik.com/us/products/qlik-answers"),
        ("Qlik Predict Documentation", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/home-automl.htm"),
        ("Qlik Automate Product Page", "https://www.qlik.com/us/products/qlik-automate"),
        ("Qlik Cloud Help", "https://help.qlik.com/en-US/cloud-services/"),
        ("Qlik Developer Portal", "https://qlik.dev/"),
    ])


def _build_part1(pdf: _QlikPDF):
    _add_part_title(pdf, "Part 1: Qlik Answers - Agentic Analytics with Structured Data")

    # 1.1
    _add_section_title(pdf, "1.1 Executive Summary")
    _exec_box(pdf, "Executive Summary - Qlik Answers Structured Data", [
        "What: Qlik Answers now supports structured data from Qlik analytic applications alongside unstructured documents (PDFs, DOCX, HTML), powered by an agentic AI framework and the Qlik Analytics Engine.",
        "When: General Availability as of February 10, 2026. Private preview began December 2025.",
        "Impact: Qlik Answers replaces Insight Advisor and Insight Advisor Chat in enabled tenants. This is a tenant-wide change, and the two experiences cannot run side by side.",
        "Key Requirement: Tenant admins must opt in to cross-region data processing to enable the agentic experience.",
        "Core Capabilities: Multi-step agentic reasoning, visual + narrative responses, MCP Server for third-party AI assistants (Claude, ChatGPT), Discovery Agent for anomaly detection.",
        "Extended April 2026: Qlik Connect 2026 added the Predict, Automate, and Analytics Agents, turning Answers into a detect, investigate, predict, and act loop rather than a question-and-answer surface.",
        "Added July 2026: Qlik Predict inside Answers, the Answers Review Portal, Automate actions triggered from insights, and conversation PDF export.",
    ])

    # 1.2
    _add_section_title(pdf, "1.2 Latest Capability: Structured Data")
    _body(pdf, "Qlik Answers evolved from a document-only Q&A chatbot (2024) into a full agentic analytics platform that works across both structured application data and unstructured documents.")
    _body(pdf, "The agentic experience is delivered through Qlik Answers as the unified conversational interface, powered by:")
    _bullet(pdf, "Qlik Analytics Engine - performs governed, context-preserving calculations on structured app data")
    _bullet(pdf, "Specialized AI Agents - a 7-agent pipeline: Answers, Semantic Search, Data Analyst, Chart, Dashboard Authoring, Knowledge Base, and Help agents")
    _bullet(pdf, "RAG (Retrieval Augmented Generation) - retrieves relevant passages from curated knowledge bases")
    _bullet(pdf, "LLM Reasoning - synthesizes insights into rich narrative and visual responses with citations")
    pdf.ln(3)

    _add_subsection(pdf, "Key Components")
    _table(pdf, ["Component", "Description"], [
        ["Qlik Answers (Core)", "Unified conversational interface. Structured + unstructured data. Always-on side panel. Citations and reasoning explanations. Embeddable in external apps."],
        ["Discovery Agent", "Continuously monitors key measures using dynamic baselines. Surfaces anomalies and shifts. Proactive alerting. GA Feb 2026; 100,000+ discoveries surfaced for customers by April 2026."],
        ["MCP Server", "Exposes Qlik at engine, tool, and agent levels. 7+ supported AI assistants (Claude, ChatGPT, Copilot, Cursor, Gemini). Secure access to governed data. GA Feb 2026. Expanded through 2026 to run automations, data quality workflows, and pipeline introspection."],
        ["Help Agent", "Backed by Qlik product documentation. Answers platform navigation and how-to questions within the same chat interface. GA Feb 2026."],
    ], [40, 150])

    _add_subsection(pdf, "The Agent Roster (Expanded at Qlik Connect 2026)")
    _body(pdf, "At Qlik Connect 2026 (April 13-15, Kissimmee FL), Qlik extended Answers from a single conversational surface into a set of cooperating agents. Qlik describes the resulting flow as detect, investigate, predict, and act: an agent notices a shift, an analyst asks why, a model estimates what happens next, and a workflow does something about it, all inside one governed experience.")
    _table(pdf, ["Agent", "What It Does", "Status"], [
        ["Discovery Agent", "Continuous anomaly and shift detection against dynamic baselines. Insight cards retrievable via REST API (June 2026).", "GA Feb 2026"],
        ["Analytics Agent", "Query response and insight generation; assists with analytics development and creation workflows.", "Announced Apr 2026"],
        ["Predict Agent", "Forward-looking natural-language questions. Guides users through the full data science lifecycle: framing the problem, building and validating models, generating predictions.", "Available per Qlik, Jun 2026"],
        ["Automate Agent", "Executes workflows across Qlik and downstream systems from natural-language requests.", "Available per Qlik, Jun 2026"],
    ], [32, 108, 50])
    _body(pdf, "Status caveat: Qlik's own June 2026 announcement lists the Predict Agent and Automate Agent as 'available now.' Qlik has not published a separate GA date for the Analytics Agent, and independent commentary has described parts of the newer agent lineup as still maturing toward production. Confirm current availability for your tenant and region before designing around any specific agent.")

    _add_subsection(pdf, "Qlik Answers Enhancements (2026)")
    _body(pdf, "Available now:")
    _bullet(pdf, "Fast Mode (Jun 2026) - concise, low-latency responses for quick exploration and faster-paced workflows")
    _bullet(pdf, "Qlik Predict in Qlik Answers (Jul 2026) - describe a business problem in natural language and get a trained model or a prediction, with no data science background required")
    _bullet(pdf, "Answers Review Portal (Jul 2026) - tenant-wide review of conversations and feedback across agentic experiences from one location")
    _bullet(pdf, "Actions via Qlik Automate (Jul 2026) - trigger automations directly from agentic insights, on structured and unstructured data")
    _bullet(pdf, "Conversation PDF export (Jul 2026) - export new Answers conversations in both app and assistant contexts")
    pdf.ln(2)
    _body(pdf, "Coming soon (per Qlik, Jun 2026):")
    _bullet(pdf, "Multimodal input - Answers reads images, charts, and documents")
    _bullet(pdf, "Semantic customization - add definitions for fields and master items directly in the logical model")
    _bullet(pdf, "Advanced reasoning tools via MCP - pattern analysis, causality estimation, resource allocation optimization, risk scenario simulation, ML model deployment, and alternative scenario exploration")
    pdf.ln(3)

    # 1.3
    _add_section_title(pdf, "1.3 Requirements & Permissions")
    _body(pdf, "CRITICAL: Enabling Qlik Answers agentic experience is a tenant-wide change that replaces Insight Advisor and Insight Advisor Chat. This cannot be done per-app or per-user.")

    _add_subsection(pdf, "Step 1: Enable Cross-Region Data Processing")
    _body(pdf, "Path: Administration activity center > Settings > Tenant > AI features in Qlik\nAction: Toggle 'Enable cross-region data processing' to ON\nConfirmation: Check the authorization checkbox, then click Confirm > Submit")

    _add_subsection(pdf, "Step 2: Configure Permissions")
    _table(pdf, ["Permission", "Description", "Default", "Category"], [
        ["Data analysis", "Analyze data with Qlik Answers", "Not allowed", "Tenant-level"],
        ["Qlik product help", "Access docs via Qlik Answers", "Not allowed", "Tenant-level"],
        ["Qlik MCP server access", "Third-party AI via MCP", "Not allowed", "Tenant-level"],
        ["Manage assistants", "Create/manage assistants", "Not allowed", "Custom Role"],
        ["Manage knowledge bases", "Create/manage/index KBs", "Not allowed", "Custom Role"],
        ["Index knowledge bases", "Trigger KB indexing", "Not allowed", "Custom Role"],
        ["Search knowledge bases", "Access KBs for questions", "Not allowed", "Custom Role"],
    ], [35, 70, 30, 55])

    _add_subsection(pdf, "Step 3: Space-Level Access")
    _table(pdf, ["Space Type", "Space", "Required Permissions"], [
        ["Shared", "Assistant space", "Can view + Can consume data"],
        ["Shared", "Knowledge base space", "Can consume data"],
        ["Shared", "Data source spaces", "Can consume data"],
        ["Managed", "Assistant space", "Has restricted view + Can consume data"],
        ["Managed", "Knowledge base space", "Has restricted view + Can consume data"],
        ["Managed", "Data source spaces", "Can consume data"],
    ], [30, 50, 110])

    _add_subsection(pdf, "Regional Availability")
    _table(pdf, ["Region", "Agentic Experience"], [
        ["US East (N. Virginia)", "Yes"],
        ["Europe (Frankfurt)", "Yes"],
        ["Europe (Ireland)", "Yes"],
        ["Asia Pacific (Mumbai, Singapore, Sydney, Tokyo)", "Yes"],
        ["Europe (London)", "No (legacy only)"],
    ], [110, 80])

    _add_subsection(pdf, "Operational Limits")
    _table(pdf, ["Limit", "Value"], [
        ["Max file size", "50 MiB"],
        ["Concurrent documents per data source", "10"],
        ["Searches per minute per subscription", "50"],
        ["Assistant questions per minute", "20"],
        ["Monthly question quota", "Resets each month (does not carry over)"],
        ["Question capacity", "Varies by tier (Standard, Premium, Enterprise). Qlik Sense Enterprise SaaS baseline is 200 questions per month"],
        ["Indexed page size", "~2,000 characters of text data"],
    ], [80, 110])

    _add_subsection(pdf, "Scope and Behavior Constraints")
    _table(pdf, ["Constraint", "Detail"], [
        ["Query scope", "One Qlik Sense application per query. Multi-app querying is not in the current GA release."],
        ["Language", "Optimized and fully supported for English queries and responses."],
        ["Response time", "Qlik prioritizes answer quality over raw speed. Use Fast Mode (Jun 2026) when latency matters more than depth."],
        ["Required scopes", "App questions need Data analysis. Assistant questions need Data analysis plus Search knowledge base."],
        ["Mutual exclusivity", "Within a tenant you must choose Insight Advisor or Qlik Answers. They cannot run side by side."],
        ["Deployment", "Qlik Cloud only. There is no planned on-premises deployment."],
        ["Business logic", "Master measures and dimensions are always prioritized and existing business logic is applied automatically. Packages, Hierarchies, Behaviors, and Calendar periods are not carried over."],
    ], [45, 145])

    # 1.4
    _add_section_title(pdf, "1.4 Comparison: Structured vs Unstructured")
    _table(pdf, ["Aspect", "Previous (2024)", "Agentic (Feb 2026)"], [
        ["Data Sources", "Unstructured only (PDF, DOCX, TXT, HTML)", "Structured (Qlik apps) AND unstructured"],
        ["Architecture", "RAG only", "Agentic framework + RAG + Qlik Analytics Engine"],
        ["Analytics Engine", "None - document Q&A only", "Full Qlik Analytics Engine calculations"],
        ["Output Format", "Text answers with citations", "Rich narrative AND visual responses"],
        ["Reasoning", "Single-step document retrieval", "Multi-step agentic reasoning"],
        ["Cross-Region", "Optional (can stay in-region)", "Required (must opt in)"],
        ["MCP Integration", "Not available", "Qlik MCP Server for third-party AI"],
        ["Business Logic", "N/A", "Synonyms only (Packages, Hierarchies removed)"],
    ], [35, 75, 80])

    # 1.5
    _add_section_title(pdf, "1.5 Qlik Answers vs Insight Advisor")
    _body(pdf, "Qlik Answers REPLACES Insight Advisor in tenants where the agentic experience is enabled. Insight Advisor and Insight Advisor Chat options are hidden tenant-wide.")
    _table(pdf, ["Aspect", "Insight Advisor", "Qlik Answers (Agentic)"], [
        ["Scope", "Structured data within apps only", "Structured app data AND unstructured documents"],
        ["Interface", "Search + chat within apps", "Unified conversational agentic interface"],
        ["AI Architecture", "Augmented analytics with some GenAI", "Full agentic framework + LLM + Qlik Engine"],
        ["Business Logic", "Full support", "Synonyms only"],
        ["MCP / External", "Not available", "MCP Server for third-party assistants"],
        ["Status", "Being replaced", "Generally Available (Feb 2026)"],
    ], [30, 75, 85])

    _body(pdf, "Migration Warning: If you have existing analyses relying on business logic settings (Behaviors, Hierarchies, Calendar periods), you cannot modify these after enabling Qlik Answers. Plan your migration carefully.")

    _add_subsection(pdf, "Clarification: What 'Business Logic' Means")
    _body(pdf, "'Business logic' refers specifically to the Logical Model settings that govern Insight Advisor's behavior (found under App Edit > Logical Model > Business Logic). These include:")
    _table(pdf, ["Setting", "What It Controls"], [
        ["Behaviors", "Rules telling Insight Advisor how to treat fields (e.g., default aggregations, preferred dimensions)"],
        ["Hierarchies", "Logical drill-down groupings for Insight Advisor NL query interpretation"],
        ["Calendar periods", "Time-based analysis periods for Insight Advisor suggestions"],
        ["Packages", "Groups of related fields for Insight Advisor analysis"],
        ["Synonyms", "Alternative names for fields - the only setting carried over to Qlik Answers"],
    ], [40, 150])
    _body(pdf, "This does NOT affect regular app objects. Drill-down dimensions, master items, variables, expressions, and all other standard app-level objects are completely unaffected. The restriction applies only to the Insight Advisor-specific logical model configuration, which becomes frozen once Qlik Answers is enabled.")

    _add_subsection(pdf, "Embedding Qlik Answers")
    _body(pdf, "Qlik Answers can be embedded into external web applications using qlik-embed with OAuth M2M impersonation. The ai/assistant component type allows embedding the full conversational interface into any web app.")

    _add_subsection(pdf, "Monitoring: Qlik Cloud Answers Analyzer")
    _body(pdf, "The Answers Analyzer is a community-supported Qlik Sense monitoring app that provides operational analytics for Qlik Answers deployments.")
    _table(pdf, ["Capability", "Description"], [
        ["User Question Tracking", "Monitor what questions users are asking across knowledgebases and assistants"],
        ["Behavioral Analysis", "Analyze question types and content usage patterns"],
        ["Knowledgebase Optimization", "Identify inaccurate, unused, and unreferenced documents"],
        ["Quota Monitoring", "Track knowledgebase page sizes relative to quotas"],
        ["Index Freshness", "Monitor how recently knowledgebases have been re-indexed"],
        ["Alerting", "Set alerts on metrics (e.g., stale knowledgebases)"],
    ], [50, 140])
    _body(pdf, "Requires: TenantAdmin + AuditAdmin roles. Part of the Qlik Cloud Monitoring Apps suite.")

    _links_section(pdf, "Sources & References", [
        ("Qlik GA Press Release (Feb 2026)", "https://www.businesswire.com/news/home/20260210837577/en/Qlik-Brings-Agentic-Analytics-to-General-Availability-and-Launches-MCP-Server-for-Third-Party-Assistants"),
        ("Qlik Answers - Qlik Cloud Help", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/Qlik-Answers.htm"),
        ("Qlik Agentic AI Vision Blog", "https://www.qlik.com/blog/a-vision-for-the-future-qliks-new-agentic-ai-experience"),
        ("Enabling Cross-Region Data Processing", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Admin/cross-region-data-processing.htm"),
        ("Qlik Answers Access and Permissions", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/qlik-answers-permissions.htm"),
        ("Deploying and Administering Qlik Answers", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/administering-qlik-answers.htm"),
        ("Qlik Answers Product Page", "https://www.qlik.com/us/products/qlik-answers"),
        ("Qlik MCP Community Video", "https://community.qlik.com/t5/Integration-Extension-APIs/Qlik-Cloud-Development-with-Claude-Desktop-and-MCP-Servers-Video/td-p/2535891"),
        ("Embedding Qlik Answers (GitHub)", "https://github.com/qlik-oss/qlik-cloud-embed-oauth-impersonation"),
        ("Qlik Cloud Answers Analyzer (GitHub)", "https://github.com/qlik-oss/qlik-cloud-answers-analyzer"),
    ])


def _build_part2(pdf: _QlikPDF):
    _add_part_title(pdf, "Part 2: Qlik Predict - Automated Machine Learning")

    # 2.1
    _add_section_title(pdf, "2.1 Executive Summary")
    _exec_box(pdf, "Executive Summary - Qlik Predict", [
        "What: Qlik Predict (formerly Qlik AutoML) is a no-code automated machine learning platform embedded in Qlik Cloud Analytics.",
        "Capabilities: Binary/multiclass classification, regression, and multivariate time series forecasting (GA Oct 2025) with GPU-accelerated deep learning.",
        "Explainability: Built-in SHAP-based explainability shows which features drive predictions at both global and row levels.",
        "Deployment: Three methods: batch predictions, real-time API, and the Qlik Predict analytics connector for in-app integration.",
        "Natural Language (2026): The Predict Agent and Qlik Predict inside Qlik Answers let a business user describe a problem in plain language and receive a trained model or a prediction, with no data science background required.",
        "HR Applications: Ideal for predicting employee turnover, promotions, lateral movements, absenteeism, compensation equity, and workforce demand forecasting.",
    ])

    # 2.2
    _add_section_title(pdf, "2.2 How Qlik Predict Works")
    _body(pdf, "Qlik Predict follows a six-step automated workflow:\n1. Data Loading & Profiling - Upload CSV, QVD, XLSX\n2. Experiment Creation - Select target column, auto-detect problem type\n3. Automated Model Training - Multiple algorithms, intelligent optimization\n4. Model Evaluation & Scoring - SHAP explainability, feature importance\n5. Deployment - Model approval, versioning, swapping\n6. Prediction & Visualization - Batch, real-time API, analytics connector")

    _add_subsection(pdf, "Key Constraints")
    _bullet(pdf, "Max 500 columns per dataset")
    _bullet(pdf, "API rate limit: 300 requests/minute")
    _bullet(pdf, "Dataset size: up to 2 GiB (CSV/Parquet/QVD) or 100M-500M cells; analytics connector batched in 2,000-row chunks")
    _bullet(pdf, "API change (Feb 2026): Legacy AutoML real-time API removed; use new Machine Learning API /api/v1/ml/deployments/{id}/realtime-predictions/actions/run")
    _bullet(pdf, "Not available on Qlik Cloud Government or Qlik Cloud Government - DoD")
    _bullet(pdf, "Available in Premium and Enterprise tiers")
    pdf.ln(3)

    _add_subsection(pdf, "Responsible AI / Bias Detection (GA Feb 2026)")
    _body(pdf, "Model training surfaces bias signals including imbalanced feature groups and proxy features, which helps detect and mitigate bias before deployment. Not available in Qlik Cloud Government.")

    _add_subsection(pdf, "Natural-Language Prediction (2026)")
    _body(pdf, "Through 2026 Qlik added a conversational path into Predict, so that building a model no longer requires starting in the ML experiment UI.")
    _table(pdf, ["Capability", "Detail"], [
        ["Predict Agent", "Announced at Qlik Connect 2026 and described by Qlik as available as of June 2026. Generates predictions from plain-language questions and guides the user through the full data science lifecycle: understanding and framing the business problem, building and validating candidate models, then generating and explaining predictions. Qlik positions this as bringing predictive signals, explainable reasoning, and workflow action together."],
        ["Qlik Predict in Qlik Answers", "Released July 2026. A natural-language interface to predictive modeling inside the Answers experience. A user describes a business problem in conversation and receives a trained model or a direct insight back, without leaving the assistant. Paired with the Automate Agent, a prediction can flow straight into a downstream action."],
    ], [45, 145])
    _body(pdf, "Governance note for people analytics: natural-language model building lowers the barrier to creating models over HR data, which also lowers the barrier to creating an unreviewed one. Pair it with the Responsible AI bias signals above, and keep an approval step between a generated model and any decision that affects an individual.")

    # 2.3
    _add_section_title(pdf, "2.3 ML Algorithms & Models")

    _add_subsection(pdf, "Classification Algorithms (Binary & Multiclass)")
    _table(pdf, ["Algorithm", "Category", "Strengths"], [
        ["Logistic Regression", "Linear", "Good at extrapolating, interpretable"],
        ["Lasso Regression", "Linear", "Feature selection via L1 regularization"],
        ["Elastic Net Regression", "Linear", "Combines L1 + L2 regularization"],
        ["Gaussian Naive Bayes", "Probabilistic", "Handles non-linear patterns"],
        ["Random Forest", "Ensemble", "Non-linear trends, variable interactions"],
        ["XGBoost", "Ensemble", "Strong non-linear pattern recognition"],
        ["LightGBM", "Ensemble", "Fast training on large datasets"],
        ["CatBoost", "Ensemble", "Native categorical feature handling"],
    ], [50, 30, 110])

    _add_subsection(pdf, "Regression Algorithms")
    _table(pdf, ["Algorithm", "Category", "Strengths"], [
        ["Linear Regression", "Linear", "Extrapolation, linear trends"],
        ["SGD Regression", "Linear", "Scalable to large datasets"],
        ["Random Forest", "Ensemble", "Non-linear trend detection"],
        ["XGBoost", "Ensemble", "High accuracy for complex patterns"],
        ["LightGBM", "Ensemble", "Fast, memory-efficient"],
        ["CatBoost", "Ensemble", "Native categorical feature handling"],
    ], [50, 30, 110])

    _add_subsection(pdf, "Time Series Algorithms (Deep Learning, GPU)")
    _table(pdf, ["Algorithm", "Type", "Best For"], [
        ["DeepAR", "Deep learning / probabilistic", "Retail, supply chain; probabilistic forecasting"],
        ["TSMixer", "Transformer-inspired", "Balances accuracy and speed"],
        ["TiDE", "Deep learning encoder", "Long-term dependencies in large datasets"],
    ], [40, 55, 95])

    # 2.4
    _add_section_title(pdf, "2.4 HR Use Cases")

    _add_subsection(pdf, "Employee Turnover / Attrition Prediction")
    _body(pdf, "Problem Type: Binary Classification (Stayed vs. Left)")
    _table(pdf, ["Feature Category", "Example Fields"], [
        ["Demographics", "Tenure, commute distance, education level"],
        ["Job Details", "Department, role, job level, years in current role"],
        ["Performance", "Performance rating (last 3 years), project outcomes"],
        ["Engagement", "Engagement survey scores, satisfaction index, eNPS"],
        ["Compensation", "Base salary, bonus %, last raise %, salary band position"],
        ["Work Patterns", "Overtime hours, remote work frequency, PTO usage"],
        ["Development", "Training completions, certifications, mentoring participation"],
        ["Manager", "Manager tenure, span of control, manager change count"],
    ], [40, 150])

    _add_subsection(pdf, "Promotion Prediction")
    _body(pdf, "Problem Type: Binary Classification (Promoted vs. Not) or Multiclass (Promotion Level)\nKey features: performance ratings over time, training completion, tenure in role, project outcomes, 360-degree feedback, education, certifications.")

    _add_subsection(pdf, "Lateral Movement Prediction")
    _body(pdf, "Problem Type: Multiclass Classification or Regression\nUse historical data with Markov-style transitions to predict movement patterns. Key features: role tenure, skill breadth, cross-functional projects, career interests, internal application history.")

    # 2.5
    _add_section_title(pdf, "2.5 People Analytics Ideation")
    use_cases = [
        ("Flight Risk Scoring (60-90 day)", "Binary Classification"),
        ("Absenteeism Prediction", "Regression / Classification"),
        ("Employee Engagement Forecasting", "Regression"),
        ("Recruitment Success Prediction", "Binary Classification"),
        ("Time-to-Hire Forecasting", "Time Series (MVTS)"),
        ("Compensation Equity Analysis", "Regression"),
        ("Training ROI Prediction", "Regression"),
        ("Workforce Demand Forecasting", "Time Series (MVTS)"),
        ("Succession Planning", "Classification"),
        ("Internal Mobility Optimization", "Multiclass Classification"),
        ("New Hire Onboarding Success", "Binary Classification"),
        ("Benefits Utilization Prediction", "Regression"),
        ("Team Performance Forecasting", "Regression"),
    ]
    _table(pdf, ["Use Case", "Problem Type"],
           [[uc[0], uc[1]] for uc in use_cases], [100, 90])

    _links_section(pdf, "Sources & References", [
        ("Qlik Predict Tutorial", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/tutorial-machine-learning.htm"),
        ("Request a Qlik Predict Demo", "https://www.qlik.com/us/contact-us/demo-request-predict"),
        ("Tech Field Day Demo Video (June 2024)", "https://techfieldday.com/video/qlik-self-service-ai-demo/"),
        ("Community Sample Data", "https://community.qlik.com/t5/Qlik-Predict/Qlik-AutoML-on-Qlik-Cloud-sample-data/td-p/1966212"),
        ("Multivariate Time Series Blog", "https://www.datavoyagers.net/post/beyond-the-event-horizon-multivariate-time-series-with-qlik-predict"),
        ("Real-Time Predictions Guide", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/creating-real-time-predictions.htm"),
    ])


def _build_part3(pdf: _QlikPDF):
    _add_part_title(pdf, "Part 3: Application Automations & External LLM Integration")

    # 3.1
    _add_section_title(pdf, "3.1 Executive Summary")
    _exec_box(pdf, "Executive Summary - Application Automations & External LLMs", [
        "What: Qlik Application Automations (Qlik Automate) is a no-code workflow automation platform built into Qlik Cloud.",
        "LLM Connectors: Native OpenAI connector + generic API Key connector (for any LLM) + 9+ native analytic connections (incl. Google AI Gemini added July 2025).",
        "Dynamic Updates: Analytic connections in chart expressions respond to user selections in real-time.",
        "Embedding: Two patterns: button-triggered automations (workflow) and analytic connection chart expressions (inline AI).",
        "Agent-Triggered (2026): Automations can now be launched from an AI assistant through the Qlik MCP server, and directly from Qlik Answers insights via the Automate Agent. The automation becomes a tool the agent can call rather than a button a person clicks.",
        "Fallback Strategy: When Qlik Answers is insufficient, external LLMs provide free-form narratives, sentiment analysis, and custom reasoning.",
    ])

    # 3.2
    _add_section_title(pdf, "3.2 Application Automations Overview")
    _body(pdf, "Qlik Application Automations are a no-code workflow automation platform (iPaaS) built into Qlik Cloud. Users build automated workflows between Qlik Cloud and external SaaS applications without writing code.")
    _bullet(pdf, "Visual drag-and-drop builder with data and logic blocks")
    _bullet(pdf, "On-demand triggers (manual or from Qlik Sense buttons)")
    _bullet(pdf, "Webhook triggers from external events (up to 4 hours runtime as of March 2026)")
    _bullet(pdf, "Scheduled automations at specific times")
    _bullet(pdf, "Pre-built connectors: Salesforce, Teams, Slack, GitHub, ServiceNow, OpenAI, Hugging Face, etc.")
    pdf.ln(3)

    _add_subsection(pdf, "Automations as Agent Tools (2026)")
    _body(pdf, "The most consequential 2026 change to Qlik Automate is not a new block. It is that an automation is now something an AI agent can discover and call, not only something a person triggers.")
    _table(pdf, ["Capability", "What It Enables", "Availability"], [
        ["Run automations from an AI assistant (MCP)", "Qlik documents dedicated MCP tools for the full run lifecycle: qlik_list_automation_runs, qlik_get_automation_inputs, qlik_start_automation_run, qlik_start_automation_run_interactive, qlik_update_automation_run_input (answer a run waiting for input), qlik_fetch_automation_run, and qlik_get_automation_run_display. Create, update, and delete tools exist as well.", "2026"],
        ["Actions via Qlik Automate in Answers", "Qlik Answers triggers automations directly from agentic insights, on both structured and unstructured data.", "Jul 2026"],
        ["Automate Agent", "Executes workflows across Qlik and downstream systems from a natural-language request.", "Available per Qlik, Jun 2026"],
        ["AI-generated automation descriptions", "A button generates a description of an automation from its workspace structure, so both people and AI agents can find the right one.", "Jul 2026"],
    ], [42, 105, 43])
    _body(pdf, "Why the descriptions matter more than they look: an agent picks a tool by reading its description. An automation named Automation_17 with an empty description is effectively invisible to the Automate Agent and to any MCP client. Populating descriptions is the practical prerequisite for agent-triggered workflows, not a documentation nicety.")

    _add_subsection(pdf, "Automation APIs (2026)")
    _table(pdf, ["API", "Purpose", "Date"], [
        ["Workflows namespace APIs", "Automations API, Automation Connections API, and Automation Connectors API, replacing the legacy v1 equivalents.", "Apr 10, 2026"],
        ["AI MCP system events", "com.qlik.ai.mcp.tool.calls.aggregated and com.qlik.ai.mcp.tool.executed for analyzing tool usage patterns and monitoring performance.", "Apr 23, 2026"],
        ["Connector details endpoint", "GET /workflows/automation-connectors/{connectorId} returns connector information and available blocks programmatically.", "Jul 22, 2026"],
        ["Webhook configuration endpoint", "GET /workflows/automation-connectors/{connectorId}/webhooks/configuration discovers which webhook events a connector supports.", "Jul 22, 2026"],
    ], [42, 118, 30])

    # 3.3
    _add_section_title(pdf, "3.3 Integrating External LLMs")

    _add_subsection(pdf, "Native OpenAI Connector (Application Automation)")
    _table(pdf, ["Block", "Purpose"], [
        ["List Models", "Returns available OpenAI models"],
        ["Retrieve Model", "Returns details about a specific model"],
        ["Create Completion", "Generates text using a specified model"],
        ["Raw API Request", "Full control - any OpenAI endpoint"],
        ["Raw API List Request", "GET request returning iterable results"],
    ], [50, 140])

    _add_subsection(pdf, "API Key Connector (Generic REST - Any LLM)")
    _body(pdf, "For LLMs without a dedicated connector (Google Gemini, Cohere, custom endpoints). Configure Base URL, HTTP Method, Headers, Request Body, and Query Parameters to call any REST API.")

    _add_subsection(pdf, "Analytic Connections (Native In-App Connectors)")
    _table(pdf, ["Connector", "LLM Provider", "Auth Method"], [
        ["OpenAI", "GPT models", "API key"],
        ["Azure OpenAI", "GPT via Azure", "Azure API key + endpoint"],
        ["Anthropic (Amazon Bedrock)", "Claude models", "AWS Access Key + Secret"],
        ["Amazon Bedrock - Converse API", "All Bedrock models", "AWS credentials"],
        ["Amazon Titan (Bedrock)", "Titan models", "AWS credentials"],
        ["Cohere (Amazon Bedrock)", "Cohere models", "AWS credentials"],
        ["Meta (Amazon Bedrock)", "Llama models", "AWS credentials"],
        ["Hugging Face", "Open-source models", "HF API key"],
        ["Google AI - Gemini", "Gemini models (added Jul 2025)", "Google AI Studio API key"],
    ], [60, 65, 65])

    # 3.4
    _add_section_title(pdf, "3.4 Analytic Connections - Dynamic Updates")
    _body(pdf, "When used in chart expressions, analytic connections respond dynamically to user selections:\n1. User makes a selection in Qlik Sense app\n2. Associative engine recalculates all expressions\n3. SSE expression sends filtered data to external LLM\n4. LLM response is returned and displayed in Text & Image object\n5. User changes selection - entire flow repeats automatically")

    _add_subsection(pdf, "Key Constraints")
    _bullet(pdf, "Max 25 rows per request, batch size of 1 row")
    _bullet(pdf, "Use only in Text & Image chart objects (not Tables)")
    _bullet(pdf, "Gate LLM calls with if(count(distinct [Field]) = 1, ...) to control costs")
    _bullet(pdf, "For Anthropic (Messages API via Bedrock), no special prompt syntax needed")
    pdf.ln(3)

    # 3.5
    _add_section_title(pdf, "3.5 Fallback Architecture")
    _body(pdf, "When Qlik Answers' structured data capabilities are insufficient, external LLM integration provides a fallback:")
    _table(pdf, ["Limitation of Qlik Answers", "Fallback via External LLM"], [
        ["Cannot generate free-form text narratives", "Use OpenAI/Claude expressions for summaries"],
        ["Cannot analyze unstructured text", "Send text to LLM for sentiment/classification"],
        ["Cannot perform cross-domain reasoning", "External LLMs combine data with general knowledge"],
        ["Limited question patterns", "External LLMs handle open-ended prompts"],
        ["No custom model fine-tuning", "Connect to fine-tuned models on HuggingFace"],
        ["Cannot generate code dynamically", "Use LLM to generate Qlik expressions"],
    ], [80, 110])

    _add_subsection(pdf, "Integration Method Summary")
    _table(pdf, ["Method", "Providers", "Trigger", "Best For"], [
        ["Analytic Connection (Chart)", "OpenAI, Azure, Bedrock, HF", "User selection", "Real-time inline AI"],
        ["Analytic Connection (Load)", "Same", "Data reload", "Batch pre-computation"],
        ["Automation (OpenAI)", "OpenAI", "Button/webhook/schedule", "Multi-step workflows"],
        ["Automation (API Key)", "Any REST API", "Button/webhook/schedule", "Any LLM via HTTP"],
        ["Qlik MCP Server", "Claude, ChatGPT, custom", "External AI initiates", "Exposing Qlik to AI"],
    ], [45, 50, 45, 50])

    _links_section(pdf, "Sources & References", [
        ("Interactive OpenAI Example App", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/LoadData/ac-openai-tutorial-example-interactive.htm"),
        ("OpenAI Analytics Connector Tutorial", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/LoadData/ac-openai-tutorial.htm"),
        ("Anthropic (Bedrock) Connection Guide", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/LoadData/ac-bedrock-anthropic-use.htm"),
        ("Application Automation Overview Video", "https://help.qlik.com/en-US/video/GBvy1WtF2B9Akf1e564dtv"),
        ("Automation Trigger Extension (GitHub)", "https://github.com/rileymd88/automation-trigger"),
    ])


def _build_part4(pdf: _QlikPDF):
    _add_part_title(pdf, "Part 4: Qlik Cloud AI/ML Ecosystem")

    # 4.1
    _add_section_title(pdf, "4.1 Executive Summary")
    _exec_box(pdf, "Executive Summary - Qlik Cloud AI/ML Ecosystem", [
        "Platform: Qlik's AI strategy is branded under Qlik Staige - spanning data integration, analytics, and AI.",
        "GA Features (2025-2026): Qlik Answers, Qlik Predict, MCP Server, 9+ LLM connectors (incl. Google AI Gemini), Automations, Discovery Agent, Data Products for Analytics, Agentic Data Engineering (GA July 2026), Bias Detection.",
        "Added in 2026: Predict, Automate, and Analytics Agents (Qlik Connect, April 2026), Semantic Layer for Data Products, Answers Fast Mode, Answers Review Portal, and Qlik Predict inside Qlik Answers.",
        "Coming Soon: Multimodal Answers input, semantic customization in the logical model, advanced reasoning tools via MCP, and additional Trust Score dimensions (Security, LLM Readiness).",
        "Key Differentiator: AI grounded in the Qlik Associative Engine - governed calculations, not hallucinated responses.",
        "Cloud Only: All features are Qlik Cloud (SaaS) - not available in Qlik Sense Enterprise on Windows.",
    ])

    # 4.2
    _add_section_title(pdf, "4.2 Current AI/ML Features")
    _table(pdf, ["Feature", "Status", "Description"], [
        ["Qlik Answers (Agentic)", "GA (Feb 2026)", "Unified conversational AI, structured + unstructured data"],
        ["Qlik Predict (AutoML)", "GA", "No-code ML: classification, regression, time series"],
        ["Multivariate Time Series", "GA (Oct 2025)", "GPU deep learning: DeepAR, TSMixer, TiDE"],
        ["Qlik MCP Server", "GA (Feb 2026)", "Third-party AI assistants access governed Qlik data"],
        ["Analytic Connections", "GA", "9+ native LLM connectors incl. Google AI Gemini (Jul 2025)"],
        ["Application Automations", "GA", "No-code workflows with OpenAI + API Key connectors"],
        ["Insight Advisor", "GA (being replaced)", "NL search + chat, full business logic"],
        ["AI-Generated Narratives", "GA", "Auto-generated NL summaries of charts"],
        ["Key Driver Analysis", "GA", "Automated key driver identification"],
        ["Anomaly Detection", "GA", "Outlier detection in time series"],
        ["NLP Engine", "GA", "Powers NL understanding in Insight Advisor/Answers"],
        ["Write Table (Writeback)", "GA (Oct 2025)", "Native writeback in Qlik Sense apps"],
        ["Qlik Trust Score for AI", "GA (Jul 2025)", "Data readiness scoring for AI"],
        ["Knowledge Mart Tasks", "GA", "Vector store automation for RAG/GenAI"],
        ["NL Expression Generator", "GA", "Natural language to Qlik expressions"],
        ["AI Script Generation", "GA", "NL to Qlik load scripts"],
        ["Table Recipe", "GA", "No-code data preparation (60+ functions)"],
        ["Qlik Open Lakehouse", "GA (Oct 2025)", "Iceberg-powered lakehouse on AWS"],
        ["Responsible AI / Bias Detection", "GA (Feb 2026)", "Bias signals (imbalanced groups, proxy features) surfaced during model training in Qlik Predict"],
        ["Data Products for Analytics", "GA (Feb-Mar 2026)", "Curated governed datasets with Trust Scores and quality indicators in Qlik apps. Extended at Qlik Connect 2026 with a Semantic Layer carrying shared business definitions for measures, dimensions, and relationships."],
        ["Discovery Agent", "GA (Feb 2026)", "Continuous anomaly monitoring via dynamic baselines; proactive alerts to user feeds. 100,000+ discoveries surfaced for customers by April 2026. Insight cards retrievable via REST API (Jun 2026)."],
        ["Predict Agent", "Available per Qlik (Jun 2026)", "Forward-looking natural-language questions; guides the user through framing, model building and validation, then prediction. Announced at Qlik Connect 2026."],
        ["Automate Agent", "Available per Qlik (Jun 2026)", "Executes actions and workflows across Qlik and downstream systems from natural-language requests."],
        ["Analytics Agent", "Announced (Apr 2026)", "Query response and insight generation; supports analytics development and creation workflows. No separate GA date published."],
        ["Qlik Answers Fast Mode", "Available (Jun 2026)", "Concise, low-latency responses for quick exploration, trading depth for speed."],
        ["Qlik Predict in Qlik Answers", "GA (Jul 2026)", "Natural-language interface to predictive modeling inside the Answers experience."],
        ["Answers Review Portal", "GA (Jul 2026)", "Tenant-wide review of conversations and feedback across agentic experiences from one location."],
        ["Answers Conversation PDF Export", "GA (Jul 2026)", "Exports Answers conversations to PDF in both app and assistant contexts."],
        ["Agentic Data Engineering", "GA (Jul 2026)", "Purpose-built agents across data quality, data products, catalog glossary, declarative pipelines, and MCP-enabled tools."],
        ["Data Quality Agents", "GA (Jul 2026)", "Trust scores, quality rules, SLOs, and anomaly detection via natural language or MCP workflows."],
        ["Declarative Pipelines (YAML)", "GA (Jun-Jul 2026)", "YAML pipeline definition with published schemas, validation, and GitOps support; agents generate schema-valid YAML."],
    ], [50, 35, 105])

    # 4.3
    _add_section_title(pdf, "4.3 Planned / Upcoming Features")
    _body(pdf, "Based on Qlik's announcements and roadmap communications as of September 2026.")
    _table(pdf, ["Feature", "Status", "Description"], [
        ["Multimodal Qlik Answers", "Coming soon (per Qlik, Jun 2026)", "Qlik Answers reads images, charts, and documents as input, not only text and structured fields."],
        ["Semantic Customization", "Coming soon (per Qlik, Jun 2026)", "Add definitions for fields and master items directly within the logical model, so the agent inherits the business vocabulary instead of guessing at it."],
        ["Advanced Reasoning Tools (MCP)", "Coming soon (per Qlik, Jun 2026)", "Pattern analysis, causality estimation, resource allocation optimization, risk scenario simulation, ML model deployment, and alternative scenario exploration from an MCP client."],
        ["Analytics Agent (general availability)", "Announced Apr 2026, GA date not published", "Query response, insight generation, and analytics development assistance."],
        ["Trust Score: Security + LLM Readiness", "Planned", "Additional dimensions beyond Diversity, Timeliness, Accuracy, Discoverability, and Usage."],
        ["Governed Writeback (SAP, SF, Snowflake)", "Planned", "Native writeback to enterprise systems."],
        ["AWS European Sovereign Cloud", "In progress", "$1.5B European investment over 5 years. Reinforced by the AI Sovereignty Initiative announced at Qlik Connect 2026."],
        ["GenAI Insight Advisor Narratives", "Private Preview", "ChatGPT-like answers via Amazon Bedrock. Insight Advisor itself is being superseded by Qlik Answers."],
    ], [55, 45, 90])
    _body(pdf, "Shipped since the March 2026 edition of this document: the Discovery Agent and Data Products for Analytics reached GA, the Predict and Automate Agents became available, Agentic Data Quality and Stewardship capabilities shipped inside Agentic Data Engineering (GA July 2026), and MCP support expanded to cover automations, data quality workflows, and pipeline introspection. They are documented in section 4.2 rather than here.")
    _body(pdf, "Status language follows Qlik's own published wording. Where Qlik describes something as 'available now' without a formal GA date, that phrasing is preserved rather than upgraded to GA.")

    _add_subsection(pdf, "Strategic Partnerships & Recognition")
    _table(pdf, ["Achievement", "Details"], [
        ["AWS Generative AI Competency", "Technical proficiency in Amazon Bedrock and SageMaker"],
        ["Gartner MQ: Analytics & BI", "Leader for the 16th consecutive year (June 2026)"],
        ["Gartner MQ: Data Quality Solutions", "Leader for 6th time (2025)"],
        ["Gartner MQ: Augmented Data Quality Solutions", "Leader for 7th time (Feb 2026) - cited Trust Score for AI, RAG support"],
        ["ISO/IEC 42001:2023 Certification", "AI management system certification, highlighted at Qlik Connect 2026"],
        ["AI Sovereignty Initiative", "Announced at Qlik Connect 2026, covering regional cloud expansion and sovereign deployment options"],
        ["Canada Cloud Region", "Announced Sep 2025; onboarding 2026. Data residency + AI sovereignty for Canadian customers."],
        ["Qlik Cloud Government - DoD", "Launched Feb 18, 2026 on AWS Marketplace for JWCC customers."],
        ["Qlik AI Specialist Certification", "Covers AI concepts, Qlik Predict, GenAI assistants"],
        ["Qlik Connect 2026", "April 13-15, Gaylord Palms, Kissimmee FL. Announced the Predict, Automate, and Analytics Agents, the Semantic Layer for Data Products, Open Lakehouse native streaming, and the AI Sovereignty Initiative."],
    ], [60, 130])

    # 4.4
    _add_section_title(pdf, "4.4 Qlik Staige Platform")
    _body(pdf, "Qlik Staige is Qlik's unified platform brand for AI capabilities across the data lifecycle. Key principles:")
    _bullet(pdf, "Grounded in Governed Data - calculations powered by Qlik Associative Engine, not hallucinated")
    _bullet(pdf, "Transparent Reasoning - citations and explanations of how conclusions were reached")
    _bullet(pdf, "No Data Science Required - AutoML for analytics teams without coding expertise")
    _bullet(pdf, "Open Ecosystem - MCP Server and Analytic Connections for broad AI integration")
    _bullet(pdf, "Embedded, Not Bolted On - AI in side panels, chart expressions, and automations")
    pdf.ln(3)

    _add_subsection(pdf, "AI Governance Framework")
    _table(pdf, ["Governance Layer", "Mechanism"], [
        ["Governed Calculations", "All answers powered by Qlik Associative Engine"],
        ["Citations & Explainability", "Every AI answer traces to original sources"],
        ["SHAP Model Explainability", "Feature importance at global and individual levels"],
        ["Data Lineage & Provenance", "Full tracking of transformations and origins"],
        ["Trust Score for AI", "Data readiness scoring (Diversity, Timeliness, Accuracy)"],
        ["Role-Based Access Controls", "Granular permissions on AI features and data products"],
        ["Global AI Council", "External experts guiding responsible AI (formed Jan 2024)"],
        ["Enterprise MLOps", "Version control, monitoring, retraining, lifecycle management"],
    ], [55, 135])

    _links_section(pdf, "Sources & References", [
        ("Qlik Trust Score for AI", "https://www.qlik.com/us/news/company/press-room/press-releases/qlik-releases-trust-score-for-ai-in-qlik-talend-cloud"),
        ("Knowledge Mart Help", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/DataIntegration/KnowledgeMart/Creating-knowledge-marts.htm"),
        ("Qlik Open Lakehouse", "https://community.qlik.com/t5/Release-Notes/Qlik-Cloud-Release-Notes-October-2025/ta-p/2532869"),
        ("Qlik Announces Qlik Staige", "https://www.qlik.com/us/news/company/press-room/press-releases/qlik-announces-qlik-staige"),
        ("AWS Generative AI Competency", "https://www.qlik.com/us/news/company/press-room/press-releases/qlik-achieves-aws-generative-ai-competency"),
        ("Qlik AI Specialist Certification", "https://learning.qlik.com/student/page/2537679-qlik-ai-specialist-certification-exam"),
        ("Qlik Brings Agentic Analytics to GA", "https://www.businesswire.com/news/home/20260210837577/en/Qlik-Brings-Agentic-Analytics-to-General-Availability-and-Launches-MCP-Server-for-Third-Party-Assistants"),
        ("Qlik Agentic AI", "https://www.qlik.com/us/agentic-ai"),
        ("Qlik Cloud Analytics", "https://www.qlik.com/us/products/qlik-cloud-analytics"),
        ("Qlik Augmented Analytics", "https://www.qlik.com/us/products/qlik-augmented-analytics"),
        ("Qlik Predict", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/AutoML/home-automl.htm"),
        ("Qlik MCP Server", "https://www.qlik.com/us/products/model-context-protocol"),
        ("Qlik Why AI", "https://www.qlik.com/us/why-qlik-for-ai"),
    ])

    # 4.5
    _add_section_title(pdf, "4.5 Open-Source Tools & Developer Resources")
    _body(pdf, "Qlik maintains an active open-source presence through the qlik-oss GitHub organization (~130+ repositories), providing developer SDKs, monitoring apps, embedding examples, and extensibility tools for Qlik Cloud.")

    _add_subsection(pdf, "Qlik Cloud Monitoring Apps")
    _body(pdf, "Community-supported Qlik Sense applications for operational and usage analytics. Installed via Qlik Automate workflows or manual .qvf import.")
    _table(pdf, ["App", "Description", "Multi-Tenant"], [
        ["App Analyzer", "Analyzes and monitors Qlik Sense applications", "Yes"],
        ["Reload Analyzer", "Tracks reload tasks, durations, and failures", "Yes"],
        ["Automation Analyzer", "Analyzes Qlik Automate automation runs", "No"],
        ["Answers Analyzer", "Monitors Qlik Answers usage and accuracy", "No"],
        ["Access Evaluator", "Analyzes user roles, access, permissions", "No"],
        ["Entitlement Analyzer", "Tracks license/entitlement usage", "Yes"],
        ["Report Analyzer", "Analyzes metered report metadata", "No"],
        ["OEM Dashboard", "Multi-tenant estate overview", "Multi only"],
    ], [45, 110, 35])

    _add_subsection(pdf, "Developer SDKs & CLI Tools")
    _table(pdf, ["Tool", "Language", "Description"], [
        ["@qlik/api", "TypeScript", "Full Qlik Cloud REST API + QIX Engine client"],
        ["enigma.js", "JavaScript", "WebSocket library for Qlik Associative Engine"],
        ["enigma-go", "Go", "Go client for the Qlik Associative Engine"],
        ["qlik-cli", "CLI", "Command-line access to all Qlik Cloud APIs"],
        ["nebula.js", "JavaScript", "Product-agnostic visualization APIs"],
        ["halyard.js", "JavaScript", "Programmatic Qlik Load Script generation"],
        ["picasso.js", "JavaScript", "Charting library for interactive visualizations"],
    ], [35, 30, 125])

    _add_subsection(pdf, "MCP Registry & Native MCP Endpoint")
    _body(pdf, "Qlik maintains an MCP Registry listing MCP servers for AI-assisted development workflows. Qlik Cloud exposes a native MCP endpoint at /api/ai/mcp using streamable-http transport, enabling external AI assistants to interact directly with governed analytics data.")
    _bullet(pdf, "Qlik Cloud MCP Server - native analytics access for third-party AI")
    _bullet(pdf, "Qlik Design System (Sprout) - AI-assisted code generation with Qlik design tokens")
    _bullet(pdf, "Qlik R&D Knowledge Base - developer documentation for AI-assisted use cases")
    pdf.ln(3)

    _add_subsection(pdf, "MCP Capability Expansion (2026)")
    _table(pdf, ["Added", "Capability"], [
        ["2026", "Run automations from an assistant: documented tools cover listing runs, reading required inputs, starting a run, starting an interactive run, submitting inputs to a run that is waiting, fetching run state, and retrieving run display output. No tool for stopping a run is documented."],
        ["Jul 2026", "Data quality workflows: retrieve trust scores, define and refine quality rules, and work with quality metrics through natural language or MCP."],
        ["Sep 7, 2026", "Declarative pipeline tools: qlik_search, qlik_get_pipeline_project_details, and qlik_search_connection_objects, letting coding agents such as Claude Code or GitHub Copilot query a live Qlik tenant from the editor and introspect connection names, table structures, and project bindings."],
    ], [30, 160])
    _body(pdf, "Client registration: Anthropic's Claude Desktop uses a predefined static client ID, so no administrator setup is required beyond initial approval. OAuth Dynamic Client Registration (DCR) lets an LLM client register itself: the client presents its metadata to a Qlik DCR endpoint and receives a client ID back.")

    _add_subsection(pdf, "Embedding & Extensibility")
    _table(pdf, ["Resource", "Description"], [
        ["qlik-embed OAuth Impersonation", "Embed Qlik Sense and Qlik Answers (ai/assistant) in external apps"],
        ["Embedded Analytics Workshop", "Self-directed workshop for embedding Qlik Cloud visualizations"],
        ["Server-Side Extensions (SSE)", "gRPC protocol for extending Qlik expressions with Python, R, C++, Java, Go"],
        ["SSE R Plugin", "R integration for statistical and ML computations in Qlik"],
        ["Insight Advisor API Example", "Programmatic NL querying of Qlik analytics"],
        ["Qlik Cloud Examples", "Scripts and snippets for Qlik Cloud integration"],
    ], [60, 130])

    _links_section(pdf, "Sources & References", [
        ("Qlik OSS GitHub Organization", "https://github.com/orgs/qlik-oss"),
        ("Qlik Cloud Monitoring Apps", "https://github.com/qlik-oss/qlik-cloud-monitoring-apps"),
        ("Qlik MCP Registry", "https://github.com/qlik-oss/qlik-mcp-registry"),
        ("Qlik Developer Portal", "https://qlik.dev/"),
        ("enigma.js", "https://github.com/qlik-oss/enigma.js"),
        ("qlik-api-ts", "https://github.com/qlik-oss/qlik-api-ts"),
        ("Server-Side Extensions", "https://github.com/qlik-oss/server-side-extension"),
        ("Embedding Qlik Answers", "https://github.com/qlik-oss/qlik-cloud-embed-oauth-impersonation"),
    ])


# ===========================================================================
#  Public API
# ===========================================================================

def generate_pdf() -> bytes:
    """Generate the full PDF and return as bytes."""
    logo_path = Path(__file__).parent / "logo" / "logo.png"
    pdf = _QlikPDF(logo_path=logo_path if logo_path.exists() else None)
    pdf.alias_nb_pages()

    _build_home(pdf)
    _build_part1(pdf)
    _build_part2(pdf)
    _build_part3(pdf)
    _build_part4(pdf)

    return bytes(pdf.output())
