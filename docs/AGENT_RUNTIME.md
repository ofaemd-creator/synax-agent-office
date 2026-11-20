# SYNAX Agent Runtime & Orchestration (`docs/AGENT_RUNTIME.md`)

```
================================================================================
           SYNAX MULTI-AGENT EXECUTION RUNTIME & PIPELINE PROTOCOL
================================================================================
```

## 1. Multi-Agent Roster & Capabilities

The SYNAX 3D Agent Office hosts 8 specialized agents, each possessing an isolated process control block, capability permissions, and domain tools:

1. **Masa 1: `synax-llm` (Hub & Orchestration)**
   - Engine: SYNAX-LLM v6.0 + Groq LPU fallback.
   - Responsibilities: Natural language query parsing, Turkish morphology normalization, task decomposition, and dispatching subtasks across the office.
2. **Masa 2: `agent-scholar` (Academic Literature & PRISMA)**
   - Capabilities: NCBI PubMed E-Utilities, CrossRef REST API, PICO formulation, dynamic PRISMA flow matrix generation.
3. **Masa 3: `agent-biostat` (Meta-Analysis & Critique)**
   - Capabilities: Inverse-variance weighting, DerSimonian-Laird random effects, Cochran's $Q$, Higgins $I^2$, ASCII forest plots, IMRaD manuscript drafting.
4. **Masa 4: `biomed-autocal` (Lyapunov Sensor Calibration)**
   - Capabilities: Discrete Lyapunov stability energy decay ($V_{k+1} < V_k$), baseline drift suppression for ICU ECG/IBP hemodynamics.
5. **Masa 5: `egraph-prover` (Interval Prover & E-Graph)**
   - Capabilities: Static IEEE-754 interval abstract interpretation, overflow bounds verification, verification certificate signing.
6. **Masa 6: `token-shield` (AST Compression Shield)**
   - Capabilities: AST skeletonization, whitespace pruning, context compression yielding 75%-90% token reduction.
7. **Masa 7: `context-vault` (Cryptographic State Vault)**
   - Capabilities: SHA-256 state capsules (<180 tokens), cross-session and cross-agent zero-token context handoffs.
8. **Masa 8: `silicon-studio` (FullStack & Silicon Codegen)**
   - Capabilities: Automated TDD unit test synthesis, C11/ARM64 NEON/AVX2/Q16.16 hardware emission, OWASP security audit.

---

## 2. Execution Pipeline Protocol

```
Operator Query: "Analyze intensive care hemodynamics and verify zero-drift bounds"
                                    |
                                    v
                       [Masa 1: Orchestration Hub]
                     Decomposes into 3-Agent DAG
                                    |
            +-----------------------+-----------------------+
            | Stage 1: Research                             |
            v                                               |
  [Masa 2: Agent-Scholar]                                   |
  - Live PubMed & CrossRef Query                            |
  - Dynamic PRISMA Flow (2 Screened, 0 Duplicates)          |
  - Outputs Verified Evidence Matrix                        |
            |                                               |
            | (Passes Verified Study Records)               |
            v                                               |
  [Masa 3: Agent-Biostat]                                   |
  - Computes DerSimonian-Laird Pooling                      |
  - theta_DL = 0.816, tau^2 = 0.0039, I^2 = 40.0%           |
  - Generates Reproducible Python Script                    |
            |                                               |
            | (Passes Python Script + Expected Results)     |
            v                                               |
  [Masa 5/8: Agent-Verifier]                                |
  - Enters WAITING_FOR_APPROVAL Checkpoint                  |
  - Operator Confirms Execution                             |
  - Executes Script in SynaxRestrictedSandbox               |
  - Asserts Discrepancy == 0.000                            |
  - Signs VerificationCertificate (Status: VERIFIED)        |
            |                                               |
            +-----------------------+-----------------------+
                                    |
                                    v
                     Final Verified Research Report
```
