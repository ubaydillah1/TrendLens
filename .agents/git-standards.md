# 📦 Git Commit & Version Control Standards

This document establishes the **industry-standard Git workflow, atomic commit rules, and conventional commit specifications** for all developers and AI agents operating in this repository.

---

## 1. 🎯 Core Principle: Atomic Commits

> **"One logical change per commit."**

AI agents and developers must adhere to the following boundaries:
* **No Mega-Commits:** Never bundle unrelated changes (e.g., database models + AI prompt changes + Go routing) into a single commit.
* **No Broken Commits:** Every commit must represent a working, syntactically valid state of the application.
* **No Accidental Secrets:** Never commit `.env` files, API keys, credentials, or local virtual environments (`.venv`).
* **Clean Working Tree:** Never commit temporary scratchpads, debug prints (`print()`, `fmt.Println()`), or untracked test dumps.

---

## 2. 📝 Conventional Commits Specification (v1.0.0)

Every commit message must follow this exact structure:

```
<type>(<scope>): <short summary in imperative mood>

[optional body explaining 'why' and context]

[optional footer(s), e.g., references to issues]
```

### Allowed Types

| Type | When to Use | Example |
| :--- | :--- | :--- |
| **`feat`** | A new user-facing feature or domain capability | `feat(agent): implement cross-synthesis matching node` |
| **`fix`** | A bug fix or error resolution | `fix(alembic): resolve circular import in models init` |
| **`refactor`**| Code change that neither fixes a bug nor adds a feature | `refactor(py-be): extract timestamp mixin into base model` |
| **`docs`** | Documentation only changes | `docs: add architecture rules and git standards` |
| **`test`** | Adding missing tests or correcting existing tests | `test(agent): add pytest for hook schema validation` |
| **`chore`** | Maintenance, package config, repo setup, gitignore | `chore: initialize repo and configure root gitignore` |
| **`perf`** | Code change that improves performance or latency | `perf(scraper): add parallel fetching for youtube trends` |
| **`ci`** | Changes to CI/CD workflows and pipelines | `ci: add github action for ruff and go vet` |

### Allowed Scopes
Scopes identify the area of the monorepo being modified:
* `go-be` — Golang Gin backend
* `py-be` — Python FastAPI backend
* `agent` — LangGraph flows, prompts, nodes, tools
* `db` — Database schemas, migrations (Alembic / SQL)
* `api` — API routing and request/response contracts
* `config` — Environment configurations, settings, Docker

---

## 3. ✍️ Formatting Rules for the Subject Line

1. **Use the Imperative Mood:**
   * ✅ `feat(py-be): add health check endpoint`
   * ❌ `feat(py-be): added health check endpoint`
   * ❌ `feat(py-be): adds health check endpoint`
2. **Lowercase Only:** Do not capitalize the first letter after the colon.
3. **No Period at the End:** Do not end the subject line with a `.`.
4. **Length Limit:** Keep the subject line under **72 characters**.

---

## 4. 🤖 AI Agent Execution Boundaries

When an AI agent is instructed to make commits:
1. **Review Diff First:** Run `git status` and `git diff --staged` before running `git commit`. Ensure no unwanted files are staged.
2. **Stage Intentionally:** Use explicit paths `git add <path>` rather than blindly executing `git add .` if untracked temporary files exist.
3. **Commit Milestone Trigger:** Commit only upon completing a distinct milestone or verifiable unit of work (e.g., schema created, migration applied, node tested). Do not commit halfway through a broken edit.
