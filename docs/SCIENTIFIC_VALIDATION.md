# SYNAX Scientific Integrity & Mathematical Validation (`docs/SCIENTIFIC_VALIDATION.md`)

```
================================================================================
              SYNAX SCIENTIFIC INTEGRITY & BIOSTATISTICAL PROTOCOL
================================================================================
```

## 1. Guiding Principles & Anti-Hallucination Policy

1. **No Data Fabrication:** Under no circumstance will SYNAX agents invent sample sizes ($N$), standard errors ($SE$), effect sizes ($d$), PMIDs, or DOIs.
2. **Explicit Verification States:** All scientific and numerical artifacts carry explicit verification status:
   - `NOT_TESTED`: Unverified assertion or proposal.
   - `SIMULATED`: Numerical simulation under idealized assumptions.
   - `TESTED`: Evaluated against an empirical test suite.
   - `VERIFIED`: Mathematically or formally checked with invariant assertions.
   - `FAILED`: Violated formal boundary or stability constraint.
3. **Data Sufficiency Gate (`INSUFFICIENT_VERIFIED_DATA`):** If fewer than two verified empirical studies are available, the Biostat agent halts quantitative pooling and reports qualitative synthesis only.

---

## 2. DerSimonian-Laird Random-Effects Estimator Formulation

Let $k$ be the number of studies, $y_i$ the observed effect size in study $i$, and $v_i = SE_i^2$ the within-study variance.

1. **Fixed-Effect Weights:**
   $$w_i = \frac{1}{v_i}, \quad S_1 = \sum_{i=1}^k w_i, \quad S_2 = \sum_{i=1}^k w_i^2$$

2. **Fixed-Effect Pooled Estimate:**
   $$\hat{\theta}_{\text{fixed}} = \frac{\sum_{i=1}^k w_i y_i}{S_1}$$

3. **Cochran's $Q$ Statistic & Degrees of Freedom:**
   $$Q = \sum_{i=1}^k w_i (y_i - \hat{\theta}_{\text{fixed}})^2, \quad df = k - 1$$

4. **DerSimonian-Laird Between-Study Variance $\tau^2$:**
   $$c = S_1 - \frac{S_2}{S_1}, \quad \tau^2 = \max\left(0, \frac{Q - df}{c}\right)$$

5. **Random-Effects Weights & Pooled Estimator:**
   $$w_i^* = \frac{1}{v_i + \tau^2}, \quad \hat{\theta}_{\text{random}} = \frac{\sum_{i=1}^k w_i^* y_i}{\sum_{i=1}^k w_i^*}, \quad SE(\hat{\theta}_{\text{random}}) = \sqrt{\frac{1}{\sum_{i=1}^k w_i^*}}$$

6. **Heterogeneity Index ($I^2$):**
   $$I^2 = \max\left(0, \frac{Q - df}{Q}\right) \times 100\%$$

---

## 3. Discrete Lyapunov Contractivity for Sensor Drift Elimination

For sensor telemetry error $e_k = x_k - x_{\text{nominal}}$:
- **Lyapunov Energy Candidate:** $V_k = e_k^2 \ge 0$.
- **Error Dynamics:** $e_{k+1} = (1 - \gamma) e_k$, where $\gamma \in (0, 1)$ is the convergence parameter.
- **Energy Evolution:**
  $$V_{k+1} = e_{k+1}^2 = (1 - \gamma)^2 e_k^2 = (1 - \gamma)^2 V_k$$
- **Contractivity Condition:**
  Since $0 < \gamma < 1$, $(1 - \gamma)^2 < 1$, which strictly guarantees:
  $$V_{k+1} < V_k \quad \forall e_k \neq 0$$
  This proves asymptotic exponential convergence of sensor baseline drift to zero.
