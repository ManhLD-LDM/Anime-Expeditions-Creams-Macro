---
description: Design patterns for autonomous agents, tool execution safety, context budgeting, and multi-agent coordination
globs: ["**/*.{py,ts,js,go,rs,json}"]
---

# AI Agent Design & Tool Calling Rules

## 1. Tool Execution Safety
- **Validate Arguments First**: Always validate tool inputs with strict schemas (Pydantic/Zod) before executing external APIs or database commands.
- **Graceful Tool Errors**: Tools must catch exceptions and return informative error strings rather than throwing unhandled exceptions that crash the agent.
- **Maximum Retry Limit**: Cap tool retry loops at **3 iterations** on failures to prevent infinite execution loops and compute exhaustion.

## 2. Context Window & Token Budgeting
- **No Unbounded Context Dumping**: Never inject raw multi-megabyte log files, whole database dumps, or 50+ source files into an LLM prompt. Use chunking, summaries, or vector search.
- **Structured XML Prompts**: Structure system prompts and few-shot exemplars with XML tags (`<context>`, `<rules>`, `<instructions>`) to guard against prompt injection.
