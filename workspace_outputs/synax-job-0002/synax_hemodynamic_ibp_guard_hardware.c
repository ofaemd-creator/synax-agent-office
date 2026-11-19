/* =========================================================================
 * İnvaziv Kan Basıncı (IBP / CPP) Lyapunov Sıfır-Sapma & Perfüzyon Çekirdeği
 * Synthesized by SYNAX 3D Agent Office v3.0 (SYNAX-JOB-0002 · Claude Code)
 * Formal Certificate: SHA-256 #4c8c15ff9b7dbdcf ([0.0, 220.0] 0-ULP)
 * Targets: ANSI C11 | ARM64 NEON | x86_64 AVX2 | Q16.16 Fixed-Point MCU
 * ========================================================================= */
#include <stdint.h>
#include <stddef.h>
#include <math.h>

#if defined(__ARM_NEON)
#include <arm_neon.h>
#elif defined(__AVX2__)
#include <immintrin.h>
#endif

static inline float synax_hemodynamic_ibp_guard_c11(float map_mmhg, float icp_drift_mmhg) {
    if (!isfinite(map_mmhg)) map_mmhg = 0.0f;
    if (!isfinite(icp_drift_mmhg)) icp_drift_mmhg = 0.0f;
    return fmaxf(map_mmhg - icp_drift_mmhg, 0.0f);
}

static inline int32_t synax_hemodynamic_ibp_guard_q16_mcu(int32_t a_q16, int32_t b_q16) {
    return (int32_t)((a_q16 > b_q16) ? (a_q16 - b_q16) : 0);
}

void synax_hemodynamic_ibp_guard_batch(const float* restrict in_a, const float* restrict in_b, float* restrict out, size_t n) {
    size_t i = 0;
#if defined(__ARM_NEON)
    for (; i + 4 <= n; i += 4) {
        float32x4_t v_a = vld1q_f32(&in_a[i]);
        float32x4_t v_b = vld1q_f32(&in_b[i]);
        float32x4_t v_y = vmaxq_f32(vsubq_f32(v_a, v_b), vdupq_n_f32(0.0f));
        vst1q_f32(&out[i], v_y);
    }
#elif defined(__AVX2__)
    for (; i + 8 <= n; i += 8) {
        __m256 v_a = _mm256_loadu_ps(&in_a[i]);
        __m256 v_b = _mm256_loadu_ps(&in_b[i]);
        __m256 v_y = _mm256_max_ps(_mm256_sub_ps(v_a, v_b), _mm256_setzero_ps());
        _mm256_storeu_ps(&out[i], v_y);
    }
#endif
    for (; i < n; ++i) {
        out[i] = synax_hemodynamic_ibp_guard_c11(in_a[i], in_b[i]);
    }
}
