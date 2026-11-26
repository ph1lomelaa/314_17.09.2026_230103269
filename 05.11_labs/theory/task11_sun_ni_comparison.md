# Task 11: Gustafson and Memory-Bounded Speedup

Gustafson’s model increases the workload while keeping execution time approximately constant. The Sun–Ni memory-bounded approach considers how much the workload can grow when more total memory becomes available.

These conditions are different. A problem may fit in the available memory while still taking longer to execute.

## A simplified generalized formulation

Let the serial fraction and 1 − the serial fraction represent the normalized serial and parallelizable work of a baseline problem on one processor. Let G(P) represent the growth of parallel computational work allowed by the available memory. Assuming unchanged serial work and ideal parallel execution:

[The relationship is explained in words below.]

If G(P) = 1, the workload remains fixed and the formula reduces to Amdahl’s Law. If G(P) = P, parallel execution time stays constant and the formula has Gustafson’s form. Other growth functions describe different relationships between memory capacity and work.

Memory growth and computational growth are not always equal. For example, dense matrix storage grows as N², while multiplication work grows as N³. Increasing available memory by a factor of P can allow computational work to grow by the processor count raised to the power of one and a half, if the memory is used for larger matrices.

Gustafson’s ideal prediction can overestimate achieved speedup when communication, synchronization, or memory contention increases. A memory-bounded workload may allow more computational growth than the fixed-time model, producing a larger scaled speedup relative to serial execution of that enlarged workload. However, execution time may also increase.

I would distinguish scaled speedup from throughput: doing more total work does not automatically mean a higher rate of useful operations per second.
