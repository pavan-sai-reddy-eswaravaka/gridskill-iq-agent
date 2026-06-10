\# GridSkill IQ Architecture



\## System Overview



GridSkill IQ is a multi-agent reasoning system for synthetic UK energy workforce certification readiness.



The system coordinates specialist agents to support:



\- Learning path curation

\- Workload-aware study planning

\- Engagement recommendations

\- Readiness assessment

\- Manager-level insights

\- Safety validation



\## Architecture Diagram



```mermaid

flowchart TD

&#x20;   A\[User Request] --> B\[GridSkill Orchestrator Agent]



&#x20;   B --> C\[Learning Path Curator Agent]

&#x20;   B --> D\[Study Plan Generator Agent]

&#x20;   B --> E\[Engagement Agent]

&#x20;   B --> F\[Assessment Agent]

&#x20;   B --> G\[Manager Insights Agent]



&#x20;   C --> H\[Synthetic Knowledge Base]

&#x20;   D --> I\[Synthetic Work Signals]

&#x20;   E --> I

&#x20;   F --> H

&#x20;   G --> J\[Synthetic Learner Data]



&#x20;   C --> K\[Agent Outputs]

&#x20;   D --> K

&#x20;   E --> K

&#x20;   F --> K

&#x20;   G --> K



&#x20;   K --> L\[Safety Critic Agent]

&#x20;   L --> M\[Final Grounded Response]

&#x20;   M --> N\[Streamlit Demo Frontend]

