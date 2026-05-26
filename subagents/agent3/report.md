# Agent3 independent validation report

All `A.cpp` to `M.cpp` were compiled with:

```text
g++ -std=c++17 -O2 -pipe -static -s
```

Per-case timeout used for local execution: 5 seconds.

| Problem | Result | Failed groups | Failure type | Brief reason |
| --- | ---: | --- | --- | --- |
| A | 25/25 AC | - | - | DP over the two preserved subsequences passed all data. |
| B | 25/25 AC | - | - | Fixed output. |
| C | 17/25 AC | 11_stress, 12_stress, 13_stress, 14_stress, 15_stress, 16_stress, 17_stress, 18_stress | TLE | Implementation answers each query by scanning all vertices, so stress cases exceed timeout. |
| D | 25/25 AC | - | - | Prefix/suffix periodic counts plus NTT convolution passed all data. |
| E | 25/25 AC by legality checker | - | - | Exact `.ans` text differs on 23 cases, but output uses `floor(n^2/4)` elevators, covers every pair as consecutive stops, and stays within the stop-count limit. |
| F | 25/25 AC | - | - | Offline mode reads `n` and hidden bit string, outputs the number of `1`s. |
| G | 24/25 AC | 11_stress | TLE | Brute recomputation for each query is too slow on the largest stress case. |
| H | 25/25 AC | - | - | Maximum repeated substring count equals maximum character frequency in the queried substring. |
| I | 25/25 AC | - | - | Binary search on production time. |
| J | 25/25 AC | - | - | Per-stall optimized pack/single purchase calculation. |
| K | 25/25 AC by legality checker | - | - | Exact `.ans` text differs on 22 cases, but all outputs have exact RGB counts and every constrained interval contains at most two colors. |
| L | 25/25 AC | - | - | Compared with `1e-9` tolerance; all outputs passed. |
| M | 25/25 AC | - | - | Brute sleep-one-dog simulation passed all local data. |

Notes:

- `E` and `K` are construction problems, so exact text comparison is not meaningful. I used problem-specific legality checks after the initial exact comparison.
- `L` was judged with absolute/relative error tolerance `1e-9`.
- `C` and `G` are the remaining performance failures in this independent implementation.
