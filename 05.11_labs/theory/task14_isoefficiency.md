# Task 14: Isoefficiency and Gustafson Scaling

Isoefficiency describes how quickly the problem must grow to maintain a chosen parallel efficiency.

Let W be useful work measured in equivalent single-processor time. Let Tₒ be total overhead:

[The relationship is explained in words below.]

Efficiency is:

[The relationship is explained in words below.]

For a chosen efficiency E₀ between zero and one:

[The relationship is explained in words below.]

Therefore, useful work must grow in proportion to overhead to maintain that efficiency.

## Ideal Gustafson case

With normalized parallel time Tₚ = 1 and constant serial fraction the serial fraction:

[The relationship is explained in words below.]

and

[The relationship is explained in words below.]

For 0 < the serial fraction < 1, both useful work and overhead grow linearly:

[The relationship is explained in words below.]

Thus, linear workload growth supports asymptotically constant efficiency in this ideal model. The exact efficiency is 1 − the serial fraction + the serial fraction/P, so it approaches 1 − the serial fraction rather than being exactly constant at every processor count.

This result depends on the overhead assumptions. If real communication costs grow faster, a faster workload growth rate may be needed. Gustafson’s formula alone does not provide a universal isoefficiency function for every algorithm.
