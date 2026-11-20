# SYNAX Sovereign Agentic OS Security Model (`docs/SECURITY_MODEL.md`)

```
================================================================================
             SYNAX ZERO-TRUST AGENTIC SECURITY & SANDBOX SPECIFICATION
================================================================================
```

## 1. Threat Model & Security Boundaries

In an autonomous multi-agent environment where LLMs generate code, evaluate literature, and execute system commands, security cannot rely on post-hoc filtering. SYNAX-OS implements a multi-layered defense-in-depth security model:

```
+-------------------------------------------------------------------------+
| Layer 1: Prompt & Secret Sanitization                                   |
| - Strips API keys, bearer tokens, passwords before logging or caching   |
| - Memory vault encrypts state in volatile ramdisks                      |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Layer 2: Abstract Syntax Tree (AST) Safety Auditor (`sandbox.py`)       |
| - Rejects dangerous imports: os, posix, subprocess, socket, pty, ctypes |
| - Forbids dangerous built-ins: eval(), exec(), __import__(), compile()  |
| - Blocks attribute invocations: .system(), .popen(), .spawn(), .unlink()|
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Layer 3: Human Authorization & Checkpoint Gate                          |
| - Sensitive tasks pause at WAITING_FOR_APPROVAL state                   |
| - Explicit operator confirmation required prior to sandboxed execution  |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Layer 4: Restricted Disposable Workspace Sandbox                        |
| - Temporary isolated directory (mkdtemp) destroyed immediately upon exit|
| - Resource quotas: strict CPU execution time limits (RLIMIT_CPU)        |
| - Memory limits (RLIMIT_AS) preventing Denial of Service (DoS) memory bombs
| - Process count limits (RLIMIT_NPROC) preventing fork-bombs             |
+-------------------------------------------------------------------------+
```

---

## 2. Capability-Based Access Control

Each agent in SYNAX-OS operates under least-privilege capability manifests:

| Agent Identifier | Role | Allowed System Calls | Network Access | Code Execution |
| :--- | :--- | :--- | :--- | :--- |
| `agent-scholar` | Literature Review | `sys_send`, `sys_recv`, `sys_exec_tool` (PubMed/CrossRef) | Read-only (REST API) | Denied |
| `agent-biostat` | Statistical Analysis | `sys_send`, `sys_recv` | Denied | Denied |
| `agent-verifier` | Formal Verification | `sys_send`, `sys_recv`, `sys_exec_tool` (Sandbox) | Denied | Contained Sandbox |
| `biomed-autocal` | Sensor Calibration | `sys_send`, `sys_recv` | Denied | Denied |
| `egraph-prover` | E-Graph Optimization | `sys_send`, `sys_recv` | Denied | Denied |
| `token-shield` | AST Skeletonizer | `sys_send`, `sys_recv` | Denied | Denied |
| `context-vault` | Memory Storage | `sys_send`, `sys_recv` | Denied | Denied |
| `silicon-studio` | TDD & Codegen | `sys_send`, `sys_recv`, `sys_exec_tool` (TDD) | Denied | Contained Sandbox |

---

## 3. Secret Management & Storage

- **Zero Plaintext Credentials:** API keys are never stored in browser `localStorage` or unencrypted configuration files.
- **Environment Isolation:** Keys are supplied via OS environment variables (`GROQ_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) and scrubbed from error logs and stack traces.
- **Desktop Security:** For standalone desktop installations, OS-native keychains (macOS Keychain, Windows Credential Manager) are utilized.
