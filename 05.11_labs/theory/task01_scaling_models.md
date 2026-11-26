# Task 01: Strong Scaling and Weak Scaling

Amdahl’s Law and Gustafson’s Law consider different ways of using additional processors.

## Amdahl’s Law

Amdahl’s model keeps the problem size fixed. For example, if the task is to process 1,000 images, the number of images stays the same when more processors are added. The goal is to finish the same task sooner.


Here, the serial fraction is the serial fraction measured during a single-processor execution. This approach is called strong scaling or fixed-size scaling.

As P approaches infinity, the problem size stays constant. If the serial fraction > 0, the maximum speedup is 1/s. For example, a serial fraction of 0.1 limits speedup to 10.

## Gustafson’s Law

Gustafson’s model increases the workload when more processors become available. The goal is to complete more work in approximately the same time.

Here, the serial fraction is the serial fraction measured on the parallel machine. This is a fixed-time scaling model and is closely related to weak scaling.

As P increases, the parallel workload grows. In the ideal case, computational work grows approximately in proportion to P. The input dimension does not always grow at the same rate. For an algorithm with work proportional to N³, constant parallel computation time requires N ∝ the cube root of the processor count.

I understand the main difference as follows: Amdahl asks how much faster a fixed task can run, while Gustafson asks how much more work can be completed within a fixed time.

