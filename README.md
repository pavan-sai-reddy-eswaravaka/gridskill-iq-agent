\# GridSkill IQ



\*\*GridSkill IQ\*\* is a multi-agent reasoning system for UK energy workforce certification readiness, workload-aware study planning, grounded assessment, and manager-level readiness insights.



This project is built for the \*\*Microsoft Agents League Hackathon – Reasoning Agents track\*\*.



\---



\## Project Summary



GridSkill IQ helps a synthetic UK energy organisation manage internal certification readiness across technical teams such as grid operations, smart meter analytics, cybersecurity support, renewable operations, energy forecasting, and Power BI reporting.



The system uses multiple specialised agents to:



\* Map learner roles to relevant certifications

\* Generate workload-aware study plans

\* Recommend engagement and reminder strategies

\* Assess learner readiness

\* Produce manager-level readiness insights

\* Apply a safety critic before final output

\* Provide evaluation and safety reporting through a Streamlit demo



\---



\## Important Data Notice



This project uses \*\*synthetic demonstration data only\*\*.



No real employee data, customer data, confidential information, credentials, or personally identifiable information is used.



Synthetic identifiers include examples such as:



\* `EMP-001`

\* `L-1001`

\* `TEAM-A`



\---



\## Core Features



\* Multi-agent orchestration

\* Synthetic workforce learning data

\* Synthetic knowledge base documents

\* Role-to-certification mapping

\* Workload-aware study planning

\* Practice-readiness assessment

\* Manager-level team readiness summary

\* Safety Critic Agent

\* Evaluation report

\* Streamlit frontend demo



\---



\## Challenge Alignment



GridSkill IQ is aligned with the Reasoning Agents challenge because it demonstrates:



\* Multi-agent system design

\* Multi-step reasoning and orchestration

\* Grounded recommendations using synthetic knowledge documents

\* Context-aware study planning using synthetic work signals

\* Semantic modelling of learner, role, certification, skill gap, readiness score, and recommended hours

\* Responsible AI controls and safety checks

\* A demoable Streamlit user experience

\* Evaluation reporting



\---



\## Multi-Agent Architecture



```text

User Request

&#x20;  ↓

GridSkill Orchestrator Agent

&#x20;  ↓

Learning Path Curator Agent

&#x20;  ↓

Study Plan Generator Agent

&#x20;  ↓

Engagement Agent

&#x20;  ↓

Assessment Agent

&#x20;  ↓

Manager Insights Agent

&#x20;  ↓

Safety Critic Agent

&#x20;  ↓

Final Grounded Response

```



\---



\## Agents



\### 1. GridSkill Orchestrator Agent



Coordinates the full workflow. It receives the user request, loads the relevant synthetic learner profile, calls the specialist agents, collects outputs, and returns a final response.



\### 2. Learning Path Curator Agent



Maps a learner’s role and target certification to relevant skills and study direction.



Example:



\* Role: Grid Operations Analyst

\* Certification: PL-300

\* Skill gap: Power BI modelling



\### 3. Study Plan Generator Agent



Creates a workload-aware study plan using:



\* Recommended certification hours

\* Hours already studied

\* Meeting load

\* Focus hours

\* Preferred learning slot

\* Shift pattern



\### 4. Engagement Agent



Suggests reminder and engagement strategy based on synthetic work signals.



Example:



\* High meeting load → shorter, lower-disruption reminders

\* Strong focus capacity → structured study sessions



\### 5. Assessment Agent



Evaluates readiness using:



\* Practice score

\* Recommended study hours

\* Progress against target threshold

\* Certification skill requirements



It also generates grounded practice questions from the synthetic certification knowledge base.



\### 6. Manager Insights Agent



Provides team-level readiness summaries without exposing unnecessary personal detail.



Example output:



\* TEAM-A readiness status

\* TEAM-B risk status

\* TEAM-C manager action recommendation



\### 7. Safety Critic Agent



Checks the final output for:



\* Synthetic data disclaimer

\* Privacy issues

\* Unsupported claims

\* Unsafe wording

\* Confidential-data risk



\---



\## Microsoft IQ Alignment



\### Foundry IQ Alignment



The project uses synthetic knowledge base documents to ground agent responses.



Knowledge base files include:



\* `grid\_certification\_guide.md`

\* `workload\_learning\_policy.md`

\* `manager\_readiness\_policy.md`



In a Microsoft Foundry implementation, these documents can be indexed as approved knowledge sources for grounded retrieval and cited responses.



\### Work IQ Alignment



The project uses synthetic work-context signals such as:



\* Meeting hours per week

\* Focus hours per week

\* Preferred learning slot

\* Shift pattern



These signals help the Engagement Agent and Study Plan Generator create realistic, workload-aware recommendations.



\### Fabric IQ Alignment



The project uses a synthetic semantic model connecting:



\* Learner

\* Employee

\* Team

\* Role

\* Certification

\* Skill gap

\* Practice score

\* Recommended study hours

\* Readiness status



This supports manager-level reasoning and structured decision support.



\---



\## Project Structure



```text

gridskill-iq-agent/

│

├── app/

│   └── streamlit\_app.py

│

├── data/

│   └── synthetic/

│       ├── learners.csv

│       ├── work\_signals.csv

│       └── certifications.json

│

├── knowledge\_base/

│   ├── grid\_certification\_guide.md

│   ├── workload\_learning\_policy.md

│   └── manager\_readiness\_policy.md

│

├── reports/

│   └── evaluation\_report.txt

│

├── src/

│   ├── create\_synthetic\_data.py

│   ├── evaluate\_gridskill\_iq.py

│   └── gridskill\_multi\_agent.py

│

├── tests/

│

├── README.md

├── requirements.txt

└── .gitignore

```



\---



\## How to Run the Project



\### 1. Install requirements



```bash

pip install -r requirements.txt

```



\### 2. Generate synthetic data



```bash

python src/create\_synthetic\_data.py

```



\### 3. Run learner workflow



```bash

python src/gridskill\_multi\_agent.py --learner EMP-003

```



\### 4. Run manager workflow



```bash

python src/gridskill\_multi\_agent.py --manager

```



\### 5. Run evaluation report



```bash

python src/evaluate\_gridskill\_iq.py

```



\### 6. Run Streamlit demo



```bash

streamlit run app/streamlit\_app.py

```



\---



\## Streamlit Demo



The Streamlit frontend includes four tabs:



1\. \*\*Learner Readiness Agent\*\*



&#x20;  \* Runs the learner-level multi-agent workflow



2\. \*\*Manager Insights Agent\*\*



&#x20;  \* Produces team-level readiness summaries



3\. \*\*System Architecture\*\*



&#x20;  \* Shows the agent workflow and Microsoft IQ alignment



4\. \*\*Evaluation \& Safety\*\*



&#x20;  \* Displays the evaluation report and responsible AI controls



\---



\## Example Use Cases



\### Learner Use Case



A synthetic learner asks:



> I am EMP-003. Help me prepare for my certification.



The system:



1\. Identifies the learner role

2\. Maps the role to a certification

3\. Checks workload capacity

4\. Creates a study plan

5\. Generates practice questions

6\. Assesses readiness

7\. Runs safety validation



\### Manager Use Case



A manager asks:



> Which teams need certification readiness support?



The system:



1\. Aggregates synthetic readiness status by team

2\. Identifies high-risk teams

3\. Recommends manager action

4\. Avoids exposing unnecessary individual details



\---



\## Evaluation



The project includes a lightweight evaluation suite in:



```text

src/evaluate\_gridskill\_iq.py

```



The evaluation checks whether:



\* The learner workflow calls the expected agents

\* The manager workflow produces team insights

\* Synthetic data disclaimers are present

\* Sources are included

\* Safety Critic Agent is active

\* Key readiness outputs are generated



The generated report is saved to:



```text

reports/evaluation\_report.txt

```



\---



\## Responsible AI and Safety



GridSkill IQ includes the following safety controls:



\* Synthetic data only

\* No real employee or customer information

\* No confidential or proprietary data

\* No credentials committed to the repository

\* `.env` excluded through `.gitignore`

\* Safety Critic Agent checks final output

\* Human oversight recommended

\* Designed for decision support, not automatic certification approval



\---



\## Current Limitations



\* This is a hackathon prototype, not a production system.

\* Current data is synthetic and small-scale.

\* Current implementation runs locally through Python and Streamlit.

\* Microsoft Foundry / Foundry IQ production deployment should be added for a full cloud implementation.

\* The current Safety Critic Agent is rule-based and should be expanded for production use.

\* Real organisational use would require security review, privacy review, access control, monitoring, and evaluation.



\---



\## Future Enhancements



\* Microsoft Foundry Agent Service deployment

\* Foundry IQ knowledge indexing

\* Azure AI Search grounding

\* Microsoft Learn MCP integration

\* Fabric semantic model integration

\* Advanced evaluation suite

\* Telemetry and trace logging

\* Role-based access control

\* Docker container deployment

\* Manager dashboard with charts

\* Multi-team readiness forecasting



\---



\## Tech Stack



\* Python

\* Streamlit

\* CSV / JSON synthetic data

\* Markdown synthetic knowledge base

\* Multi-agent orchestration logic

\* Rule-based safety critic

\* Evaluation script



\---



\## Project Positioning



GridSkill IQ demonstrates how a multi-agent reasoning system can support enterprise workforce learning and certification readiness in a safety-conscious, explainable, and demoable way.



The project is designed around the idea that organisations need more than generic chatbots. They need systems that can reason across:



\* Role requirements

\* Learning content

\* Workload capacity

\* Certification readiness

\* Team-level risk

\* Responsible AI controls



\---



\## License



This project is for hackathon demonstration and educational use.





## V3 Grounded Reasoning Upgrade

GridSkill IQ now includes a V3 grounded multi-agent workflow.

This upgrade adds a Foundry IQ-style local retrieval layer that searches synthetic knowledge base documents before the specialist agents generate their outputs. This makes the system more explainable because learner and manager recommendations are supported by retrieved evidence and source files.

### V3 Features

- Synthetic knowledge retrieval from markdown policy and certification documents
- Grounded evidence snippets before agent decisions
- Source tracking for retrieved evidence
- Confidence scoring based on practice score, study progress, focus capacity and evidence availability
- Specialist agent execution after evidence retrieval
- Safety Critic Agent validation before final output
- JSON trace logging for observability and auditability
- Streamlit frontend buttons for Grounded V3 learner and manager workflows

### Why V3 Matters

The V3 workflow moves the project beyond a simple rule-based prototype. It demonstrates an agentic reasoning pattern where the system first retrieves relevant knowledge, then executes specialist agents, then validates the final answer using a safety critic.

This aligns with the hackathon focus on reasoning agents, grounded knowledge, Microsoft IQ-style architecture, synthetic data, evaluation and responsible AI design.

