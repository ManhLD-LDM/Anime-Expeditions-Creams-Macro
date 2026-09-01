---
name: prompt-engineering-and-evals
description: Production prompt engineering standards, XML tag structuring, few-shot prompting, and automated LLM evaluation frameworks (Evals/Ragas).
---

# Prompt Engineering & LLM Evaluation Framework

This skill establishes the production standard for engineering resilient system prompts and running automated evaluation benchmarks (Evals).

---

## 1. Production System Prompt Anatomy

Format system prompts as explicit **Operating Manuals** using XML tags for compartmentalization:

```xml
<system_prompt>
  <role>
    You are an expert Backend Systems Architect specialized in high-concurrency Node.js and PostgreSQL.
  </role>

  <operational_constraints>
    - Never invent API endpoints or database columns not present in <schema>.
    - Always use parameterized queries for database operations.
    - If required information is missing, ask for clarification instead of guessing.
  </operational_constraints>

  <context>
    <!-- Dynamic context, RAG retrieved chunks, or user profile injected here -->
  </context>

  <instructions>
    1. Analyze the user request against <context>.
    2. Think step-by-step in <thinking> tags before generating code.
    3. Output the final solution inside ```language code blocks.
  </instructions>

  <output_format>
    Strict JSON adhering to the provided JSON Schema.
  </output_format>
</system_prompt>
```

### Why XML Tags?
- **Prompt Injection Defense**: Clear delimiters prevent user inputs from overriding system instructions.
- **Model Attention**: LLMs parse structural XML tags significantly better than plain markdown headers or markdown blocks.

---

## 2. Prompting Techniques

1. **Chain-of-Thought (CoT)**: Force the model to reason through intermediate steps before producing the final output:
   `"Think step-by-step: first analyze the invariants, then identify edge cases, and finally write the code."`
2. **Few-Shot Exemplars**: Provide 2-3 input/output pairs representing the hardest edge cases to anchor model behavior.
3. **Negative Constraints**: State clearly what the model **must NOT do** (e.g. `"Do NOT use third-party libraries for date formatting; use native Date or Temporal API"`).

---

## 3. Automated LLM Evaluations (Evals)

Never "prompt harder" without an evaluation benchmark. Measure quality using structured metrics:

```
┌─────────────────────────────────────────────────────────┐
│ 1. Faithfulness (Hallucination Metric)                   │
│    - Is all generated information grounded in context?  │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ 2. Answer Relevance                                     │
│    - Does the response directly address the user query? │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ 3. Context Precision & Recall                           │
│    - Did the RAG system retrieve all necessary chunks?  │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ 4. Deterministic Rule Checks                            │
│    - JSON schema validity, regex pattern match, latency │
└─────────────────────────────────────────────────────────┘
```

### Automated CI Regression Evals:
- Maintain a **Golden Dataset** of 50-100 real-world user queries with verified ground truth answers.
- Run automated eval suites (using `deepeval`, `ragas`, or custom test scripts) on every prompt modification in CI before merging.
