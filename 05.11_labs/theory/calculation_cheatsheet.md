# Calculation Reference

## Notation

| Symbol | Meaning |
|---|---|
| P | Number of processors or cores |
| the serial fraction | Serial fraction measured during parallel execution |
| the serial fraction in Amdahl’s formula | Serial fraction measured during single-processor execution |
| S | Speedup |
| E | Parallel efficiency |

The assignment also uses the serial fraction for the serial fraction in Gustafson’s derivation. Its meaning depends on the execution being measured.

## Main equations

Gustafson’s speedup:

[The relationship is explained in words below.]

Parallel efficiency:

[The relationship is explained in words below.]

Efficiency as a percentage:

[The relationship is explained in words below.]

Amdahl’s speedup:

[The relationship is explained in words below.]

For a required speedup S_req and P > 1, the maximum allowed serial fraction follows from:

[The relationship is explained in words below.]

so

[The relationship is explained in words below.]

The physical fraction must lie between zero and one. A required speedup above P is impossible in this ideal model.

## Calculation method for Task 06

I use the serial fraction = 0.04. For each requested processor count, I calculate speedup first, divide it by P to find efficiency, and multiply by 100 to express efficiency as a percentage.

## Checks

- 4% = 0.04, 8% = 0.08, and 0.4% = 0.004.
- At P = 1, speedup and efficiency equal one.
- At the serial fraction = 0, speedup equals P.
- At the serial fraction = 1, speedup equals one.
- For 0 ≤ the serial fraction ≤ 1, the ideal model gives 1 ≤ S ≤ P and 0 < E ≤ 1.
- Intermediate values should be retained before rounding the final result.
- A percentage difference needs an explicit reference. For example, 100(S_G − S_A)/S_A measures the increase relative to Amdahl’s prediction.
- A numerical 3D grid memory limit requires bytes per cell and the number of stored arrays. The statement O(N³) alone does not determine the exact grid size.
