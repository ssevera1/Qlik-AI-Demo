# C4 Model — Level 4: Code-Level Patterns

Shows implementation patterns for key integration points.

## Pattern: Analytic Connection Chart Expression (LLM Call)

```mermaid
sequenceDiagram
    participant User
    participant QlikSense as Qlik Sense App
    participant AssocEngine as Associative Engine
    participant SSE as SSE Connector
    participant LLM as External LLM API

    User->>QlikSense: Select employee "Jane Doe"
    QlikSense->>AssocEngine: Recalculate expressions
    AssocEngine->>AssocEngine: Evaluate if(count(distinct [Name]) = 1, ...)
    AssocEngine->>SSE: endpoints.ScriptAggrStr(config, prompt)
    SSE->>LLM: POST /v1/chat/completions
    Note right of LLM: {"model": "gpt-4o",<br/>"messages": [{"role":"user",<br/>"content":"Analyze retention risk<br/>for Jane Doe in Engineering..."}]}
    LLM-->>SSE: {"choices":[{"message":{"content":"..."}}]}
    SSE-->>AssocEngine: Extract choices.message.content
    AssocEngine-->>QlikSense: Update Text & Image object
    QlikSense-->>User: Display AI-generated insight

    User->>QlikSense: Clear selection, select "John Smith"
    Note over User,LLM: Entire flow repeats automatically
```

### Qlik Expression Code

```
// Gate behind single selection to control API costs
if(count(distinct [EmployeeID]) = 1,
   endpoints.ScriptAggrStr(
     '{"RequestType":"endpoint",
       "endpoint":{
         "connectionname":"OpenAI_HR_Analysis",
         "column":"choices.message.content"
       }
     }',
     'You are an HR analytics expert. Analyze the following employee data '
     & 'and provide a retention risk assessment with specific recommendations. '
     & chr(10) & chr(10)
     & 'Employee: ' & only([EmployeeName])
     & chr(10) & 'Department: ' & only([Department])
     & chr(10) & 'Tenure: ' & only([YearsAtCompany]) & ' years'
     & chr(10) & 'Performance Rating: ' & only([PerformanceRating])
     & chr(10) & 'Predicted Attrition Risk: ' & only([AttritionProbability])
     & chr(10) & 'Last Promotion: ' & only([YearsSinceLastPromotion]) & ' years ago'
     & chr(10) & 'Overtime: ' & only([OverTime])
   ),
   'Please select exactly one employee to view AI-powered retention analysis.'
)
```

## Pattern: Button-Triggered Automation with LLM

```mermaid
sequenceDiagram
    participant User
    participant Button as Qlik Sense Button
    participant Auto as Automation Engine
    participant Bookmark as Bookmark API
    participant LLM as OpenAI API
    participant Slack as Slack API

    User->>Button: Click "Generate Team Report"
    Button->>Auto: Trigger automation (app_id, selections)
    Auto->>Bookmark: Create temporary bookmark
    Bookmark-->>Auto: bookmark_id
    Auto->>Auto: Apply bookmark, get selections
    Auto->>Auto: List current selections (dept=Engineering)
    Auto->>Auto: Build prompt with selection context
    Auto->>LLM: POST /v1/chat/completions
    Note right of LLM: "Generate a team health<br/>report for Engineering<br/>department based on..."
    LLM-->>Auto: Report content
    Auto->>Slack: POST message to #hr-analytics
    Slack-->>Auto: 200 OK
    Auto-->>User: Notification: "Report sent to Slack"
```

## Pattern: Qlik Predict Integration (Batch + Real-Time)

```mermaid
sequenceDiagram
    participant DataSource as HRIS Data
    participant QP as Qlik Predict
    participant Model as Trained Model
    participant QS as Qlik Sense App
    participant API as Real-Time API
    participant Manager as HR Manager

    Note over DataSource,QP: Batch Flow (scheduled)
    DataSource->>QP: Employee dataset (CSV/QVD)
    QP->>Model: Run batch predictions
    Model-->>QP: Predictions + SHAP values
    QP->>QS: Load prediction output (Parquet)
    QS->>QS: Build flight risk dashboard

    Note over Manager,API: Real-Time Flow (interactive)
    Manager->>QS: Open "What-If" scenario
    Manager->>QS: Adjust salary +10%, change dept
    QS->>API: POST /ml/predictions (modified features)
    API->>Model: Inference with modified features
    Model-->>API: New prediction probability
    API-->>QS: Updated risk score
    QS-->>Manager: "Risk drops from 78% to 34%"
```

## Pattern: MCP Server Access (External AI)

```mermaid
sequenceDiagram
    participant Claude as Claude Desktop
    participant MCP as Qlik MCP Server
    participant Engine as Analytics Engine
    participant App as Qlik Sense App

    Claude->>MCP: Connect via MCP protocol
    MCP-->>Claude: Available tools: explore_apps, query_data, create_sheet...

    Claude->>MCP: explore_apps()
    MCP->>App: List available apps
    App-->>MCP: [HR Dashboard, Workforce Planning, ...]
    MCP-->>Claude: App list with metadata

    Claude->>MCP: query_data(app="HR Dashboard", expression="Avg(AttritionRate) by Department")
    MCP->>Engine: Execute calculation
    Engine-->>MCP: Results (Engineering: 12%, Sales: 18%, ...)
    MCP-->>Claude: Structured results with governance metadata

    Claude->>Claude: Synthesize insight
    Claude-->>Claude: "Sales has 50% higher attrition than Engineering..."
```
