# Agent5 Independent Verification Report

## Scope

- Source path: `subagents/agent5/{A..M}.cpp`
- Compile command used: `g++ -std=c++17 -O2 -pipe -static -s`
- Compile result: all A-M compiled successfully.
- Judging basis: exact `.ans` comparison for all problems except L, where `1e-9` tolerance was used.
- Note: per user instruction, further large stress runs were stopped. C stress outputs left by the aborted/timeout run are treated as timeout/incomplete rather than meaningful WA.

## Summary

| Problem | Passed | Failed cases | Failure type | Short reason |
| --- | ---: | --- | --- | --- |
| A | 25/25 | none | none | DP implementation matched all data. |
| B | 25/25 | none | none | Fixed output matched all data. |
| C | 17/25 | 11_stress-18_stress | TLE/timeout incomplete | Implementation answers by enumerating all nodes per query; regular/edge data passed, full stress scale is too large. |
| D | 25/25 | none | none | Prefix-period counting plus convolution matched all data. |
| E | 1/25 | 01_regular-18_stress, 20_edge-25_edge | WA by exact compare | Constructive output is not the same as `.ans`; no separate legality checker was completed before stop request. Only 19_edge matched exactly. |
| F | 25/25 | none | none | Offline version reads `n` plus hidden 01 string and outputs number of ones. |
| G | 17/25 | 11_stress, 12_stress-18_stress | WA/TLE | Per-query Kruskal/top-k recomputation is too slow for stress; 11_stress completed but mismatched, 12-18 timed out. |
| H | 25/25 | none | none | Prefix character frequency answer matched all data. |
| I | 25/25 | none | none | Binary search matched all data. |
| J | 25/25 | none | none | Booth purchase enumeration matched all data. |
| K | 3/25 | 01_regular-06_regular, 08_regular-18_stress, 19_edge, 20_edge, 23_edge-25_edge | WA by exact compare | Greedy constructive output only exactly matched 07_regular, 21_edge, 22_edge; no separate legality checker was completed before stop request. |
| L | 25/25 | none | none | Floating answer matched within `1e-9`. |
| M | 25/25 | none | none | BFS with one dog disabled matched all data. |

## Detailed Results

### A
- AC: all 25 cases.

### B
- AC: all 25 cases.

### C
- AC: 01_regular-10_regular, 19_edge-25_edge.
- Failed: 11_stress-18_stress.
- Type: TLE/timeout incomplete.
- Reason: current implementation performs node enumeration per query, which is not viable for `n=q=500000`.

### D
- AC: all 25 cases.

### E
- AC: 19_edge.
- Failed by exact compare: 01_regular-18_stress, 20_edge-25_edge.
- Reason: multi-answer construction did not match the provided `.ans`; legality validation was not completed after the stop request.

### F
- AC: all 25 cases.

### G
- AC: 01_regular-10_regular, 19_edge-25_edge.
- Failed: 11_stress WA; 12_stress-18_stress TLE.
- Reason: current implementation recomputes top-k set and Kruskal-style connectivity for each query.

### H
- AC: all 25 cases.

### I
- AC: all 25 cases.

### J
- AC: all 25 cases.

### K
- AC: 07_regular, 21_edge, 22_edge.
- Failed by exact compare: 01_regular-06_regular, 08_regular-18_stress, 19_edge, 20_edge, 23_edge-25_edge.
- Reason: multi-answer greedy construction often differs from `.ans`; legality validation was not completed after the stop request.

### L
- AC: all 25 cases under `1e-9` absolute/relative tolerance.

### M
- AC: all 25 cases.

