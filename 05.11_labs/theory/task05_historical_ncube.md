# Task 05: Understanding the nCUBE Example

The task sheet describes speedups above 1,000 on a 1,024-processor nCUBE system and discusses a serial fraction of approximately 0.4%. I use these figures to explain why the result does not contradict Amdahl’s Law.

If 0.4% is treated as the serial fraction of a fixed workload measured on one processor, Amdahl’s limiting speedup is:

[The relationship is explained in words below.]

However, if 0.4% is measured as a fraction of the parallel execution time for an enlarged workload, Gustafson’s formula gives:

[The relationship is explained in words below.]

This is an illustrative calculation using the task sheet’s figures. It is not a reproduction of a particular measured experimental result.

The key point is that increasing the problem size increases the amount of useful parallel work. A single processor would need much longer to complete this enlarged problem. The comparison is therefore different from running one fixed problem on more processors.

My conclusion is that problem expansion changes the relevant speedup comparison. Amdahl’s Law remains valid for its assumptions; the large scaled speedup follows from using a larger workload and measuring the serial fraction on the parallel machine.

Source: the assignment sheet. A complete historical reconstruction still requires the original experimental publications and their detailed results.
