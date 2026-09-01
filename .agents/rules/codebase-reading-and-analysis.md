---
description: Rules for analyzing, reading, exploring, and navigating codebases efficiently without making unfounded assumptions
globs: ["**/*"]
---

# Codebase Reading & Deep Analysis Rules

## 1. Grounded Analysis over Assumptions
- **Never Guess API Contracts**: Always read the source definition or type signature before using or modifying a function, interface, or module.
- **Trace Before Editing**: Before refactoring a function, find all call sites (`grep`) to understand downstream impacts and prevent regression.
- **Verify with Tests**: When in doubt about how a legacy feature works, inspect its corresponding unit tests in `tests/` to understand the intended behavior.

## 2. Token-Efficient Exploration
- Use directory listing (`list_dir`) to understand project topology first.
- Use pattern searching (`grep_search`) to locate relevant code blocks instead of viewing entire folders file by file.
- View specific line slices (e.g. lines 1 to 60) for large files (> 500 lines) rather than dumping whole multi-megabyte files into memory.

## 3. Preservation of Code Integrity
- Preserve existing comments, docstrings, licensing headers, and style conventions unless explicitly directed to change them.
- Follow the existing codebase's formatting rules (e.g. tabs vs spaces, quotes, naming conventions).
