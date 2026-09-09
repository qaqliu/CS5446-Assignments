# Tutorial 3 : Sequential Decision Making under Uncertainty

> National University of Singapore · School of Computing  
> CS4246/CS5446 Reinforcement Learning and Sequential Decision Making  
> Semester 1, AY2026-27 · Issued: 02 Sep 2026

**Group Members**

- Zhang Jiazheng (A0314707H)
- Phyo Han (A0196680R)
- Wang Shiyu (A0354696L)
- Liu Hengyan (A0350634J)

## AI Assistance Declaration

> ChatGPT was used to help transcribe the tutorial questions into Markdown and prepare answer placeholders. I remain responsible for the accuracy, originality, and final content of this submission.

## Guidelines

You may discuss the content of the questions with your classmates. But everyone should work on and be ready to present **ALL** the solutions.

## Note: Transition Reward Calculation Conventions

AIMA (4e) defines the immediate reward as a transition reward $R(s, a, s')$. The reward-on-entry convention is compatible with this definition by taking $R(s, a, s') = f(s')$, that is, reward depends only on the next state. A reward-of-current-state convention corresponds to $R(s, a, s') = f(s)$, where reward depends only on the current state. Both are special cases of AIMA's general $R(s, a, s')$.

In episodic reinforcement learning, terminal states are assigned value 0, and the reward for reaching them is accounted on the transition into the terminal state. This aligns with the Sutton & Barto convention, which is the most common in reinforcement learning.

Both conventions are mathematically valid, but mixing them leads to inconsistent results. It is best to adopt one convention consistently across all parts of a problem.

In this course, by default we use the reward-on-entry convention, unless specified otherwise.

## Problem 1: Nova the Mars Rover

Nova is an autonomous Mars rover that collects scientific data while managing its limited battery. Each sol, Nova must decide whether to operate in an energy-saving mode or use a high-power boost mode. Boost mode collects more data immediately but drains the battery more quickly.

Having learned about Markov Decision Processes (MDPs), Nova's controller models this decision as an infinite horizon MDP with two states—charged and low—and two actions—eco or boost. Therefore, the state set:

$$
S = \{\text{charged}, \text{low}\}
$$

and action set:

$$
A = \{\text{eco}, \text{boost}\}
$$

Nova estimates the state-transition probabilities $P(s' \mid s, a)$ as follows:

| State $s$ | Action $a$ | $P(s' = \text{charged})$ |
| --- | --- | --- |
| charged | eco | 0.95 |
| charged | boost | 0.7 |
| low | eco | 0.5 |
| low | boost | 0.1 |

This means that if Nova is charged and uses boost mode, there is a 30% chance its battery becomes low. If Nova is charged and uses eco mode, there is a 95% chance it remains charged. When its battery is low, using eco mode gives a 50% chance of returning to the charged state. However, if Nova uses boost mode while its battery is low, there is only a 10% chance it will become charged again.

Nova estimates the rewards, independent of the resulting state, as follows:

| State $s$ | Action $a$ | Reward |
| --- | --- | --- |
| charged | eco | 7 |
| charged | boost | 10 |
| low | eco | 0 |
| low | boost | 2 |

Thus, boost mode always gives Nova a higher immediate reward than eco mode. However, Nova performs much better when its battery is charged, and using boost mode makes a low battery more likely.

The challenge is to determine what Nova should do each sol. Nova's decision-making can be modeled as an MDP with two states and two actions, giving $2 \times 2 = 4$ possible policies:

- Always use eco mode.
- Always use boost mode.
- Use eco mode when charged and boost mode when low.
- Use boost mode when charged and eco mode when low.

Without discounting, each of these policies would yield an infinite total reward over an infinite horizon.

### Part 1: Discounting

**a)** Explain the role of discounting future rewards in MDPs. How would an agent behave differently if the discount factor was 0.6 instead of 0.9?

### Answer

> _To be completed._

**b)** As the discount factor varies from 0 to 1, how does the optimal policy change? Provide an example discount factor for each distinct policy obtainable by varying the discount factor.

### Answer

> _To be completed._

**c)** How could the MDP or the discount factor be altered so that the optimal policy is to use eco mode when charged and boost mode when low? Provide a modified MDP that requires minimal changes in probabilities, rewards, or discount factors to achieve this outcome.

### Answer

> _To be completed._

**d)** What does the discount factor $\gamma$ represent in practical terms? Why can $\gamma = 1$ cause problems?

### Answer

> _To be completed._

### Part 2: Optimal Policy

Consider Nova's two-state MDP with $\gamma = 0.8$. Represent the value function as $[V_{\text{charged}}, V_{\text{low}}]$.

Assume the initial value function is $V^{(0)} = [0, 0]$, and initialize the Q-values as:

$$
Q^{(0)}(c, \text{eco}) = 0, \qquad Q^{(0)}(c, \text{boost}) = 0, \qquad Q^{(0)}(l, \text{eco}) = 0, \qquad Q^{(0)}(l, \text{boost}) = 0.
$$

**a)** What are the updated Q-values starting from $V^{(0)}$?

### Answer

> _To be completed._

**b)** What is the next updated value function $V^{(1)}$?

### Answer

> _To be completed._

**c)** Starting from $V^{(1)} = [10, 2]$, compute the next update $V^{(2)}$:

- **Value Iteration (VI):** Apply the Bellman optimality update.
- **Policy Iteration (PI):** Derive the greedy policy $\pi^{(1)}$ wrt $V^{(1)}$, then evaluate it exactly by solving the linear system for $V^{\pi^{(1)}}$.

### Answer

> _To be completed._

**d)** What is the optimal policy?

### Answer

> _To be completed._

## Problem 2: Aster's Rescue Route—Comparing Active RL Methods

Aster is an autonomous rescue drone learning how to return to base through an uncertain environment. At state $s_0$, it can choose between two routes:

$$
a = \text{valley route}, \qquad b = \text{ridge shortcut}.
$$

The drone may reach an intermediate state $s_1$ or return directly to base $T$, which is terminal. At $s_1$, it can choose between actions $c$ and $d$.

Assume the environment model is initially unknown. The discount factor is $\gamma = 0.8$.

Before the current episode, Aster has observed the following outcomes from $s_0$:

| Action | Next state | Reward | Number observed |
| --- | --- | --- | --- |
| $a$ | $s_1$ | 0 | 4 |
| $b$ | $T$ | 6 | 3 |
| $b$ | $s_1$ | $-2$ | 1 |

When the previous transition under action $b$ reached $s_1$, the episode continued with action $d$ and reward 5 on reaching $T$.

A new episode now begins. Aster takes action $b$ in $s_0$ and observes

$$
s_0 \xrightarrow{b, -2} s_1.
$$

Its exploring behavior policy then selects action $d$, producing

$$
s_1 \xrightarrow{d, 5} T.
$$

Consider how different active reinforcement learning methods use this experience.

### (a) Active ADP

After observing the new transition $s_0 \xrightarrow{b, -2} s_1$, update the estimated transition probabilities for actions $a$ and $b$ at $s_0$.

Suppose the current utility estimates from the learned model are

$$
U(s_1) = 4, \qquad U(T) = 0.
$$

Using the updated model, compute the expected value of actions $a$ and $b$ at $s_0$ and determine the greedy action.

### Answer

> _To be completed._

### (b) Monte Carlo Control

Before the new episode, the observed complete returns following $(s_0, b)$ were

$$
6, \qquad 6, \qquad 6, \qquad 2.
$$

Compute the return following $(s_0, b)$ in the new episode and update the Monte Carlo estimate $Q(s_0, b)$ using all five returns.

### Answer

> _To be completed._

### (c) SARSA and Q-learning

Consider separate SARSA and Q-learning agents with learning rate $\alpha = 0.5$ and the following current Q-values:

|  | First action | Second action |
| --- | --- | --- |
| $s_0$ | $Q(s_0, a) = 3$ | $Q(s_0, b) = 2$ |
| $s_1$ | $Q(s_1, c) = 4$ | $Q(s_1, d) = 1$ |

Both agents observe

$$
s_0 \xrightarrow{b, -2} s_1,
$$

and the behavior policy selects action $d$ in $s_1$.

Compute the updated value of $Q(s_0, b)$ using:

- **SARSA**;
- **Q-learning**.

### Answer

> _To be completed._

### (d)

Suppose the behavior policy had selected action $c$ rather than $d$ in $s_1$. What would happen to the SARSA and Q-learning updates?

### Answer

> _To be completed._

### (e)

Compare the four active RL methods. What does each learn, and how does each use experience to improve its policy?

### Answer

> _To be completed._

### (f)

Why is exploration necessary for all four methods?

### Answer

> _To be completed._

## (Optional) Problem 3: Reinforcement Learning in the Real World

Reinforcement learning is a general computational framework for learning from interaction and feedback. It has important connections to the study of learning and decision making in behavioral psychology and neuroscience, and related ideas arise in evolution and education.

**a.** Investigate how reinforcement learning ideas can be used to model human behavior and decision making.

### Answer

> _To be completed._

**b.** How is reinforcement learning relevant to one of these fields—evolution and adaptive behavior, behavioral psychology, neuroscience, or education? What connection, if any, exists between innate or biologically grounded reward signals and decision making in that area? How have findings or insights from that area influenced the development of reinforcement learning techniques in machine learning or AI?

### Answer

> _To be completed._
