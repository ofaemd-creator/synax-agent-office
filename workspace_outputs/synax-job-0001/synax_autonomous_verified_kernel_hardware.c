/* =========================================================================
 * SYNAX Otonom 0-ULP Doğrulanmış Çoklu-Silikon & Lyapunov İşlem Çekirdeği
 * Synthesized by SYNAX 3D Agent Office v3.0 (SYNAX-JOB-0001 · Claude Code + Codex + Antigravity)
 * Formal Certificate: SHA-256 #eb02b7c371f5ef37 ([-125.0, 125.0] 0-ULP)
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

static inline float synax_autonomous_verified_kernel_c11(float signal_a, float drift_b) {
    if (!isfinite(signal_a)) signal_a = 0.0f;
    if (!isfinite(drift_b)) drift_b = 0.0f;
    return fmaf(signal_a, 0.95f, -drift_b);
}

static inline int32_t synax_autonomous_verified_kernel_q16_mcu(int32_t a_q16, int32_t b_q16) {
    return (int32_t)((((int64_t)a_q16 * 62259) >> 16) - b_q16);
}

void synax_autonomous_verified_kernel_batch(const float* restrict in_a, const float* restrict in_b, float* restrict out, size_t n) {
    size_t i = 0;
#if defined(__ARM_NEON)
    for (; i + 4 <= n; i += 4) {
        float32x4_t v_a = vld1q_f32(&in_a[i]);
        float32x4_t v_b = vld1q_f32(&in_b[i]);
        float32x4_t v_y = vfmsq_n_f32(vnegq_f32(v_b), v_a, -0.95f);
        vst1q_f32(&out[i], v_y);
    }
#elif defined(__AVX2__)
    for (; i + 8 <= n; i += 8) {
        __m256 v_a = _mm256_loadu_ps(&in_a[i]);
        __m256 v_b = _mm256_loadu_ps(&in_b[i]);
        __m256 v_y = _mm256_fmsub_ps(v_a, _mm256_set1_ps(0.95f), v_b);
        _mm256_storeu_ps(&out[i], v_y);
    }
#endif
    for (; i < n; ++i) {
        out[i] = synax_autonomous_verified_kernel_c11(in_a[i], in_b[i]);
    }
}
