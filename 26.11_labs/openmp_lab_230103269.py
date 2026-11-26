import os
os.environ["NUMBA_THREADING_LAYER"] = "omp"

import time, hashlib, json
import math
import numpy as np
import numba as nb
from numba import njit, prange, set_num_threads, get_num_threads, get_thread_id

STUDENT_NAME = "Muslima Kosmagambetova"
STUDENT_ID = 230103269

assert isinstance(STUDENT_ID, int) and STUDENT_ID > 0, "Set a valid numeric STUDENT_ID!"
assert (os.cpu_count() or 1) >= 4, "Local multi-core CPU (>=4 logical cores) required; no Colab!"


@njit(parallel=True)
def _omp_probe():
    acc = 0
    for i in prange(64):
        acc += get_thread_id() + 1
    return acc


_ = _omp_probe()
assert nb.threading_layer() == "omp", f"Expected 'omp' layer, got {nb.threading_layer()}"

rng = np.random.default_rng(STUDENT_ID)

N_T1 = 4_000_000 + (STUDENT_ID % 991) * 1024
BINS_T1 = 48 + (STUDENT_ID % 17)
ITERS_T2 = 35_000_000 + (STUDENT_ID % 503) * 10_000
PAD_STRIDE = 8 + (STUDENT_ID % 5) * 8
ROWS_T3 = 12_000 + (STUDENT_ID % 257) * 16
SKEW_MOD = 37 + (STUDENT_ID % 19)
GRID_H = 384 + (STUDENT_ID % 4) * 32
GRID_W = 512 + (STUDENT_ID % 5) * 32
OMEGA_SOR = np.float64(1.72 + (STUDENT_ID % 11) * 0.015)

data_t1 = rng.integers(0, BINS_T1, size=N_T1, dtype=np.int32)
weights_t1 = rng.uniform(0.25, 2.50, size=N_T1).astype(np.float64)

print(f"Backend: {nb.threading_layer()} | Logical Cores: {os.cpu_count()} | Student: {STUDENT_ID}")

MAX_T = nb.config.NUMBA_NUM_THREADS
assert MAX_T >= 8, f"Need >= 8 OpenMP threads, got {MAX_T}"


@njit(parallel=True)
def buggy_hist_omp(indices, weights, num_bins):
    hist = np.zeros(num_bins, dtype=np.int64)
    w_sums = np.zeros(num_bins, dtype=np.float64)
    for i in prange(indices.shape[0]):
        b = indices[i]
        hist[b] += 1
        w_sums[b] += weights[i]
    return hist, w_sums


@njit(parallel=True)
def safe_hist_omp(indices, weights, num_bins):
    n = indices.shape[0]
    max_threads = MAX_T
    priv_hist = np.zeros((max_threads, num_bins), dtype=np.int64)
    priv_wsum = np.zeros((max_threads, num_bins), dtype=np.float64)
    worker_hits = np.zeros(max_threads, dtype=np.int64)

    for p in prange(max_threads):
        tid = get_thread_id()
        lo = p * n // max_threads
        hi = (p + 1) * n // max_threads
        for i in range(lo, hi):
            b = indices[i]
            priv_hist[p, b] += 1
            priv_wsum[p, b] += weights[i]
        worker_hits[tid] += 1

    hist = np.zeros(num_bins, dtype=np.int64)
    w_sums = np.zeros(num_bins, dtype=np.float64)
    for b in range(num_bins):
        h = 0
        s = 0.0
        for t in range(max_threads):
            h += priv_hist[t, b]
            s += priv_wsum[t, b]
        hist[b] = h
        w_sums[b] = s
    return hist, w_sums, worker_hits


def run_task1():
    print("\n===== TASK 1 =====")

    set_num_threads(1)
    ref_hist, ref_wsum = buggy_hist_omp(data_t1, weights_t1, BINS_T1)
    print(f"reference 1 thread: sum(hist)={int(np.sum(ref_hist))}, N_T1={N_T1}")

    set_num_threads(8)
    print("\nbuggy_hist_omp, 8 threads, 10 runs:")
    lost_list = []
    disc_list = []
    for r in range(1, 11):
        h, w = buggy_hist_omp(data_t1, weights_t1, BINS_T1)
        lost = N_T1 - int(np.sum(h))
        disc = int(np.max(np.abs(h - ref_hist)))
        lost_list.append(lost)
        disc_list.append(disc)
        print(f"  run {r}: sum={int(np.sum(h))} lost={lost} max_diff={disc}")
    print(f"total lost = {sum(lost_list)}")
    print(f"worst run lost = {max(lost_list)} ({100 * max(lost_list) / N_T1:.4f}%)")
    print(f"max bin discrepancy = {max(disc_list)}")
    assert max(lost_list) > 0, "race not observed, run again"

    set_num_threads(8)
    safe_hist_omp(data_t1[:1000], weights_t1[:1000], BINS_T1)

    print("\nsafe_hist_omp:")
    first_h = None
    first_w = None
    hist_t1 = None
    wsums_t1 = None
    for t in (1, 2, 4, 8):
        set_num_threads(t)
        t0 = time.perf_counter()
        h, w, hits = safe_hist_omp(data_t1, weights_t1, BINS_T1)
        dt = time.perf_counter() - t0
        workers = int(np.count_nonzero(hits))
        if first_h is None:
            first_h = h.copy()
            first_w = w.copy()
        same = np.array_equal(h, first_h) and np.array_equal(w, first_w)
        print(f"  {t} threads: sum={int(np.sum(h))} workers={workers} time={dt:.4f}s identical={same}")
        assert int(np.sum(h)) == N_T1
        assert np.array_equal(h, ref_hist)
        assert same
        if t > 1:
            assert workers == t
        hist_t1, wsums_t1 = h, w

    print("OK: bit-identical on 1, 2, 4, 8 threads")
    return hist_t1, wsums_t1


DIAGNOSIS_T1 = (
    "The integer histogram loses counts because hist[b] += 1 is a non-atomic load-modify-store: two "
    "OpenMP threads can read the same stale value, both add one and both store the same result, so one "
    "increment disappears. Making that increment atomic would fix the integer total but would not make "
    "w_sums deterministic, because IEEE-754 double addition is not associative - rounding to 53 mantissa "
    "bits happens after every add, so (a+b)+c and a+(b+c) differ in the last ulp when the operands have "
    "different magnitudes. Even with an atomic float accumulator the thread interleaving would still "
    "decide the summation order, and the order decides the rounding, so every run would give a slightly "
    "different total. The thread-private buffer plus an ordered row-wise merge removes both problems: "
    "inside the parallel region no two workers touch the same memory, and after the barrier the reduction "
    "visits rows 0 to max_threads-1 in a fixed sequence, which pins one rounding order. One extra detail "
    "is needed to make the result bit-identical across 1, 2, 4 and 8 threads: if each private row were "
    "indexed by get_thread_id(), the set of elements landing in a given row would change with the thread "
    "count, so the partial sums and therefore the final rounding would change too. I index the rows by a "
    "fixed partition of the index space instead, so row p always accumulates exactly the same contiguous "
    "slice in exactly the same ascending order whatever the thread count is, and get_thread_id() is used "
    "only to record worker participation."
)


@njit(parallel=True)
def unpadded_state_omp(iters, seed_val):
    n_threads = get_num_threads()
    state = np.zeros(n_threads, dtype=np.int64)
    for t in prange(n_threads):
        x = np.int64(seed_val + get_thread_id() * 1315423911)
        for step in range(iters):
            tid = get_thread_id()
            x = (x * np.int64(6364136223846793005) + np.int64(1442695040888963407)) & np.int64(0x7FFFFFFFFFFFFFFF)
            state[tid] ^= (x >> 17)
    return state


@njit(parallel=True)
def padded_state_omp(iters, seed_val, pad_stride):
    n_threads = get_num_threads()
    state = np.zeros((n_threads, pad_stride), dtype=np.int64)
    for t in prange(n_threads):
        x = np.int64(seed_val + get_thread_id() * 1315423911)
        for step in range(iters):
            tid = get_thread_id()
            x = (x * np.int64(6364136223846793005) + np.int64(1442695040888963407)) & np.int64(0x7FFFFFFFFFFFFFFF)
            state[tid, 0] ^= (x >> 17)
    return state


def run_task2():
    print("\n===== TASK 2 =====")
    print(f"PAD_STRIDE = {PAD_STRIDE} slots = {PAD_STRIDE * 8} bytes")

    set_num_threads(8)
    unpadded_state_omp(1000, STUDENT_ID)
    padded_state_omp(1000, STUDENT_ID, PAD_STRIDE)

    times_un = {}
    times_pd = {}
    state_t2 = None
    print()
    for t in (1, 2, 4, 8):
        set_num_threads(t)

        t0 = time.perf_counter()
        s_un = unpadded_state_omp(ITERS_T2, STUDENT_ID)
        dt_un = time.perf_counter() - t0

        t0 = time.perf_counter()
        s_pd = padded_state_omp(ITERS_T2, STUDENT_ID, PAD_STRIDE)
        dt_pd = time.perf_counter() - t0

        equal = np.array_equal(s_un, s_pd[:, 0])
        assert equal, f"padded result differs at {t} threads"
        times_un[t] = dt_un
        times_pd[t] = dt_pd
        state_t2 = s_un
        print(f"  {t} threads: unpadded={dt_un:.4f}s padded={dt_pd:.4f}s speedup={dt_un / dt_pd:.2f}x equal={equal}")

    speedup_8 = times_un[8] / times_pd[8]
    print(f"\nspeedup at 8 threads = {speedup_8:.2f}x")
    print(f"time growth 1->8 unpadded = {times_un[8] / times_un[1]:.2f}x")
    print(f"time growth 1->8 padded   = {times_pd[8] / times_pd[1]:.2f}x")
    return state_t2, speedup_8


DIAGNOSIS_T2 = (
    "Both kernels run exactly the same number of LCG steps per worker, so every difference in wall-clock "
    "time comes from the memory system and not from arithmetic. In the unpadded version state[0..7] are "
    "eight adjacent int64 values living in one 64-byte cache line, and each thread does a "
    "read-modify-write of its own element on every iteration. Under MESI a store needs the line in "
    "Modified state, which is exclusive, so each write invalidates the copies held by the other seven "
    "cores and forces them to re-acquire the line from the current owner before their next store. The "
    "line ping-pongs between the private L1 caches at roughly coherence latency per iteration even "
    "though no thread ever reads data another thread wrote - this is false sharing, because the "
    "contention is on the granularity of the coherence unit and not on the data itself. Padding the "
    "buffer to (n_threads, PAD_STRIDE) puts each worker's active slot on its own cache line, so every "
    "line stays Modified in exactly one L1, the invalidation traffic disappears and the kernel scales "
    "with the cores instead of stalling on the interconnect."
)


@njit
def row_score(r, units):
    x = 0.37 + (r % 101) * 0.001
    acc = 0.0
    for k in range(units):
        x = x + 0.000173
        acc += math.sin(x) * math.cos(x) + math.sqrt(abs(x) + 1.0)
    return acc


@njit(parallel=True)
def static_skew_omp(work_units, ops_pad):
    n = work_units.shape[0]
    out = np.zeros(n, dtype=np.float64)
    for r in prange(n):
        tid = get_thread_id()
        u = work_units[r]
        out[r] = row_score(r, u)
        ops_pad[tid, 0] += u
    return out


@njit(parallel=True)
def balanced_skew_omp(work_units, ops_pad, chunk):
    n = work_units.shape[0]
    n_threads = get_num_threads()
    out = np.zeros(n, dtype=np.float64)
    n_chunks = (n + chunk - 1) // chunk
    for t in prange(n_threads):
        tid = get_thread_id()
        ops = 0
        for k in range(t, n_chunks, n_threads):
            lo = k * chunk
            hi = min(lo + chunk, n)
            for r in range(lo, hi):
                u = work_units[r]
                out[r] = row_score(r, u)
                ops += u
        ops_pad[tid, 0] += ops
    return out


def imbalance(ops_pad):
    ops = ops_pad[:, 0]
    active = ops[ops > 0]
    if active.size < 2:
        return 1.0
    return float(active.max()) / float(active.min())


def run_task3():
    print("\n===== TASK 3 =====")

    rows = np.arange(ROWS_T3, dtype=np.int64)
    work_units = 40 + ((rows * 7919 + STUDENT_ID) % SKEW_MOD) ** 2
    total_units = int(work_units.sum())
    print(f"work_units: min={int(work_units.min())} max={int(work_units.max())} "
          f"mean={work_units.mean():.1f} total={total_units}")

    set_num_threads(8)
    warm = np.zeros((MAX_T, PAD_STRIDE), dtype=np.int64)
    static_skew_omp(work_units[:64], warm)
    balanced_skew_omp(work_units[:64], warm, 16)

    out_static = None
    out_balanced = None
    imb_s = {}
    imb_b = {}
    print()
    for t in (1, 2, 4, 8):
        set_num_threads(t)

        ops_s = np.zeros((MAX_T, PAD_STRIDE), dtype=np.int64)
        t0 = time.perf_counter()
        out_static = static_skew_omp(work_units, ops_s)
        dt_s = time.perf_counter() - t0
        imb_s[t] = imbalance(ops_s)

        ops_b = np.zeros((MAX_T, PAD_STRIDE), dtype=np.int64)
        t0 = time.perf_counter()
        out_balanced = balanced_skew_omp(work_units, ops_b, 16)
        dt_b = time.perf_counter() - t0
        imb_b[t] = imbalance(ops_b)

        assert int(ops_s[:, 0].sum()) == total_units
        assert int(ops_b[:, 0].sum()) == total_units
        print(f"  {t} threads: static={dt_s:.4f}s imbal={imb_s[t]:.3f} | "
              f"balanced={dt_b:.4f}s imbal={imb_b[t]:.3f}")

    max_abs = float(np.max(np.abs(out_static - out_balanced)))
    print(f"\nmax|out_static - out_balanced| = {max_abs:.3e} (gate < 1e-11)")
    print(f"imbalance at 8 threads: static={imb_s[8]:.4f} balanced={imb_b[8]:.4f} (gate < 1.15)")
    assert max_abs < 1e-11, f"gate failed: {max_abs}"
    assert imb_b[8] < 1.15, f"gate failed: {imb_b[8]:.4f}"
    print("OK: both gates passed")
    return out_static, imb_s[8], imb_b[8]


DIAGNOSIS_T3 = (
    "Numba's prange lowers to an OpenMP static schedule: the index space is cut into n_threads "
    "contiguous blocks assigned once before any iteration runs, so the partitioning cannot react to the "
    "real per-row cost and the barrier at the end of the region runs at the speed of the slowest block. "
    "My balanced kernel replaces that with an explicit worker loop over threads and cuts the row space "
    "into chunks of 16 rows that are claimed stride-interleaved, so thread t takes chunks t, t+T, t+2T "
    "and so on until the chunk space is exhausted. Because each worker keeps taking small batches spread "
    "across the whole index range instead of one large contiguous block, every thread samples the same "
    "cost distribution and the heavy rows are spread evenly, which is what drives the imbalance ratio "
    "below the 1.15x gate, while a chunk of 16 rows keeps the per-claim bookkeeping negligible against "
    "the cost of a row. One honest note about this workload: 7919 is coprime to SKEW_MOD, so the skew "
    "factor cycles through all residues with period SKEW_MOD and any contiguous block longer than "
    "SKEW_MOD rows already holds a near-uniform mix of cheap and expensive rows, which means the static "
    "schedule happens to start out close to balanced here. The dynamic distribution is what makes the "
    "bound hold by construction instead of by luck, since it does not depend on the skew pattern being "
    "coprime with the block size and would still remove stragglers under a clustered or monotonically "
    "increasing cost profile, where static partitioning would collapse."
)


def make_grid():
    U = np.zeros((GRID_H, GRID_W), dtype=np.float64)
    U[0, :] = 100.0
    U[-1, :] = -50.0
    U[:, 0] = 25.0 * np.sin(np.linspace(0, np.pi, GRID_H))
    U[:, -1] = 75.0 * np.cos(np.linspace(0, np.pi / 2, GRID_H))
    return U


@njit(parallel=True)
def sor_red_black_step(U, omega, color, tmax_pad):
    H, W = U.shape
    for r in prange(1, H - 1):
        tid = get_thread_id()
        local = 0.0
        start = 1 + (((r + 1) & 1) ^ color)
        for c in range(start, W - 1, 2):
            old = U[r, c]
            new = (1.0 - omega) * old + 0.25 * omega * (
                U[r - 1, c] + U[r + 1, c] + U[r, c - 1] + U[r, c + 1]
            )
            U[r, c] = new
            d = abs(new - old)
            if d > local:
                local = d
        if local > tmax_pad[tid, 0]:
            tmax_pad[tid, 0] = local


@njit
def reset_tmax(tmax_pad):
    for i in range(tmax_pad.shape[0]):
        tmax_pad[i, 0] = 0.0


def solve_pde_omp(sweeps, n_threads):
    set_num_threads(n_threads)
    U = make_grid()
    tmax_pad = np.zeros((MAX_T, PAD_STRIDE), dtype=np.float64)
    max_delta = 0.0
    for it in range(sweeps):
        reset_tmax(tmax_pad)
        sor_red_black_step(U, OMEGA_SOR, 0, tmax_pad)
        sor_red_black_step(U, OMEGA_SOR, 1, tmax_pad)
        max_delta = float(tmax_pad[:, 0].max())
    return U, max_delta


def run_task4():
    print("\n===== TASK 4 =====")
    sweeps = 600
    print(f"grid={GRID_H}x{GRID_W} omega={OMEGA_SOR:.4f} sweeps={sweeps}")

    solve_pde_omp(2, 8)

    print()
    t0 = time.perf_counter()
    ref_U, ref_delta = solve_pde_omp(sweeps, 1)
    t_ref = time.perf_counter() - t0
    print(f"  1 threads: time={t_ref:.4f}s speedup=1.00x max_delta={ref_delta:.3e} diff=0.0e+00")

    grid_t4 = ref_U
    speedups = {1: 1.0}
    for t in (2, 4, 8):
        t0 = time.perf_counter()
        U, delta = solve_pde_omp(sweeps, t)
        dt = time.perf_counter() - t0
        diff = float(np.max(np.abs(U - ref_U)))
        speedups[t] = t_ref / dt
        print(f"  {t} threads: time={dt:.4f}s speedup={t_ref / dt:.2f}x max_delta={delta:.3e} diff={diff:.3e}")
        assert diff < 1e-9, f"gate failed at {t} threads: {diff}"
        grid_t4 = U

    print(f"\nresidual after {sweeps} sweeps: max_delta={ref_delta:.6e}")
    print(f"OK: max_abs_diff < 1e-9, speedup at 8 threads = {speedups[8]:.2f}x")
    return grid_t4, speedups


hist_t1, wsums_t1 = run_task1()
state_t2, speedup_t2 = run_task2()
out_t3, imb_static_t3, imb_balanced_t3 = run_task3()
grid_t4, speedups_t4 = run_task4()

set_num_threads(8 if (os.cpu_count() or 1) >= 8 else os.cpu_count())

for idx, diag in enumerate([DIAGNOSIS_T1, DIAGNOSIS_T2, DIAGNOSIS_T3], start=1):
    assert isinstance(diag, str) and len(diag.strip()) >= 80, f"Complete DIAGNOSIS_T{idx}!"

checksum_blob = (
    f"{STUDENT_ID}|"
    f"{int(np.sum(hist_t1))}|{float(np.sum(wsums_t1)):.4f}|"
    f"{int(np.bitwise_xor.reduce(state_t2))}|"
    f"{float(np.sum(out_t3)):.6f}|"
    f"{float(np.sum(grid_t4)):.6f}"
)
lab_digest = hashlib.sha256(checksum_blob.encode()).hexdigest()[:20].upper()

bundle = {
    "instructor": "Instructor - Sufyan bin Uzayr",
    "student_name": STUDENT_NAME,
    "student_id": STUDENT_ID,
    "omp_layer": nb.threading_layer(),
    "cpu_cores": os.cpu_count(),
    "verification_digest": lab_digest,
}
print("\n=== OPENMP PYTHON LAB VERIFICATION BUNDLE ===")
print(json.dumps(bundle, indent=2))
