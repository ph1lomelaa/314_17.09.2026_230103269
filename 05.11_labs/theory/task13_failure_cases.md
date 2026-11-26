# Task 13: Cases Where Simple Weak Scaling Fails

## Direct all-pairs N-body simulation

In a direct N-body simulation, every particle interacts with the other particles. The computational work is proportional to N².

If the particle count grows proportionally to P, then the ideal computation time is:

[The relationship is explained in words below.]

Execution time increases even though the number of particles per processor stays constant. Ignoring communication, constant computation time would instead require the particle count grows as the square root of the processor count. Exchanging particle information can add further overhead.

## Comparison-based merge sort

Merge sort requires work of order N log N. If the input size grows as N = kP, an ideal balanced computation has a work-per-processor term:

[The relationship is explained in words below.]

This term grows with P. Parallel merging can also require data movement and synchronization, which add more time.

These examples show that constant input size per processor does not always mean constant computational work per processor. The simple assumption that input grows proportionally to P while execution time remains constant does not hold for these cases. A different workload growth rate and an explicit overhead model are needed.
