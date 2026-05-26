# Agent 4 Independent Validation Report

Scope: source files are `subagents/agent4/A.cpp` through `subagents/agent4/M.cpp`.

Judging method:
- Initial compile of all files with `g++ -std=c++17 -O2 -pipe` succeeded.
- After later edits, `G.cpp` and `L.cpp` were individually recompiled and retested successfully.
- A final full recompile was interrupted/blocked by stale `C.exe` test processes locking the executable on Windows; those processes were stopped afterward.
- Compared normal tasks against `data/{A..M}/*.ans` for the groups that were run.
- `L` used absolute/relative tolerance `1e-9`.
- `K` was additionally checked by a local legality validator because outputs are non-unique.
- `E` was treated as WA when the first line was not the minimum `m`.
- Per user instruction after interruption, no further huge stress points were run.

| Problem | Passed | Failed groups | Type | Brief reason |
| --- | ---: | --- | --- | --- |
| A | 25/25 | - | - | DP over keep/throw stable partition states. |
| B | 25/25 | - | - | Fixed output. |
| C | 17/25 | 11_stress, 12_stress, 13_stress, 14_stress, 15_stress, 16_stress, 17_stress, 18_stress | TLE | Exact per-query scan is correct on small/edge data but too slow for `n=500000`. |
| D | 25/25 | - | - | Z-function period counting plus NTT convolution. |
| E | 1/25 | 01_regular-18_stress, 20_edge-25_edge | WA | Construction covers pairs but uses `n(n-1)/2` elevators, not the required minimum `floor(n^2/4)`. |
| F | 25/25 | - | - | Offline mode counts `1` in hidden string. |
| G | 25/25 | - | - | Kruskal reconstruction tree plus treap prefix LCA. |
| H | 25/25 | - | - | Answer is max character frequency in interval. |
| I | 25/25 | - | - | Binary search on time. |
| J | 25/25 | - | - | Checks best pack count near greedy maximum. |
| K | 25/25 | - | - | Exact text matched 3/25; legality validator accepted all 25 outputs, including the impossible case. |
| L | 25/25 | - | - | Circular angle sliding window of `k` consecutive points. |
| M | 25/25 | - | - | Zero-risk components plus single-dog visibility component check. |

Notes:
- `G.cpp` was updated after a stress-case stack overflow in recursive DSU `find`; the final version uses iterative path compression.
- `L.cpp` was updated from a quadratic verifier to an `O(n log n)`/sliding-window solution.
- Some earlier bulk Python runners timed out while `C.exe` was still executing huge stress data; this is the source of the final Windows executable lock and is recorded above as `C` TLE on stress groups.
