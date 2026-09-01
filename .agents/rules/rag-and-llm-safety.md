---
description: Rules for RAG grounding, hallucination prevention, data privacy, and cost optimization
globs: ["**/*.{py,ts,js,go,rs,json}"]
---

# RAG Systems & LLM Safety Rules

## 1. Grounding & Hallucination Prevention
- **Strict Context Attribution**: The LLM must be instructed to answer strictly based on retrieved reference chunks.
- **Explicit Fallback**: If the retrieved documents do not contain the answer, the model must output an explicit fallback (e.g. "I do not have sufficient information in the provided context") rather than speculating or inventing facts.
- **Mandatory Chunk Citations**: Include source identifiers or document IDs in the response when answering from RAG data.

## 2. Privacy, PII & Cost Optimization
- **PII Scrubbing**: Scrub personally identifiable information (emails, phone numbers, SSNs, credit cards) before sending user text to external third-party LLM APIs.
- **Stream Generation**: Always use streaming (`stream=True`) for user-facing chat applications to reduce time-to-first-token (TTFT) latency.
- **Prompt Caching**: Structure static prompt instructions at the beginning of API payloads to take advantage of provider prefix/prompt caching.
