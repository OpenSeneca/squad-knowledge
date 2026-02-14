# Task: 2026-02-10-EVAL-SUITE

## Objective
Build Navari Evaluation Suite — integrate automated evaluation tools directly into Navari for 600+ users at AZ.

## Context
Justin needs production-ready evaluation for Navari (MCP-based agentic AI framework). Manual labeling doesn't scale at 600+ users. Squad research identified:
- LLM-as-a-Judge: 82-92% human agreement, hybrid model strategy saves 60-70% cost
- RAGAS: $0.02-0.05/eval, comprehensive RAG metrics (Faithfulness, Contextual Recall, Precision, Answer Relevancy)
- DeepEval: 10-15% lower cost than manual human eval, custom metrics, CI/CD integration
- Observability: Braintrust ($499-5k/mo) or Arize Phoenix ($3-7k/mo) recommended for Navari

## Components to Build

### 1. RAGAS Integration
- **Purpose:** Automated RAG evaluation
- **Metrics:** Faithfulness (0-1), Contextual Recall (0-1), Contextual Precision (0-1), Answer Relevancy (0-1)
- **Integration points:**
  - RAGAS library installation in Navari codebase
  - Evaluation endpoints for Navari's RAG queries
  - Scheduled evaluation runs (daily/weekly)
  - Results storage and trend visualization
- **Cost target:** $0.02-0.05 per evaluation (Claude 3.5 Haiku)

### 2. DeepEval Integration
- **Purpose:** General agent evaluation with custom metrics
- **Features:**
  - Custom metrics definition (Navari-specific)
  - Concurrent processing for batch evaluation
  - CI/CD pipeline integration
  - 10-15% cost reduction vs manual human evaluation
- **Integration points:**
  - DeepEval library installation
  - Evaluation workflow triggers
  - Results aggregation and dashboard display

### 3. LLM-as-a-Judge Service
- **Purpose:** Automated evaluation scaling without manual labeling
- **Strategy:** Hybrid small-large model approach
  - 80% of evaluations with small models (Claude 3.5 Haiku, GPT-4o Mini)
  - 20% with large models (Claude 3.5 Sonnet, GPT-4o)
  - **Cost savings:** 60-70% reduction while maintaining 90%+ accuracy
- **Agreement targets:** 82-92% human judge agreement for binary classification, 75-85% for fine-grained scoring
- **Implementation:**
  - Judge model routing logic (small vs large)
  - Evaluation prompt templates
  - Result comparison against ground truth or human samples

### 4. Observability Platform Connector
- **Purpose:** Production observability integration
- **Options:**
  - Braintrust: $499-5,000/mo, superior dev experience, real-time evaluation
  - Arize Phoenix: $3,000-7,000/mo, RBAC + SOC2/HIPAA compliance, drift detection
- **Integration points:**
  - SDK installation for chosen platform
  - Agent execution tracing hooks
  - Metrics export to Navari dashboard
  - Alert configuration (quality degradation thresholds)
- **Recommended TCO:** $2,500-4,000/month for Navari's 600+ users (Braintrust + Arize Phoenix combo)

### 5. Evaluation Dashboards
- **Purpose:** Real-time quality metrics and trend analysis
- **Features:**
  - RAG evaluation scores (Faithfulness, Recall, Precision, Relevancy)
  - Agent performance trends (success rate, latency, cost)
  - LLM-as-a-judge accuracy tracking
  - Multi-run reliability metrics (Pass@k)
  - CLEAR Framework 5-dimensional view (Cost, Latency, Efficiency, Assurance, Reliability)
- **Visualization:**
  - Time-series charts for metrics over time
  - Agent-by-agent performance comparison
  - Anomaly detection alerts
  - Export capabilities (CSV, JSON) for reporting

## Technical Requirements

### Technology Stack
- **Language:** Python 3.12+ (matches AZ's environment)
- **Dependencies:**
  - RAGAS (pip install ragas)
  - DeepEval (pip install deepeval)
  - OpenAI API / Anthropic API / Google AI API (for LLM-as-a-judge)
  - Observability platform SDK (Braintrust or Arize Phoenix)
- **Architecture:**
  - Modular components (plug-and-play evaluation tools)
  - Asynchronous evaluation for non-blocking agent execution
  - Configuration-driven (easy metric threshold tuning)

### Integration Points
- **Navari RAG system:** Hook into retrieval and generation pipelines for RAGAS evaluation
- **Navari agent execution:** Wrap agent calls for DeepEval custom metrics
- **Navari dashboard:** Add evaluation metrics panel with real-time updates
- **AZ compliance:** SOC2/HIPAA-ready data handling (use Arize Phoenix if compliance required)

## Quality Criteria
- [ ] Modular design (each evaluation component pluggable)
- [ ] Configuration-driven (easy metric tuning without code changes)
- [ ] Production-ready (error handling, logging, monitoring)
- [ ] Documentation (API reference, integration guide)
- [ ] Testing examples (sample evaluation runs with expected outputs)
- [ ] Cost estimation (per evaluation, monthly TCO for 600+ users)
- [ ] Performance benchmarks (evaluation overhead <10% of agent call time)

## Output Format

**Deliverables:**
1. `navari-eval-suite/` — Python package structure
   - `src/ragas_integration.py` — RAGAS integration module
   - `src/deepeval_integration.py` — DeepEval integration module
   - `src/llm_as_judge.py` — LLM-as-a-judge service
   - `src/observability_connector.py` — Platform connector
   - `src/dashboard.py` — Evaluation metrics dashboard
2. `README.md` — Setup guide, configuration reference, usage examples
3. `docs/INTEGRATION.md` — Detailed integration steps for Navari
4. `tests/` — Evaluation component tests
5. `examples/` — Sample evaluation runs

**Documentation should include:**
- Installation instructions (pip install, dependency versions)
- Configuration examples (environment variables, config files)
- Integration guide for Navari (hooks, endpoints, data flow)
- Troubleshooting guide (common issues, debugging)

## Relevance to Justin
Navari scales to 600+ users at AZ. Manual evaluation is the bottleneck. This evaluation suite enables:
- Automated quality assessment at production scale
- 60-70% cost reduction via LLM-as-a-judge strategy
- Real-time quality metrics for rapid issue detection
- Compliance-ready (SOC2/HIPAA) with Arize Phoenix option

## Priority
HIGHEST — this addresses Justin's immediate need for scaling evaluation at Navari

## Collaboration
Marcus and Galen provide evaluation metric specifications, thresholds, and domain-specific requirements (biotech/pharma, regulatory compliance). Archimedes builds the technical implementation.

## Due
Within 4 hours (scaffold + integration + documentation + testing)

## Domain
1 - Agentic AI & Agent Frameworks (Navari-specific)
