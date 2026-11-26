# Task 04: Asymptotic Parallel Efficiency

Parallel efficiency is speedup divided by the processor count:

[The relationship is explained in words below.]

## Gustafson’s model

[The relationship is explained in words below.]

For constant the serial fraction, the term the serial fraction/P approaches zero as P approaches infinity. Therefore:

[The relationship is explained in words below.]

For example, if the serial fraction = 0.04, efficiency approaches 0.96, or 96%.

## Amdahl’s model

[The relationship is explained in words below.]

For a constant positive serial fraction s, the denominator grows without limit. Therefore:

[The relationship is explained in words below.]

If the serial fraction = 0, efficiency remains equal to one.

This difference follows from the workload assumptions. A fixed workload eventually provides too little useful work for additional processors. A growing workload can continue providing useful work, provided that overhead does not increase enough to break the model.
