import os
os.environ["NUMBA_THREADING_LAYER"] = "omp"

import numba as nb
from numba import njit, prange, get_thread_id


@njit(parallel=True)
def probe():
    acc = 0
    for i in prange(64):
        acc += get_thread_id() + 1
    return acc


probe()
layer = nb.threading_layer()
print("numba:", nb.__version__)
print("layer:", layer)
print("cores:", os.cpu_count())
print("threads:", nb.config.NUMBA_NUM_THREADS)

if layer == "omp":
    print("OK")
else:
    print("PROBLEM: got", layer, "instead of omp")
