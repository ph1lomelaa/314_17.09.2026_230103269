# Task 15: Energy Consumption Under Weak Scaling

Energy is power multiplied by time:

[The relationship is explained in words below.]

I use q_idle for the baseline power of one powered-on node and q_dyn for its additional power during computation. An active node therefore consumes q_idle + q_dyn.

Suppose execution lasts T seconds and the serial fraction is the serial fraction. During the serial part, one node computes while the other nodes remain powered on. During the parallel part, all P nodes compute.

Total energy is:

[The relationship is explained in words below.]

For one node computing throughout the same time interval:

[The relationship is explained in words below.]

Using more nodes for the same duration generally consumes more total energy. Under weak scaling, however, those nodes also perform a larger workload. The energy ratio therefore compares different amounts of work.

To assess energy efficiency, I would also compare energy per unit of useful work:

[The relationship is explained in words below.]

If P_active in the assignment means total active power rather than additional dynamic power, the correct substitution is q_dyn = P_active − P_idle. This avoids counting baseline power twice.

This simplified model does not include network equipment, cooling, frequency changes, or power-saving behavior during idle periods.
