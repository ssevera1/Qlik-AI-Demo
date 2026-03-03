# ADR-004: Qlik Predict (AutoML) for HR Predictive Analytics Over External ML Platforms

## Status
Accepted

## Context
People analytics teams need predictive capabilities for employee turnover, promotion readiness,
and workforce demand forecasting. Several options exist:

1. **Qlik Predict** — Native no-code AutoML within Qlik Cloud
2. **Amazon SageMaker** — Full ML platform with Qlik connector
3. **Python/R-based ML** — Custom models deployed via SSE or external endpoints
4. **Third-party HR analytics platforms** — Visier, One Model, etc.

## Decision
Recommend **Qlik Predict** as the primary ML platform for HR predictive analytics, with external
ML platforms as supplements for advanced use cases.

## Rationale
- **No data science required**: HR analytics teams typically lack dedicated data scientists — Qlik Predict's no-code interface removes this barrier
- **Native integration**: Predictions flow directly into Qlik Sense dashboards without ETL or custom API development
- **SHAP explainability**: Built-in feature importance visualization is critical for HR — must explain *why* an employee is flagged as at-risk, not just the score
- **Governance workflow**: Model approval step ensures predictions are reviewed before deployment — important for HR decisions that affect people
- **Real-time what-if**: Managers can explore "what happens if we promote this person?" scenarios directly in the dashboard
- **Automation integration**: Qlik Automate can trigger alerts and workflows based on prediction outcomes
- **Algorithm coverage**: 8 classification algorithms, 6 regression algorithms, 3 deep learning time series models cover all standard HR prediction use cases

## Trade-offs Accepted
- **Algorithm limitations**: No neural networks for tabular data (beyond time series), no deep learning for unstructured data (e.g., resume parsing, sentiment on free-text)
- **Scale constraints**: 500 columns max, 200K rows per connector request — sufficient for most HR datasets but may limit very large enterprises
- **No custom feature engineering**: While intelligent optimization handles transformations automatically, complex domain-specific features (e.g., organizational network analysis) must be pre-computed
- **No online/streaming learning**: Models are retrained in batch — not suitable for real-time model updates
- **Premium/Enterprise tier required**: Not available in standard Qlik Cloud subscriptions

## Consequences
- Application documents all HR use cases with implementation guidance (Part 2)
- SHAP visualization patterns documented for HR-specific dashboards
- Qlik Automate integration shown for alert workflows (e.g., high flight risk employees)
- External LLM integration (Part 3) supplements Qlik Predict with narrative generation
- Time series forecasting used for workforce demand planning use cases
