# 🤖 TrendLens Agent Workspace Rules

These guidelines govern how AI agents operate within the `trendlens` repository.

---

## 1. 🏗️ Repository Architecture
* **`go-be/`**: Core backend service built with Golang & Gin. Responsible for Auth, user management, scheduling, and client APIs.
* **`py-be/`**: AI Agent service built with FastAPI, LangGraph, and Alembic. Responsible for intelligent research, trend analysis, and synthesis.
* **`fastapi/` & `Golang-Learn/`**: Ignored legacy/playground directories. Never modify or commit code into these folders.

---

## 2. 📜 Standards & Guidelines Reference
* **Git Standards:** Follow all rules in [git-standards.md](file:///c:/Users/Ubay%20Dillah/Documents/Pemrograman/On%20Going/trendlens/.agents/git-standards.md).
* **Python Backend Architecture:** Follow strict rules in [py-be/ARCHITECTURE_RULES.md](file:///c:/Users/Ubay%20Dillah/Documents/Pemrograman/On%20Going/trendlens/py-be/ARCHITECTURE_RULES.md).
* **Project Roadmap:** Follow the phases outlined in [PROJECT_PLAN.md](file:///c:/Users/Ubay%20Dillah/Documents/Pemrograman/On%20Going/trendlens/PROJECT_PLAN.md).

---

## 3. ⚠️ Safety & Operational Constraints
* **Never Run Dev Servers in Background:** Never execute commands like `pnpm run dev`, `npm run dev`, or long-running development servers unless explicitly requested by the user.
* **Separation of Concerns:** Keep business logic inside services, routing inside endpoints, and AI reasoning inside agent graphs.
* **Migrations:** Never alter database schemas directly; always use migration tools (Alembic for `py-be`).
