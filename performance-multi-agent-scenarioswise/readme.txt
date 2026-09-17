Multi-Agent Performance Testing PoC —  Flow
                         USER
                          │
                          ▼
                ┌─────────────────────┐
                │ Scenario Selection   │
                │                     │
                │ 1. LOAD             │
                │ 2. STRESS           │
                │ 3. SPIKE            │
                │ 4. ENDURANCE        │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Test Planner      │
                │       Agent         │
                │                     │
                │ Understands         │
                │ requirement         │
                │                     │
                │ Generates:          │
                │ • Test type         │
                │ • URL               │
                │ • VUs / stages      │
                │ • Duration          │
                │ • Thresholds        │
                │ • Scenarios         │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  K6 Script Generator│
                │       Agent         │
                │                     │
                │ Converts test plan  │
                │ into executable     │
                │ k6 JavaScript       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Script Reviewer    │
                │       Agent         │
                │                     │
                │ Validates:          │
                │ • JavaScript syntax │
                │ • k6 structure      │
                │ • stages            │
                │ • thresholds        │
                │ • HTTP request      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Generated K6 Script │
                │                     │
                │ k6/generated_test.js│
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    K6 Executor      │
                │       Agent         │
                │                     │
                │ Executes generated  │
                │ k6 test              │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Result Analyzer     │
                │       Agent         │
                │                     │
                │ Analyzes:           │
                │ • P95               │
                │ • Max response time │
                │ • Error rate        │
                │ • Requests          │
                │ • Throughput        │
                │ • Thresholds        │
                │ • Findings          │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Report Generator    │
                │       Agent         │
                │                     │
                │ Creates professional│
                │ Markdown report     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Scenario-Specific   │
                │ Performance Report  │
                │                     │
                │ reports/            │
                │ performance_report  │
                │ .md                 │
                └─────────────────────┘


Key Points:

"This PoC demonstrates an AI-driven multi-agent performance testing framework using GitHub Copilot and k6."

"The user first selects the required performance test type—Load, Stress, Spike, or Endurance."

"The Test Planner Agent analyzes the requirement and creates a structured performance test plan containing the target URL, HTTP method, load profile, thresholds, scenarios, and assumptions."

"The K6 Script Generator Agent then converts that test plan into an executable k6 JavaScript script."

"Before execution, the Script Reviewer Agent validates the generated script to make sure the k6 configuration, stages, thresholds, HTTP request, and JavaScript structure are valid."

"The reviewed script is then saved as the generated k6 test and passed to the K6 Executor Agent."

"K6 executes the test and produces the actual performance results."

"The Result Analyzer Agent analyzes those results against the performance thresholds and determines whether the test passed or failed."

"Finally, the Report Generator Agent converts the test plan and analysis into a professional scenario-specific Markdown performance report."

"So instead of manually creating different scripts for Load, Stress, Spike, and Endurance testing, the same framework dynamically generates and executes the appropriate k6 test based on the selected scenario."

What makes this valuable:

The key point to highlight is:

                 ONE FRAMEWORK
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
     LOAD           STRESS          SPIKE
       │              │              │
       └──────────────┼──────────────┘
                      │
                   ENDURANCE
                      │
                      ▼
              Dynamic K6 Script
                      │
                      ▼
             Dynamic Analysis
                      │
                      ▼
          Dynamic Performance Report

we are not maintaining:

load.js
stress.js
spike.js
endurance.js

Instead:

Scenario Selection
       ↓
AI Test Plan
       ↓
Generic K6 Generator
       ↓
Generated Scenario-Specific Script
       ↓
Execute
       ↓
Analyze
       ↓
Generate Report

actual project structure :
│
├── agents/
│   ├── test_planner.py
│   ├── k6_generator.py
│   ├── script_reviewer.py
│   ├── k6_executor.py
│   ├── result_analyzer.py
│   └── report_generator.py
│
├── prompts/
│   ├── planner_prompt.txt
│   ├── k6_generator_prompt.txt
│   ├── script_reviewer_prompt.txt
│   ├── analyzer_prompt.txt
│   └── report_generator_prompt.txt
│
├── k6/
│   └── generated_test.js
│
├── reports/
│   └── performance_report.md
│
├── results/
│   └── result.json
│
├── main.py
├── config.py
└── test_config.json

One-line architecture for the entire flow

User → Scenario Selection → AI Planner → AI K6 Generator → AI Script Reviewer → K6 Execution → AI Result Analyzer → AI Report Generator → Scenario-Specific Performance Report

Test Planner = What should we test?
K6 Generator = How should k6 execute it?
Script Reviewer = Is the generated k6 script valid?
K6 Executor = Run it.
Result Analyzer = What happened?
Report Generator = Explain the result.