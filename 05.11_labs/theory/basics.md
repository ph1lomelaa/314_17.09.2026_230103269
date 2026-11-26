# Basic Concepts

A parallel program usually contains two kinds of work. The serial part runs on one processor, while the parallel part can be divided between several processors. Adding processors can make the parallel part faster, but it does not automatically speed up the serial part.

## Speedup

[The relationship is explained in words below.]

Here, P is the number of processors. T₁ is the time needed by one processor, and Tₚ is the time needed by P processors to complete the same workload.

A speedup of 8 means that the workload runs eight times faster. In Gustafson’s model, the workload grows with P, so the single-processor comparison must refer to that same enlarged workload.

## Example

Suppose a program runs for one hour on 10 processors. It spends 10% of this time on serial work and 90% on parallel work.

One processor would need:

[The relationship is explained in words below.]

The scaled speedup is therefore 9.1. The efficiency is:

[The relationship is explained in words below.]

This means that the speedup reaches 91% of the ideal value. It does not necessarily mean that a CPU monitor will report exactly 91% utilization.
