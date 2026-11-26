# Task 02: Derivation of Gustafson’s Law

I normalize the execution time on P processors to one unit:

[The relationship is explained in words below.]

Here, the serial fraction is the serial execution time and p is the parallel execution time on the parallel machine.

The serial part would still take the serial fraction time units on one processor. The parallel part takes p time units using P processors. Under ideal load distribution, one processor would need Pp time units to perform that same parallel work.

Therefore, the equivalent single-processor time is:

[The relationship is explained in words below.]

The parallel execution time is one, so the speedup becomes:

[The relationship is explained in words below.]

Using the serial fraction = the serial fraction and p = 1 − the serial fraction:

[The relationship is explained in words below.]

Expanding the expression gives:

[The relationship is explained in words below.]

This derivation assumes balanced parallel work and an equivalent serial workload of the serial fraction + Pp. Additional overhead must either be included consistently in the model or treated separately.

So basically as i unde