# CLAUDE.md Best Practices

## Purpose
CLAUDE.md is the primary way to give Claude Code project-specific context. It acts as a "briefing document" loaded at conversation start.

## Recommended Sections

### 1. Project Context
- Project name and one-line description
- Business domain and purpose
- Current status (active development, maintenance, migration, etc.)

### 2. Tech Stack
- Languages and versions
- Frameworks and major libraries
- Database type and version
- Infrastructure (cloud provider, containers, CI/CD)

### 3. Project Structure
- Key directories and what they contain
- Entry points and important files
- Naming conventions

### 4. Development Commands
- How to build/run the project
- How to run tests
- How to lint/format
- How to deploy (if applicable)

### 5. Technical Constraints and Rules
- Version requirements or restrictions
- Coding standards and patterns to follow
- Things to avoid or be careful about
- Security considerations

### 6. Architecture Notes (optional)
- Key design decisions
- Data flow overview
- Integration points with external systems

## Guidelines
- Keep under 200 lines for the main file (truncation occurs after that)
- Be concise: Claude is smart, only include what it can't infer
- Use imperative form ("Use X" not "You should use X")
- Focus on constraints and rules, not tutorials
- Update regularly as the project evolves
- For detailed reference material, link to separate files

---

Copyright 2026 simplesoft, Inc. Licensed under the [Apache License, Version 2.0](../LICENSE).
