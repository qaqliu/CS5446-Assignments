# Tutorial 2 : Rational Decision Making

> National University of Singapore · School of Computing  
> CS4246/CS5446 Reinforcement Learning and Sequential Decision Making  
> Semester 1, AY2026-27 · Issued: 26 Aug 2026

**Group Members**

- Zhang Jiazheng (A0314707H)
- Phyo Han (A0196680R)
- Wang Shiyu (A0354696L)
- Liu Hengyan (A0350634J)

## AI Assistance Declaration

> ChatGPT was used to help transcribe the tutorial questions into Markdown and prepare answer placeholders. I remain responsible for the accuracy, originality, and final content of this submission.

## Guidelines

You may discuss the content of the questions with your classmates. But everyone should work on and be ready to present **ALL** the solutions.

## Problem 1 – Utility Matchmaker: The Case of the Mysterious Preferences

### Part A

Consider the following lotteries, where $[p, x]$ denotes outcome $x$ with probability $p$:

$$
L_1 = [1, 1], \qquad L_2 = [0.5, 2;\ 0.5, 0], \qquad L_3 = [1, 2].
$$

Four students have expressed their preferences over these lotteries:

- Adam is indifferent between $L_2$ and $L_1$.
- Bing prefers $L_1$ to $L_2$.
- Candy is indifferent between $L_3$ and $L_2$.
- Diana prefers $L_2$ to $L_1$.

Match each student with a utility function that is consistent with their stated preferences (each student has a different one):

- (a) $U(x) = x^2$
- (b) $U(x) = x$
- (c) $U(x) = \sqrt{x}$
- (d) None of the above

### Answer

For each utility function, compare the expected utility of $L_1$ and $L_2$:

$$
\begin{aligned}
U(x) = x^2:& \qquad EU(L_1) = 1, \quad EU(L_2) = 0.5(2^2) + 0.5(0^2) = 2; \\
U(x) = x:& \qquad EU(L_1) = 1, \quad EU(L_2) = 0.5(2) + 0.5(0) = 1; \\
U(x) = \sqrt{x}:& \qquad EU(L_1) = 1, \quad EU(L_2) = 0.5\sqrt{2} < 1.
\end{aligned}
$$

Thus, Diana prefers $L_2$ to $L_1$ and is matched with **(a)** $U(x) = x^2$; Adam is indifferent between $L_2$ and $L_1$ and is matched with **(b)** $U(x) = x$; and Bing prefers $L_1$ to $L_2$ and is matched with **(c)** $U(x) = \sqrt{x}$.

For all three listed utility functions, $L_3$ has a strictly higher expected utility than $L_2$:

$$
U(2) > 0.5U(2) + 0.5U(0).
$$

Therefore, none of (a)--(c) makes Candy indifferent between $L_3$ and $L_2$, so Candy is matched with **(d) None of the above**.

| Student | Matching utility function |
| --- | --- |
| Adam | (b) $U(x) = x$ |
| Bing | (c) $U(x) = \sqrt{x}$ |
| Candy | (d) None of the above |
| Diana | (a) $U(x) = x^2$ |

### Part B

Assume Agent 1 has utility $U_1$ and Agent 2 has utility $U_2$. If

$$
U_1 = k_1 U_2 + k_2, \qquad k_1 > 0,\ k_2 \in \mathbb{R},
$$

do Agents 1 and 2 have the same preferences?

### Answer

Yes. Let $L_1$ and $L_2$ be any two lotteries, and write $EU_i(L)$ for Agent $i$'s expected utility of lottery $L$. Since $U_1(x) = k_1U_2(x) + k_2$, where $k_1 > 0$, taking expectations gives

$$
EU_1(L) = k_1EU_2(L) + k_2.
$$

First, suppose that Agent 1 strictly prefers $L_1$ to $L_2$, i.e., $L_1 \succ_1 L_2$. Then

$$
\begin{aligned}
EU_1(L_1) &> EU_1(L_2) \\
k_1EU_2(L_1) + k_2 &> k_1EU_2(L_2) + k_2 \\
EU_2(L_1) &> EU_2(L_2),
\end{aligned}
$$

where the final implication holds because $k_1 > 0$. Hence $L_1 \succ_2 L_2$.

Next, suppose that Agent 1 is indifferent between $L_1$ and $L_2$, i.e., $L_1 \sim_1 L_2$. Then

$$
\begin{aligned}
EU_1(L_1) &= EU_1(L_2) \\
k_1EU_2(L_1) + k_2 &= k_1EU_2(L_2) + k_2 \\
EU_2(L_1) &= EU_2(L_2).
\end{aligned}
$$

Therefore, $L_1 \sim_2 L_2$.

Conversely, the relation can be rearranged as

$$
U_2 = \frac{1}{k_1}U_1 - \frac{k_2}{k_1},
$$

and $1/k_1 > 0$. Repeating the same two arguments with Agents 1 and 2 exchanged shows that $L_1 \succ_2 L_2 \Rightarrow L_1 \succ_1 L_2$ and $L_1 \sim_2 L_2 \Rightarrow L_1 \sim_1 L_2$. Thus, the two agents have exactly the same preferences.

---

## Problem 2: Adventures of PacBaby

PacBaby just found a $100 note — it is the only thing she owns. Monsters are kind enough not to kill PacBaby, but whenever they find her, they steal all her money. The probability that the monsters find PacBaby is 20% (i.e., 0.2).

PacBaby's utility function is

$$
U(x) = \log(1 + x),
$$

where $\log$ denotes the natural logarithm and $x$ is her monetary wealth. Thus,

$$
U(100) = \log(101) \qquad \text{and} \qquad U(0) = \log(1 + 0) = 0.
$$

### (a)

What is PacBaby's expected utility without insurance?

### Answer

Without insurance, PacBaby keeps the $100 with probability $0.8$ and loses all her money with probability $0.2$. Therefore,

$$
\begin{aligned}
EU(\text{without insurance})
&= 0.8U(100) + 0.2U(0) \\
&= 0.8\log(101) + 0.2\log(1) \\
&= 0.8\log(101) \\
&\approx 3.6922.
\end{aligned}
$$

### (b)

PacIncome offers theft insurance: for a premium of $30, PacBaby will be reimbursed $70 if monsters steal her money. After paying the premium, if no theft occurs, PacBaby holds $70; if theft occurs, she also ends up with $70 (the reimbursement). What is PacBaby's expected utility if she buys insurance? Should she buy it to maximize expected utility?

### Answer

After paying the $30 premium, PacBaby has $70 if no theft occurs. If a theft occurs, the $70 reimbursement also leaves her with $70. Thus, her final wealth is $70 in either state:

$$
\begin{aligned}
EU(\text{with insurance})
&= 0.8U(70) + 0.2U(70) \\
&= U(70) \\
&= \log(71) \\
&\approx 4.2627.
\end{aligned}
$$

Since

$$
\log(71) \approx 4.2627 > 0.8\log(101) \approx 3.6922,
$$

PacBaby should buy the insurance to maximize her expected utility.

### (c)

From PacIncome's point of view, what is the expected *monetary* value of selling this insurance?

### Answer

PacIncome's monetary payoff has two possible outcomes:

$$
\text{Payoff} =
\begin{cases}
\$30, & \text{with probability } 0.8 \text{ (no theft)}, \\
\$30 - \$70 = -\$40, & \text{with probability } 0.2 \text{ (theft occurs)}.
\end{cases}
$$

Hence, its expected monetary value is

$$
\begin{aligned}
EMV(\text{insurance})
&= 0.8(30) + 0.2(-40) \\
&= 24 - 8 \\
&= \$16.
\end{aligned}
$$

---

## Problem 3: Allais Paradox

The Allais paradox (Allais, 1953) is a well-known problem potentially suggesting that humans are “predictably irrational” (Ariely, 2009).[^1] People are given a choice between lotteries A and B and then between C and D, which have the following prizes:

| Lottery | Prize | Lottery | Prize |
| --- | --- | --- | --- |
| A | 80% chance of $4000 | C | 20% chance of $4000 |
| B | 100% chance of $3000 | D | 25% chance of $3000 |

Most people consistently prefer B over A (i.e., taking the sure payoff), and C over D (taking the higher EMV).

### (a)

Show that the normative analysis (i.e., describing how a rational agent should act) disagrees.  
**Hint:** Set $U(\$0) = 0$; show that the preferences between A, B and C, D are opposites, hence a contradiction.

### Answer

Let $u_4 = U(\$4000)$ and $u_3 = U(\$3000)$, with $U(\$0) = 0$. Under normative expected-utility analysis,

$$
\begin{aligned}
EU(A) &= 0.8u_4, & EU(B) &= u_3, \\
EU(C) &= 0.2u_4, & EU(D) &= 0.25u_3.
\end{aligned}
$$

The common judgment $B \succ A$ requires

$$
EU(B) > EU(A)
\quad \Longleftrightarrow \quad
u_3 > 0.8u_4.
$$

In contrast, the common judgment $C \succ D$ requires

$$
\begin{aligned}
EU(C) &> EU(D) \\
0.2u_4 &> 0.25u_3 \\
0.8u_4 &> u_3.
\end{aligned}
$$

Thus, $B \succ A$ requires $u_3 > 0.8u_4$, whereas $C \succ D$ requires $0.8u_4 > u_3$. These are opposite inequalities and cannot both hold. Therefore, no expected-utility function can represent the judgments $B \succ A$ and $C \succ D$ simultaneously; normative expected-utility analysis disagrees with the observed common preferences.

### (b)

Prove that the judgments $B \succ A$ and $C \succ D$ in the above Allais paradox violate the axiom of substitutability. **Hint:** You may wish to consider using the axiom of decomposability.

### Answer

By decomposability, lottery $C$ can be written as a compound lottery that gives lottery $A$ with probability $0.25$ and gives $\$0$ with probability $0.75$:

$$
\begin{aligned}
C
&= [0.25, A;\ 0.75, \$0] \\
&= [0.25(0.8), \$4000;\ 0.25(0.2) + 0.75, \$0] \\
&= [0.2, \$4000;\ 0.8, \$0].
\end{aligned}
$$

Similarly, $D$ can be written as

$$
D = [0.25, B;\ 0.75, \$0],
$$

because $B$ gives $\$3000$ with certainty, so this compound lottery gives $\$3000$ with probability $0.25$ and $\$0$ with probability $0.75$.

Now assume the judgment $B \succ A$. The axiom of substitutability states that if one lottery is preferred to another, replacing the less-preferred lottery by the preferred lottery in the same probabilistic context preserves that preference. Replacing $A$ by $B$ in the common context $[0.25,\ \cdot\ ;\ 0.75,\ \$0]$ therefore implies

$$
[0.25, B;\ 0.75, \$0] \succ [0.25, A;\ 0.75, \$0],
$$

or equivalently,

$$
D \succ C.
$$

This contradicts the observed judgment $C \succ D$. Hence the pair of judgments $B \succ A$ and $C \succ D$ violates the axiom of substitutability.

[^1]: For a possible explanation of such a paradox, refer to page 620 of AIMA textbook.
