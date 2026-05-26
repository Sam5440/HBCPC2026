## 题目 D. 简单字符串题

我们可以定义 $AB$ 表示两个字符串 $A, B$ 相连接，例如 $A = \text{aab}, B = \text{ab}$ ，则 $AB = \text{aabab}$ 。  
并递归地定义 $A^{1}=A,\quad A^{n}=A^{n-1}A\quad(n\geq2$ 且为正整数）。例如 A=abb，则 $A^{3}=abbabbabb$ 。

现给定一个长度为 $n$ 的字符串 $S$ ，给定常数 $k$ ，求 $S = A^i B_1 B_2 \ldots B_k C^j$ 的方案数，其中 $A, B_1, B_2, \ldots, B_k, C$ 为任意非空字符串， $i, j$ 为任意正整数。

两种方案不同当且仅当 $A$ 、 $B_{1}$ 、 $B_{2}$ 、 $\ldots$ 、 $B_{k}$ 、 $C$ 、 $i$ 、 $j$ 中有至少一个字符串或数字不同。  
答案要对 998244353 取模。

### 输入

第一行两个正整数 $n, k$ ( $2 \leq n \leq 5 \times 10^5, 0 \leq k \leq n - 2$ ), 第二行一个字符串 $S$ , 意义见题目描述。 $S$ 仅由英文小写字母构成。

### 输出

输出一行一个整数表示答案。

### 样例

| standard input | standard output |
| -------------- | --------------- |
| 5 1 aabcc      | 11              |
| 6 2 aaaaaa     | 19              |
| 8 1 aabaabcd   | 27              |

### 注释

对于第一组样例，有以下 11 种方案：

- $A = a, \quad B_{1} = a, \quad C = bcc, \quad i = 1, \quad j = 1$
- $A = a, \quad B_{1} = ab, \quad C = cc, \quad i = 1, \quad j = 1$
- $A = a, \quad B_{1} = abc, \quad C = c, \quad i = 1, \quad j = 1$
- $A = aa, \quad B_{1} = b, \quad C = cc, \quad i = 1, \quad j = 1$
- $A = aa, \quad B_{1} = bc, \quad C = c, \quad i = 1, \quad j = 1$
- $A = aab, \quad B_1 = c, \quad C = c, \quad i = 1, \quad j = 1$
- $A = a, \quad B_{1} = ab, \quad C = c, \quad i = 1, \quad j = 2$
- $A = a, \quad B_{1} = b, \quad C = c, \quad i = 2, \quad j = 2$
- $A = oa, \quad B_1 = b, \quad C = c, \quad i = 1, \quad j = 2$
- $A = a, \quad B_{1} = b, \quad C = cc, \quad i = 2, \quad j = 1$
- $A = a, \quad B_{1} = bc, \quad C = c, \quad i = 2, \quad j = 1$

> 注：第八个方案中“A=oa”疑似笔误，应为“A=a”。

---
