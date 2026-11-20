# SYNAX 3D Agent Office — Custom Agents Specification

This repository defines 8 autonomous domain specialist agents and 1 master reasoning agent for **SYNAX-OMNI v6.0 & 3D Pixar-Tycoon Agent Office**, engineered by **Dr. Ömer Faruk Aydın** ([@ofaemd-creator](https://github.com/ofaemd-creator)).

These custom agents are configured in `.github/agents/` using the official `*.agent.md` standard. They are automatically indexed by GitHub's **Agents Tab** (`/agents?author=ofaemd-creator`), GitHub Copilot, Claude Code, and OpenAI Codex.

---

## 🤖 Active Custom Agents Roster

| Agent Identifier | Display Name | Specialty & Domain Tools | Agent Definition |
| :--- | :--- | :--- | :--- |
| **`@synax-omni-super-llm`** | SYNAX-OMNI Super-LLM | Master reasoning, Perplexity Live Search, Claude Canvas & Python Sandbox | [.github/agents/synax-omni-super-llm.agent.md](.github/agents/synax-omni-super-llm.agent.md) |
| **`@synax-biomed-autocal`** | Biomedical Autocal | Contractive Lyapunov-Kalman zero-drift calibration & live PubMed efetch | [.github/agents/synax-biomed-autocal.agent.md](.github/agents/synax-biomed-autocal.agent.md) |
| **`@synax-egraph-prover`** | E-Graph Prover & Compiler | Equality saturation, formal Interval proof, ARM64/AVX2/MCU codegen | [.github/agents/synax-egraph-prover.agent.md](.github/agents/synax-egraph-prover.agent.md) |
| **`@synax-token-shield`** | Token Shield Optimizer | AST code skeletonizer, terminal log RLE deduplication (75%-92% token cut) | [.github/agents/synax-token-shield.agent.md](.github/agents/synax-token-shield.agent.md) |
| **`@synax-context-vault`** | Context Vault Handoff | Zero-token cross-agent memory handoffs via <180 token SHA-256 capsules | [.github/agents/synax-context-vault.agent.md](.github/agents/synax-context-vault.agent.md) |
| **`@synax-fullstack-dev`** | Full-Stack Architect | Three.js 3D WebGL isometric rendering, glassmorphism UI & PHP/Python backend | [.github/agents/synax-fullstack-dev.agent.md](.github/agents/synax-fullstack-dev.agent.md) |
| **`@synax-telegram-bot`** | Telegram Remote Operations | Mobile bot daemon (@synax_compiler_bot) & remote command dispatch | [.github/agents/synax-telegram-bot.agent.md](.github/agents/synax-telegram-bot.agent.md) |
| **`@synax-academic-researcher`**| Academic Scholar | Peer-reviewed PubMed search, ArXiv preprints, CrossRef DOIs & BibTeX | [.github/agents/synax-academic-researcher.agent.md](.github/agents/synax-academic-researcher.agent.md) |
| **`@synax-tycoon-architect`** | Tycoon Office Coordinator | 3D Pixar-Tycoon diorama coordinator, agent shifts, economics & computer use | [.github/agents/synax-tycoon-architect.agent.md](.github/agents/synax-tycoon-architect.agent.md) |

---

## 🛠️ Active MCP Tools

- `synax_office_multitask(prompt)` — Executes all autonomous office agents in parallel.
- `synax_super_llm_react(query)` — Executes multi-step ReAct reasoning with live PubMed citations, Python verification, and Canvas artifacts.
- `synax_token_shield_compress(content)` — Saves 75%–92% tokens via AST skeletonization & RLE deduplication.
- `synax_context_vault_handoff(task_summary)` — Seals a `<180 token` `SHA-256` memory capsule for zero-token context switching.

---

## 🚀 How to Invoke

- **On GitHub Web:** Navigate to the repository's **Agents** tab or select from the Copilot agent menu.
- **In VS Code / Cursor / Windsurf:** Use `@synax-biomed-autocal`, `@synax-egraph-prover`, etc., in the chat window.
- **In Browser (Web Edition):** Visit [https://synaxcode.com/office.html](https://synaxcode.com/office.html) to interact with each 3D agent directly.
