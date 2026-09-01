---
description: Technical documentation formatting, markdown hygiene, docstrings, and knowledge consistency standards
globs: ["**/*.md", "**/*.mdx", "docs/**"]
---

# Technical Documentation & Markdown Standards

## 1. Markdown Formatting & Typography
- **Heading Hierarchy**: Maintain a clean single `# H1` at top, followed sequentially by `## H2` and `### H3`. Never skip heading levels.
- **GitHub-Flavored Alerts**: Use alerts strategically to emphasize critical details:
  - `> [!NOTE]` for background context and helpful explanations.
  - `> [!TIP]` for performance and workflow optimization tips.
  - `> [!IMPORTANT]` for crucial requirements or must-know prerequisites.
  - `> [!WARNING]` for breaking changes, deprecations, and potential traps.
- **Code Blocks**: Always declare the language identifier on fenced code blocks (```python, ```typescript, ```bash, ```json, ```mermaid).

## 2. Docstrings & In-Code Comments
- **Document the "Why" and "Gotchas"**: Do not write trivial comments that simply restate the function name (e.g. `// calculate total - calculates the total`). Instead, document business rationales, tricky mathematical formulas, boundary quirks, and concurrency assumptions.
- **Param & Return Types**: In typed languages (TypeScript, Python with type annotations), avoid redundant type repetition in JSDoc/docstrings; focus on field semantics and constraints.

## 3. Synchronous Documentation Updates
- Whenever modifying an API route, configuration key, or CLI command, update the corresponding `README.md`, `docs/`, or OpenAPI specification in the same commit to prevent documentation drift.
