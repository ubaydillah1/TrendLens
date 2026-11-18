# 📝 Code Documentation & Commenting Standards

This document establishes the **professional code documentation and commenting standards** for all Python and Go code in the `trendlens` repository.

---

## 1. 🎯 Golden Rule: Explain "Why", Not "What"

> **"Code tells you how; comments should tell you why."**

* ❌ **Bad (Obvious / Noisy):**
  ```python
  # 1. Initialize the LLM
  llm = ChatGoogleGenerativeAI(...)
  # 2. Create prompt
  prompt = ChatPromptTemplate(...)
  ```
* ✅ **Good (Contextual / Professional):**
  ```python
  # Gemini 3.5 Flash Lite is prioritized for high-throughput synthesis
  # without hitting 503 capacity limits on free/dev tiers.
  llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", ...)
  ```

---

## 2. 🚫 Prohibited Commenting Patterns

1. **No Numbered Tutorial Comments:**
   * Avoid `# 1. Step one`, `# 2. Step two`. Production code is not a tutorial blog post.
2. **No Redundant Comments:**
   * Do not write comments that merely rephrase the function or variable name.
   * ❌ `user_id = 123  # Set user id to 123`
3. **No Non-English Comments:**
   * All docstrings, inline comments, commit messages, and PR descriptions must be written in **English**.
4. **No Zombie Code:**
   * Do not leave commented-out blocks of code (`# old_function()`). Rely on Git history instead.

---

## 3. 📄 Standard Docstring Conventions (PEP 257 / Google Style)

Every public module, class, and node function must have a standardized docstring:

```python
def synthesis_node(state: ResearchAgentState) -> dict[str, Any]:
    """Synthesizes raw viral trends and technical news into structured content ideas.

    Marries social media hook patterns with engineering news, filtering the output
    through the creator's specific brand positioning.

    Args:
        state: Graph state containing raw trends, news, niche, and user positioning.

    Returns:
        Dictionary updating 'final_report' with the validated DailyResearchReport payload.
    """
```

---

## 4. 💡 When Inline Comments ARE Encouraged

Use inline comments strictly for:
* **Workarounds & Fallbacks:** Explaining why a specific fallback exists (e.g., fallback timestamp or model selection).
* **Non-obvious Domain Logic:** Explaining a complex algorithm, regex, or metric ratio.
* **External Integration Quirks:** Documenting third-party API rate limits, header requirements, or schema workarounds.
