# Task 12: Including Communication Overhead

Real parallel systems spend time exchanging data and synchronizing processors. I include this cost as an additional term C(P).

Let a be the serial time and b be the parallel time before adding this extra communication cost. I normalize the baseline time so that a + b = 1.

The equivalent serial workload takes:

[The relationship is explained in words below.]

If C(P) represents additional parallel-only overhead, the actual parallel time is:

[The relationship is explained in words below.]

The modified speedup is therefore:

[The relationship is explained in words below.]

Possible example models are:

[The relationship is explained in words below.]

or

[The relationship is explained in words below.]

where c controls the size of the overhead. Both expressions give C(1) = 0.

As communication costs increase, the denominator increases and speedup decreases. In this formulation, a is the serial fraction of the baseline execution before the added cost. If communication has already been included in a measured serial fraction, it must not be counted again as C(P).
