---
name: ai-agent-and-system-design
description: Architecture, engineering workflows, and design patterns for building Autonomous AI Agents, Multi-Agent Orchestration, ReAct loops, and tool-calling systems.
---

# AI Agent & Autonomous System Design Standards

This skill provides the architectural blueprints and engineering standards for developing reliable AI agents, multi-agent topologies, and tool-augmented LLM applications.

---

## 1. Agent Cognitive Architecture (The ReAct Loop)

Always structure autonomous agents around the **Reasoning → Acting → Observing → Reflecting** cycle:

```
┌─────────────────────────────────────────────────────────┐
│ 1. USER INTENT & CONTEXT INGESTION                      │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ 2. REASONING / THOUGHT (Plan & Decide)                  │
│    - Analyze state, determine missing information        │
│    - Choose specific tool and construct valid arguments │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ 3. ACTING / TOOL EXECUTION                              │
│    - Validate schema (Pydantic / Zod)                   │
│    - Execute tool (API call, DB query, shell command)   │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ 4. OBSERVATION & CRITIQUE                               │
│    - Ingest tool output or error                        │
│    - Did the tool achieve the sub-goal?                 │
│      ├── YES → Continue to next step / return answer    │
│      └── NO  → Self-correct, adjust query, retry (<= 3x)│
└─────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Agent Orchestration Topologies

### A. Supervisor (Manager-Worker) Topology
Recommended for complex, multi-domain tasks (e.g. Full-Stack feature creation):
```
                       ┌─────────────────────┐
                       │  Supervisor Agent   │
                       │ (Planner & Router)  │
                       └──────────┬──────────┘
             ┌────────────────────┼────────────────────┐
             ▼                    ▼                    ▼
     ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
     │ Frontend Dev  │    │  Backend Dev  │    │   QA / Test   │
     │ Agent (Worker)│    │ Agent (Worker)│    │ Agent (Worker)│
     └───────────────┘    └───────────────┘    └───────────────┘
```

### B. Sequential Pipeline (Assembly Line)
Recommended for linear workflows (e.g., Code Generation -> Static Analysis -> Security Scan -> Commit):
```
Input ──> [Generator Agent] ──> [Reviewer Agent] ──> [Security Agent] ──> Output
```

---

## 3. Tool Calling & Structured Output Engineering

### Rules for Tool Design:
1. **Strict Type Contracts**: Define all tools using Pydantic v2 / Zod with explicit docstrings and field descriptions.
2. **Defensive Error Handling**: When a tool fails, return a structured error message (`{"success": false, "error": "User not found with ID usr_123"}`) instead of throwing an unhandled exception that crashes the agent.
3. **Idempotency & Safe State Mutation**: Tools that modify state (write to DB, delete files, send emails) must be idempotent and support confirmation / dry-run flags.

### Pydantic Tool Definition Example (Python):
```python
from pydantic import BaseModel, Field

class SearchCodebaseArgs(BaseModel):
    query: str = Field(..., description="Target symbol, function name, or exact regex to find.")
    file_pattern: str = Field("*.py", description="Glob pattern to restrict search scope.")
    max_results: int = Field(20, ge=1, le=50, description="Maximum number of matches to return.")
```

---

## 4. Human-In-The-Loop (HITL) Checkpoints

For high-impact, irreversible actions (e.g. database schema migrations, dropping tables, deploying to production, sending external emails):
1. The agent must **PAUSE** execution.
2. Present a structured summary of the proposed action with a diff or impact assessment.
3. Require explicit user approval before executing the mutating tool.
