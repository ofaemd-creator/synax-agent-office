# SYNAX Sovereign Agentic OS Architecture (`docs/ARCHITECTURE.md`)

```
================================================================================
           SYNAX-OS: SOVEREIGN AGENTIC OPERATING SYSTEM ARCHITECTURE
================================================================================
```

## 1. Executive Summary

SYNAX-OS transforms the SYNAX multi-agent ecosystem from an experimental UI prototype into a production-grade, mathematically verified, sovereign agentic operating system. Built upon a preemptive microkernel, capability-based security model, restricted AST execution sandbox, and formal interval abstract interpretation, SYNAX-OS provides deterministic coordination across heterogeneous AI models (Claude Code, OpenAI Codex, Google Antigravity, and SYNAX-LLM).

---

## 2. Kernel & Process Model

The SYNAX Kernel (`src/synax/kernel/`) implements operating system fundamentals mapped directly to autonomous AI agents:

```
+-------------------------------------------------------------------------+
|                              USER SPACE                                 |
|   +-------------------+  +--------------------+  +------------------+   |
|   | Agent-Scholar     |  | Agent-Biostat      |  | Agent-Verifier   |   |
|   | (Literature & PM) |  | (Meta-Analysis DL) |  | (Formal Bounds)  |   |
|   +---------+---------+  +---------+----------+  +--------+---------+   |
|             |                      |                      |             |
|   +---------v----------------------v----------------------v---------+   |
|   |             SYNAX System Call Interface (syscalls)              |   |
|   |  sys_spawn(), sys_kill(), sys_send(), sys_recv(), sys_exec_tool()|  |
+---+-----------------------------------------------------------------+---+
|                              KERNEL SPACE                               |
|   +-------------------+  +--------------------+  +------------------+   |
|   | Process Control   |  | Preemptive RR      |  | IPC Message Bus  |   |
|   | Block (PCB) Table |  | Priority Scheduler |  | Mailboxes/Queues |   |
|   +-------------------+  +--------------------+  +------------------+   |
|   +-----------------------------------------------------------------+   |
|   | Virtual Agent File System (VAFS)                                |   |
|   | /proc/agents/ · /dev/tools/ · /sys/kernel/ · /var/tasks/        |   |
|   +-----------------------------------------------------------------+   |
|   +-----------------------------------------------------------------+   |
|   | Hardware Abstraction Layer & Restricted Sandboxing (HAL)        |   |
|   | AST Auditor · Resource Quotas · RLIMIT · Signal Handlers        |   |
+---+-----------------------------------------------------------------+---+
```

### 2.1 Process State Machine
Every agent process transitions across standard OS states:
- `NEW`: Process initialized, PCB allocated with PID, token budget, and capability set.
- `READY`: Scheduled and placed in the priority run queue.
- `RUNNING`: Actively executing a prompt turn, tool call, or reasoning step.
- `SLEEPING`: Blocked on asynchronous I/O, network API, or timer event.
- `BLOCKED`: Awaiting human authorization checkpoint or inter-process IPC message.
- `TERMINATED`: Successfully completed task with exit code 0.
- `ZOMBIE`: Completed execution awaiting parent process harvest (`sys_wait`).

### 2.2 Virtual Agent File System (VAFS)
- `/proc/agents/<pid>/status`: Live execution state, CPU cycles, tokens consumed.
- `/proc/agents/<pid>/io`: Input/output streams and telemetry.
- `/dev/tools/<tool_name>`: Device nodes exposing vetted capabilities (PubMed, Python sandbox, E-Graph prover).
- `/sys/kernel/stats`: Uptime, active process count, total token allocation.
- `/var/tasks/<task_id>`: Persistent execution records and signed verification certificates.

---

## 3. Subsystem Breakdown

### 3.1 Formal Verification & Interval Abstract Interpretation (`verification.py`)
Replaces unverified hashes with an authentic verification state machine:
`NOT_TESTED → SIMULATED → TESTED → VERIFIED → FAILED`.
- Discrete Lyapunov Contractivity: Proves energy decay $V_{k+1} < V_k$ for autonomous sensor drift suppression.
- IEEE-754 Interval Arithmetic: Verifies bounds $[L, U]$ under floating-point semantics.
- VerificationCertificate: Dataclass capturing verifier version, assumptions, domain bounds, and regulatory disclaimers.

### 3.2 Secure Code Execution Sandbox (`sandbox.py`)
- `ASTSafetyAuditor`: Walks abstract syntax trees to reject unauthorized imports (`os`, `subprocess`, `socket`, `pty`) and dangerous built-ins (`eval`, `exec`).
- `SynaxRestrictedSandbox`: Runs in isolated disposable temporary directories with CPU time limits (`RLIMIT_CPU`), memory limits (`RLIMIT_AS`), process quotas, and explicit user approval gates.

### 3.3 Multi-Agent Research & Analysis Pipeline (`agent_pipeline.py`)
A verified 3-stage execution pipeline:
1. **Agent-Scholar (Research):** Queries NCBI PubMed & CrossRef for genuine bibliographic metadata and tracks dynamic PRISMA flows without numeric hallucination.
2. **Agent-Biostat (Analysis):** Executes DerSimonian-Laird random-effects pooling ($\tau^2$, Cochran's $Q$, $I^2$) and produces reproducible Python scripts.
3. **Agent-Verifier (Verification):** Executes generated code inside the restricted sandbox, verifies numerical agreement with Stage 2 calculations, and issues a formal verification certificate.

### 3.4 User Interface: 2.5D Isometric Diorama & Window Manager
- Accurately categorized as a high-fidelity 2.5D Isometric Canvas Engine with custom pixel artwork and themeable workstation dioramas.
- Backed by the SYNAX-OS Desktop Window Manager (`os_app.py`) providing draggable process windows, process monitors (`top`), and interactive shells (`synax-sh`).
