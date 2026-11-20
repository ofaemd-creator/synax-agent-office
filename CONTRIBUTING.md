# Contributing to SYNAX 3D Agent Office & Super-LLM Platform

Thank you for your interest in contributing to **SYNAX Agent Office**! We welcome contributions from AI researchers, frontend 3D WebGL developers, biomedical engineers, systems programmers, and documentation contributors.

---

## 1. Core Principles

1. **Agent-First Architecture:** Domain tasks belong to specialized agents (Biomedical, E-Graph Prover, Token Shield, Context Vault, Full-Stack Dev, Telegram Ops, Academic Scholar, Tycoon Coordinator).
2. **Strict Immutability:** Always return new state copies; never mutate objects in-place.
3. **Verified Zero-Hallucination:** All biomedical and academic references must be backed by live PubMed/CrossRef citations with real PMIDs/DOIs.
4. **Comprehensive Test Coverage:** Every PR must include unit tests achieving 80%+ test coverage.

---

## 2. Development Setup

### Prerequisites
- Python 3.10+ (Python 3.11 or 3.12 recommended)
- Modern web browser with WebGL 2.0 support (Chrome, Safari, Firefox, Edge)
- Git & GitHub CLI (`gh`)

### Forking & Local Setup

1. **Fork the Repository:**
   Click the **Fork** button at the top right of [https://github.com/ofaemd-creator/synax-agent-office](https://github.com/ofaemd-creator/synax-agent-office) or navigate to [https://github.com/ofaemd-creator/synax-agent-office/fork](https://github.com/ofaemd-creator/synax-agent-office/fork) to create your personal copy.

2. **Clone Your Fork:**
   ```bash
   git clone https://github.com/<your-username>/synax-agent-office.git
   cd synax-agent-office
   ```

3. **Configure Upstream Remote:**
   Connect your local repository to the upstream main repository to stay up to date:
   ```bash
   git remote add upstream https://github.com/ofaemd-creator/synax-agent-office.git
   git remote -v
   ```

4. **Syncing with Upstream:**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

5. **Install Dependencies & Verify Tests:**
   ```bash
   pip install -r requirements.txt
   python3 -m unittest discover -s tests -v
   ```

---

## 3. Pull Request Guidelines

1. **Branch Naming:**
   - Features: `feat/<short-description>`
   - Fixes: `fix/<short-description>`
   - Documentation: `docs/<short-description>`
2. **Follow PR Template:** Complete all sections of `.github/pull_request_template.md`.
3. **Verify CI:** Ensure both Ubuntu and macOS CI passes before requesting review.
4. **No Secrets:** Never commit API keys, personal tokens, or production passwords.

---

## 4. Community Standards & Code of Conduct

All contributors are expected to uphold the [Code of Conduct](CODE_OF_CONDUCT.md). Please report any violations to `dev@synaxcode.com`.
