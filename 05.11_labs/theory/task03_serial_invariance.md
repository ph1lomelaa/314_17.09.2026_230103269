# Task 03: The Serial Fraction Invariance Paradox

The apparent contradiction comes from measuring the serial fraction in different executions. Amdahl’s fraction is measured on one processor, while Gustafson’s fraction is measured on the parallel machine.

For one particular workload, let a be its serial time and b be the time needed for its parallelizable work on one processor. Assuming ideal parallel execution:

[The relationship is explained in words below.]

These fractions are related by:

[The relationship is explained in words below.]

Solving for the serial fraction gives:

[The relationship is explained in words below.]

Substituting this value into Amdahl’s formula produces:

[The relationship is explained in words below.]

Therefore, the laws agree when they describe the same workload with consistent serial fractions.

In Gustafson’s model, keeping the serial fraction constant while increasing P means that the parallel workload grows. The serial fraction of the enlarged workload’s single-processor execution becomes smaller. Serial work still exists, but it becomes a smaller share of the total single-processor work.

The models do not remove serial overhead. They use different workload assumptions and measurement references.
