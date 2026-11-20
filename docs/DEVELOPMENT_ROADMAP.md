# SYNAX Sovereign Agentic OS Development Roadmap (`docs/DEVELOPMENT_ROADMAP.md`)

```
================================================================================
                    SYNAX ROADMAP: V6.2 → V7.0 SOVEREIGN RELEASE
================================================================================
```

## Phase 0: Discovery & Baseline (Completed - v6.2)
- [x] Complete repository audit and test baseline.
- [x] Elimination of fabricated scientific figures, mock effect sizes, and hardcoded PRISMA counts.
- [x] Introduction of `VerificationCertificate` and formal verification state model (`verification.py`).
- [x] AST-audited isolated Python sandbox (`sandbox.py`).
- [x] Microkernel architecture: PCB, preemptive scheduler, IPC bus, VAFS (`src/synax/kernel/`).

## Phase 1: Real Multi-Agent Orchestration (Completed - v6.2)
- [x] Formal 3-Agent execution pipeline: Research (Scholar) -> Analysis (Biostat) -> Verification (Verifier).
- [x] Task state machine: `QUEUED → RUNNING → VERIFYING → COMPLETED/FAILED/WAITING_FOR_APPROVAL`.
- [x] Safe installer scripts eliminating dangerous process terminations (`install-desktop.sh`, `install-desktop.ps1`).
- [x] Portable MCP server configuration (`.mcp.json`).

## Phase 2: Compiler & Hardware Integration (In Progress - v6.3)
- [ ] Direct AST compilation of `.sx` kernel source into C11, ARM64 NEON, and AVX2 via native SYNAX compiler.
- [ ] Hardware-in-the-loop (HIL) verification of discrete Lyapunov drift suppression on embedded MCU boards.
- [ ] Automated regression testing against IEEE-754 floating-point test suites.

## Phase 3: Distributed Swarm & Multi-Host Fabric (v7.0)
- [ ] ZeroMQ / gRPC distributed IPC across networked workstation nodes.
- [ ] Decentralized Context Vault using content-addressable storage (IPFS / libp2p).
- [ ] Multi-tenant isolation with Linux cgroups v2 and container namespaces.
