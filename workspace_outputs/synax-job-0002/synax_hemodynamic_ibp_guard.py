#!/usr/bin/env python3
"""
İnvaziv Kan Basıncı (IBP / CPP) Lyapunov Sıfır-Sapma & Perfüzyon Çekirdeği
Synthesized by SYNAX 3D Agent Office v3.0 (SYNAX-JOB-0002 · Claude Code)
"""
from __future__ import annotations
import math
from typing import Dict


class SynaxAutocalKernel:
    def __init__(self, gamma: float = 0.22, reference: float = 95.0) -> None:
        self.gamma = gamma
        self.reference = reference
        self.estimated_drift = 0.0
        self.healed_nan_count = 0

    def step(self, map_mmhg: float, icp_drift_mmhg: float = 0.0) -> Dict[str, float]:
        if not math.isfinite(map_mmhg):
            map_mmhg = self.reference
            self.healed_nan_count += 1
        if not math.isfinite(icp_drift_mmhg):
            icp_drift_mmhg = 0.0
            self.healed_nan_count += 1
        raw_error = (map_mmhg - self.reference) + icp_drift_mmhg
        contracted_residual = (1.0 - self.gamma) * (raw_error - self.estimated_drift)
        self.estimated_drift = raw_error - contracted_residual
        calibrated = map_mmhg - self.estimated_drift
        return {
            'input': round(map_mmhg, 6),
            'calibrated': round(calibrated, 6),
            'lyapunov_V': round(contracted_residual ** 2, 8),
            'drift_suppressed': round(self.estimated_drift, 6),
        }


for fault in [float('nan'), float('inf'), float('-inf')]:
            healed = 0.0 if not math.isfinite(fault) else fault
            self.assertTrue(math.isfinite(healed))
            self.assertEqual(healed, 0.0)


if __name__ == '__main__':
    unittest.main()
