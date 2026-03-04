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
        "Covers Qlik Answers (agentic analytics with structured + unstructured data) - GA Feb 2026",
        "Documents Qlik Predict (AutoML) with HR-specific use cases for turnover, promotions, and lateral moves",
        "Explains Application Automations for integrating external LLMs (OpenAI, Claude, etc.) into Qlik apps",
        "Maps the full Qlik Cloud AI/ML ecosystem including planned features like Discovery Agent and MCP Server",
        "All content is Qlik Cloud only - no on-premises Qlik Sense Enterprise content",
    ])

    _add_subsection(pdf, "Timeline of Key Announcements")
    _table(pdf, ["Date", "Milestone"], [
        ["2024", "Qlik Answers launched (unstructured data only)"],
        ["May 2025", "Agentic analytics vision announced at Qlik Connect"],
        ["Oct 2025", "Multivariate Time Series GA in Qlik Predict"],
        ["Dec 2025", "Agentic Qlik Answers private preview"],
        ["Feb 2026", "Qlik Answers agentic GA + MCP Server GA"],
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
        "Impact: Qlik Answers replaces Insight Advisor and Insight Advisor Chat in enabled tenants - this is a tenant-wide change.",
        "Key Requirement: Tenant admins must opt in to cross-region data processing to enable the agentic experience.",
        "New Capabilities: Multi-step agentic reasoning, visual + narrative responses, MCP Server for third-party AI assistants (Claude, ChatGPT), Discovery Agent for anomaly detection.",
    ])

    # 1.2
    _add_section_title(pdf, "1.2 Latest Capability: Structured Data")
    _body(pdf, "Qlik Answers evolved from a document-only Q&A chatbot (2024) into a full agentic analytics platform that works across both structured application data and unstructured documents.")
    _body(pdf, "The agentic experience is delivered through Qlik Answers as the unified conversational interface, powered by:")
    _bullet(pdf, "Qlik Analytics Engine - performs governed, context-preserving calculations on structured app data")
    _bullet(pdf, "Specialized AI Agents - handle multi-step reasoning, planning, and orchestration")
    _bullet(pdf, "RAG (Retrieval Augmented Generation) - retrieves relevant passages from curated knowledge bases")
    _bullet(pdf, "LLM Reasoning - synthesizes insights into rich narrative and visual responses with citations")
    pdf.ln(3)

    _add_subsection(pdf, "Key Components")
    _table(pdf, ["Component", "Description"], [
        ["Qlik Answers (Core)", "Unified conversational interface. Structured + unstructured data. Always-on side panel. Citations and reasoning explanations. Embeddable in external apps."],
        ["Discovery Agent", "Continuously monitors key measures. Surfaces anomalies and shifts. Proactive alerting. Planned rollout shortly after GA."],
        ["MCP Server", "Exposes Qlik at engine, tool, and agent levels. Third-party AI assistants (Claude, ChatGPT). Secure access to governed data. GA Feb 2026."],
    ], [40, 150])

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
        ["Indexed page size", "~2,000 characters of text data"],
    ], [80, 110])

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

    _links_section(pdf, "Sources & References", [
        ("Qlik GA Press Release (Feb 2026)", "https://www.businesswire.com/news/home/20260210837577/en/Qlik-Brings-Agentic-Analytics-to-General-Availability-and-Launches-MCP-Server-for-Third-Party-Assistants"),
        ("Qlik Answers - Qlik Cloud Help", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/Qlik-Answers.htm"),
        ("Qlik Agentic AI Vision Blog", "https://www.qlik.com/blog/a-vision-for-the-future-qliks-new-agentic-ai-experience"),
        ("Enabling Cross-Region Data Processing", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Admin/cross-region-data-processing.htm"),
        ("Qlik Answers Access and Permissions", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/qlik-answers-permissions.htm"),
        ("Deploying and Administering Qlik Answers", "https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/QlikAnswers/administering-qlik-answers.htm"),
        ("Qlik Answers Product Page", "https://www.qlik.com/us/products/qlik-answers"),
        ("Qlik MCP Community Video", "https://community.qlik.com/t5/Integration-Extension-APIs/Qlik-Cloud-Development-with-Claude-Desktop-and-MCP-Servers-Video/td-p/2535891"),
    ])


def _build_part2(pdf: _QlikPDF):
    _add_part_title(pdf, "Part 2: Qlik Predict - Automated Machine Learning")

    # 2.1
    _add_section_title(pdf, "2.1 Executive Summary")
    _exec_box(pdf, "Executive Summary - Qlik Predict", [
        "What: Qlik Predict (formerly Qlik AutoML) is a no-code automated machine learning platform embedded in Qlik Cloud Analytics.",
        "Capabilities: Binary/multiclass classification, regression, and multivariate time series forecasting (GA Oct 2025) with GPU-accelerated deep learning.",
        "Explainability: Built-in SHAP-based explainability shows which features drive predictions at both global and row levels.",
        "Deployment: Three methods - batch predictions, real-time API, and Qlik Predict analytics connector for in-app integration.",
        "HR Applications: Ideal for predicting employee turnover, promotions, lateral movements, absenteeism, compensation equity, and workforce demand forecasting.",
    ])

    # 2.2
    _add_section_title(pdf, "2.2 How Qlik Predict Works")
    _body(pdf, "Qlik Predict follows a six-step automated workflow:\n1. Data Loading & Profiling - Upload CSV, QVD, XLSX\n2. Experiment Creation - Select target column, auto-detect problem type\n3. Automated Model Training - Multiple algorithms, intelligent optimization\n4. Model Evaluation & Scoring - SHAP explainability, feature importance\n5. Deployment - Model approval, versioning, swapping\n6. Prediction & Visualization - Batch, real-time API, analytics connector")

    _add_subsection(pdf, "Key Constraints")
    _bullet(pdf, "Max 500 columns per dataset")
    _bullet(pdf, "API rate limit: 300 requests/minute")
    _bullet(pdf, "Analytics connector: 200,000 rows per request (batched in 2,000 row chunks)")
    _bullet(pdf, "Not available on Qlik Cloud Government")
    _bullet(pdf, "Available in Premium and Enterprise tiers")
    pdf.ln(3)

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
        ("Diversity & Inclusion Risk", "Classification"),
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
        "LLM Connectors: Native OpenAI connector + generic API Key connector (for any LLM) + 8 native analytic connections.",
        "Dynamic Updates: Analytic connections in chart expressions respond to user selections in real-time.",
        "Embedding: Two patterns - button-triggered automations (workflow) and analytic connection chart expressions (inline AI).",
        "Fallback Strategy: When Qlik Answers is insufficient, external LLMs provide free-form narratives, sentiment analysis, and custom reasoning.",
    ])

    # 3.2
    _add_section_title(pdf, "3.2 Application Automations Overview")
    _body(pdf, "Qlik Application Automations are a no-code workflow automation platform (iPaaS) built into Qlik Cloud. Users build automated workflows between Qlik Cloud and external SaaS applications without writing code.")
    _bullet(pdf, "Visual drag-and-drop builder with data and logic blocks")
    _bullet(pdf, "On-demand triggers (manual or from Qlik Sense buttons)")
    _bullet(pdf, "Webhook triggers from external events")
    _bullet(pdf, "Scheduled automations at specific times")
    _bullet(pdf, "Pre-built connectors: Salesforce, Teams, Slack, GitHub, ServiceNow, OpenAI, Hugging Face, etc.")
    pdf.ln(3)

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
        "GA Features (2025-2026): Qlik Answers, Qlik Predict, MCP Server, 8 LLM connectors, Automations, Augmented Analytics.",
        "Upcoming: Discovery Agent, Data Products for Analytics, expanded MCP support, agentic pipeline/quality/stewardship agents.",
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
        ["Analytic Connections", "GA", "8 native LLM connectors for chart expressions"],
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
    ], [50, 35, 105])

    # 4.3
    _add_section_title(pdf, "4.3 Planned / Upcoming Features")
    _table(pdf, ["Feature", "Status", "Description"], [
        ["Discovery Agent", "Rolling out post-GA", "Continuous anomaly monitoring and proactive alerting"],
        ["Data Products for Analytics", "Rolling out post-GA", "Curated governed datasets with quality signals"],
        ["Productivity Agents", "In development", "Contextual help and developer support across Qlik Cloud"],
        ["Expanded MCP Support", "Planned 2026", "Additional AI tools and assistants"],
        ["Agentic Data Pipeline Agents", "Planned", "AI agents for data integration and transformation"],
        ["Agentic Data Quality Agents", "Planned", "AI-powered data quality monitoring"],
        ["Agentic Stewardship Agents", "Planned", "AI governance and cataloging automation"],
        ["GenAI Insight Advisor Narratives", "Private Preview", "ChatGPT-like answers via Amazon Bedrock"],
        ["Governed Writeback (SAP, SF, Snowflake)", "Planned", "Native writeback to enterprise systems"],
        ["AWS European Sovereign Cloud", "Planned 2026", "$1.5B European investment over 5 years"],
    ], [60, 40, 90])

    _add_subsection(pdf, "Strategic Partnerships & Recognition")
    _table(pdf, ["Achievement", "Details"], [
        ["AWS Generative AI Competency", "Technical proficiency in Amazon Bedrock and SageMaker"],
        ["Gartner MQ: Analytics & BI", "Leader for 15th year (2025)"],
        ["Gartner MQ: Data Quality", "Leader for 6th time (2025)"],
        ["Qlik AI Specialist Certification", "Covers AI concepts, Qlik Predict, GenAI assistants"],
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
