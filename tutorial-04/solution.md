# Tutorial 4 : Function Approximation and Policy Search

> National University of Singapore · School of Computing  
> CS4246/CS5446 Reinforcement Learning and Sequential Decision Making  
> Semester 1, AY2026-27 · Issued: 26 Aug 2026

**Group Members**

- Zhang Jiazheng (A0314707H)
- Phyo Han (A0196680R)
- Wang Shiyu (A0354696L)
- Liu Hengyan (A0350634J)
- Cui Yi (A0353244J)

## AI Assistance Declaration

> ChatGPT was used to help transcribe the tutorial questions into Markdown and prepare answer placeholders. I remain responsible for the accuracy, originality, and final content of this submission.

## Guidelines

You may discuss the content of the questions with your classmates. But everyone should work on and be ready to present **ALL** the solutions.

## Problem 1: Review

Briefly explain the following concepts.

**(a) Linear regression and loss-function optimization.**

### Answer

Linear regression approximates an output using a weighted combination of input features:

\[
\hat{y}=\theta_0+\theta_1x_1+\cdots+\theta_nx_n
\]

or, in vector form,

\[
\hat{y}_\theta(s)=\theta^\top\phi(s).
\]

The parameters are learned by minimizing a loss function. For example, the mean squared error is

\[
L(\theta)=\frac{1}{2}\sum_{i=1}^{N}\left(y_i-\hat{y}_\theta(s_i)\right)^2.
\]

The objective is to find parameters \(\theta\) that make the predictions as close as possible to the target values.

**(b) Gradient descent.**

### Answer

Gradient descent minimizes a loss function by repeatedly moving the parameters in the opposite direction of the gradient:

\[
\theta\leftarrow\theta-\alpha\nabla_\theta L(\theta),
\]

where \(\alpha\) is the learning rate. The gradient points in the direction of greatest increase in the loss, so the negative gradient decreases the loss.

**(c) Deep learning in neural networks.**

### Answer

Deep learning uses neural networks with multiple hidden layers. Each layer applies a weighted transformation followed by a nonlinear activation function:

\[
h^{(l)}=f\left(W^{(l)}h^{(l-1)}+b^{(l)}\right).
\]

The network learns useful representations of the input and the final prediction or decision. The parameters are usually learned using backpropagation and gradient descent. In reinforcement learning, neural networks can approximate value functions, action-value functions, or policies from high-dimensional inputs such as images.

## Problem 2: Approximating TD Learning

In a navigation task, the agent's state is its position $s=(x,y)$, and the goal is at $(x_g,y_g)$. When the set of possible positions is large or continuous, storing a separate utility for every state is impractical. We therefore approximate state utility using the coordinates and the Euclidean distance to the goal as features. After observing a transition $(s,r,s')$, the agent applies one-step TD learning with learning rate $alpha$ and discount factor $gamma$.

Write out the parameter update equations for temporal-difference (TD) learning with

$$
\hat U_{\theta}(x,y)=\theta_0+\theta_1x+\theta_2y+\theta_3\sqrt{(x-x_g)^2+(y-y_g)^2}.
$$

### Answer

Define the distance from the current position to the goal as

\[
d(x,y)=\sqrt{(x-x_g)^2+(y-y_g)^2}.
\]

The approximated utility function is

\[
\hat{U}_\theta(x,y)=\theta_0+\theta_1x+\theta_2y+\theta_3d(x,y).
\]

For a transition \((s,r,s')\), where \(s=(x,y)\) and \(s'=(x',y')\), the one-step TD error is

\[
\delta=r+\gamma\hat{U}_\theta(x',y')-\hat{U}_\theta(x,y).
\]

The semi-gradient TD update is

\[
\theta\leftarrow\theta+\alpha\delta\frac{\partial \hat{U}_\theta(s)}{\partial\theta}.
\]

Therefore,

\[
\theta_0\leftarrow\theta_0+\alpha\delta,
\]

\[
\theta_1\leftarrow\theta_1+\alpha\delta x,
\]

\[
\theta_2\leftarrow\theta_2+\alpha\delta y,
\]

\[
\theta_3\leftarrow\theta_3+\alpha\delta\sqrt{(x-x_g)^2+(y-y_g)^2}.
\]

Expanding the TD error:

\[
\begin{aligned}
\delta={}&r+\gamma\left[\theta_0+\theta_1x'+\theta_2y'
 +\theta_3\sqrt{(x'-x_g)^2+(y'-y_g)^2}\right]\\
&-\left[\theta_0+\theta_1x+\theta_2y
 +\theta_3\sqrt{(x-x_g)^2+(y-y_g)^2}\right].
\end{aligned}
\]

If \(s'\) is terminal, use \(\hat{U}_\theta(s')=0\).

## Problem 3: Approximating Q-Learning

Q-learning is a model-free, off-policy TD control method. It does not need a model of the environment's transition dynamics. Instead, each observed transition $(s,a,r,s')$ is used to update the sampled state-action pair toward a target containing the immediate reward and the best estimated action value at the next state. This problem first applies the tabular update, then replaces the table with a simple function approximator.

Consider a system with a single state variable $x\in\{0,1\}$ and actions $a_1$ and $a_2$. An agent observes the state and reward. Assume $gamma=0.9$.

**(a) Perform two steps of tabular Q-learning.** Use $alpha=0.5$ and initialize all entries to zero. Show the table after each step.

Use

$$
Q(s,a)\leftarrow Q(s,a)+\alpha\left[r+\gamma\max_{a'}Q(s',a')-Q(s,a)\right].
$$

1. First transition: $x=0$, reward $r=10$, action $a_1$, next state $x'=1$.
2. Second transition: $x=1$, reward $r=-5$, action $a_2$, next state $x'=0$.

### Answer

Initially,

| State \(x\) | \(Q(x,a_1)\) | \(Q(x,a_2)\) |
|---|---:|---:|
| \(0\) | \(0\) | \(0\) |
| \(1\) | \(0\) | \(0\) |

#### Step 1

Transition:

\[
x=0,\qquad r=10,\qquad a=a_1,\qquad x'=1.
\]

The target is

\[
r+\gamma\max_{a'}Q(1,a')=10+0.9\max(0,0)=10.
\]

Therefore,

\[
Q(0,a_1)\leftarrow 0+0.5(10-0)=5.
\]

Table after Step 1:

| State \(x\) | \(Q(x,a_1)\) | \(Q(x,a_2)\) |
|---|---:|---:|
| \(0\) | \(5\) | \(0\) |
| \(1\) | \(0\) | \(0\) |

#### Step 2

Transition:

\[
x=1,\qquad r=-5,\qquad a=a_2,\qquad x'=0.
\]

At the next state,

\[
\max_{a'}Q(0,a')=\max(5,0)=5.
\]

The target is

\[
r+\gamma\max_{a'}Q(0,a')=-5+0.9(5)=-0.5.
\]

Therefore,

\[
Q(1,a_2)\leftarrow 0+0.5(-0.5-0)=-0.25.
\]

Table after Step 2:

| State \(x\) | \(Q(x,a_1)\) | \(Q(x,a_2)\) |
|---|---:|---:|
| \(0\) | \(5\) | \(0\) |
| \(1\) | \(0\) | \(-0.25\) |

**(b) Now use $Q(x,a_1)=\beta_1x$ and $Q(x,a_2)=\beta_2x$.** Let $alpha=0.5$ and initialize $beta_1=\beta_2=0$. Show the parameters after each step.

Use

$$
\beta_i\leftarrow\beta_i+\alpha\delta\frac{\partial Q(x,a)}{\partial\beta_i},
\qquad
\delta=r+\gamma\max_{a'}Q(x',a')-Q(x,a).
$$

1. First transition: $x=1$, reward $r=10$, action $a_1$, next state $x'=1$.
2. Second transition: $x=1$, reward $r=-5$, action $a_2$, next state $x'=0$.

### Answer

#### Step 1

Transition:

\[
x=1,\qquad r=10,\qquad a=a_1,\qquad x'=1.
\]

The current value and next-state values are initially zero, so

\[
\delta=10+0.9(0)-0=10.
\]

Since

\[
\frac{\partial Q(1,a_1)}{\partial\beta_1}=1,
\]

we obtain

\[
\beta_1\leftarrow 0+0.5(10)(1)=5.
\]

The parameter \(\beta_2\) is unchanged. Thus,

\[
\boxed{\beta_1=5,\qquad\beta_2=0}.
\]

#### Step 2

Transition:

\[
x=1,\qquad r=-5,\qquad a=a_2,\qquad x'=0.
\]

At \(x'=0\),

\[
Q(0,a_1)=\beta_1(0)=0,
\qquad
Q(0,a_2)=\beta_2(0)=0.
\]

Therefore,

\[
\delta=-5+0.9(0)-0=-5.
\]

Since

\[
\frac{\partial Q(1,a_2)}{\partial\beta_2}=1,
\]

we get

\[
\beta_2\leftarrow 0+0.5(-5)(1)=-2.5.
\]

Hence,

\[
\boxed{\beta_1=5,\qquad\beta_2=-2.5}.
\]

**(c) After enough data is observed, which method should perform better here? Why? How can the poorer representation be improved?**

### Answer

The tabular method should perform better for this problem because it represents every state-action pair independently.

The function approximator has the limitation

\[
Q(0,a_1)=\beta_1(0)=0,
\qquad
Q(0,a_2)=\beta_2(0)=0.
\]

Thus, it can never represent nonzero values at state \(x=0\). The tabular method does not have this restriction.

The representation can be improved by adding an intercept for each action:

\[
Q(x,a_1)=\beta_{1,0}+\beta_{1,1}x,
\]

\[
Q(x,a_2)=\beta_{2,0}+\beta_{2,1}x.
\]

Alternatively, one-hot state-action features can be used, giving one independent parameter for every state-action pair.

## Problem 4: Persy the Mars Rover Learns by REINFORCE

Persy is a Mars rover that must learn to navigate from camera observations without being given the correct action for each image. At each time step, it observes a camera state $s$ and samples a drive command (forward, left, right, or stop). The environment supplies rewards, and the return from an episode indicates how well the resulting trajectory performed. Persy's stochastic softmax policy $\pi_{\theta}(a\mid s)$, parameterised by network weights $\theta$, gives the probability of choosing action $a$ in state $s$. It is trained using REINFORCE, a Monte Carlo policy-gradient algorithm that learns from completed episodes.

Let $r_t$ be the reward received after taking action $a_t$ in state $s_t$. For an episode with $T$ actions, define the discounted return by

$$
G_t=\sum_{k=t}^{T-1}\gamma^{k-t}r_k,
$$

where $gamma$ is the discount factor.

**(a) Why does REINFORCE use $\nabla_{\theta}\log\pi_{\theta}(a_t\mid s_t)G_t$? Explain each part.**

### Answer

REINFORCE maximizes the expected return

\[
J(\theta)=\mathbb{E}_{\tau\sim\pi_\theta}[R(\tau)].
\]

Its policy-gradient estimate is

\[
\nabla_\theta J(\theta)
\approx
\sum_t\nabla_\theta\log\pi_\theta(a_t\mid s_t)G_t.
\]

Here:

- \(\pi_\theta(a_t\mid s_t)\) is the probability of selecting action \(a_t\) in state \(s_t\).
- \(\nabla_\theta\log\pi_\theta(a_t\mid s_t)\) indicates how the policy parameters should change to make the selected action more or less likely.
- \(G_t\) is the discounted return after time \(t\):

\[
G_t=\sum_{k=t}^{T-1}\gamma^{k-t}r_k.
\]

If \(G_t\) is large and positive, the probability of the selected action is increased. If \(G_t\) is negative, the probability is decreased.

REINFORCE does not require correct action labels or a differentiable model of the environment. It learns from rewards obtained from sampled trajectories.

**(b) Baseline and state value.** A baseline $b(s_t)$ is a state-dependent reference value that does not depend on the action sampled at that state. REINFORCE can use $G_t-b(s_t)$ in place of $G_t$ to weight the policy gradient. The state-value function $V_{\pi}(s)$ is the expected discounted return starting from state $s$ and following the current policy $\pi=\pi_{\theta}$. Thus $G_t$ is the return from one sampled episode, whereas $V_{\pi}(s_t)$ is an average over possible future trajectories.

How does subtracting a baseline help, and why is $b(s_t)=V_{\pi}(s_t)$ a good choice?

### Answer

REINFORCE can use

\[
G_t-b(s_t)
\]

instead of \(G_t\). Since the baseline does not depend on the action, it does not change the expected gradient:

\[
\begin{aligned}
\mathbb{E}_{a\sim\pi}\left[b(s)\nabla_\theta\log\pi_\theta(a\mid s)\right]
&=b(s)\sum_a\pi_\theta(a\mid s)\nabla_\theta\log\pi_\theta(a\mid s)\\
&=b(s)\sum_a\nabla_\theta\pi_\theta(a\mid s)\\
&=b(s)\nabla_\theta\sum_a\pi_\theta(a\mid s)\\
&=0.
\end{aligned}
\]

The baseline reduces variance by subtracting the typical return for that state.

A natural choice is

\[
b(s_t)=V_\pi(s_t),
\]

where

\[
V_\pi(s_t)=\mathbb{E}[G_t\mid s_t].
\]

Then,

\[
G_t-V_\pi(s_t)
\]

estimates the advantage:

\[
A_\pi(s_t,a_t)=Q_\pi(s_t,a_t)-V_\pi(s_t).
\]

**(c) An episode terminates after three actions, with rewards $r_0=1$, $r_1=0$, $r_2=2$, and $gamma=0.9$. Compute $G_0$ and $G_1$.**

### Answer

Given

\[
r_0=1,\qquad r_1=0,\qquad r_2=2,\qquad \gamma=0.9,
\]

\[
\begin{aligned}
G_0
&=r_0+\gamma r_1+\gamma^2r_2\\
&=1+0.9(0)+(0.9)^2(2)\\
&=\boxed{2.62}.
\end{aligned}
\]

\[
\begin{aligned}
G_1
&=r_1+\gamma r_2\\
&=0+0.9(2)\\
&=\boxed{1.8}.
\end{aligned}
\]

## Problem 5: PPO and the Spacecraft Attitude Controller

A spacecraft controller is trained with PPO. Let

$$
r_t(\theta)=\frac{\pi_{\theta}(a_t\mid s_t)}{\pi_{\mathrm{old}}(a_t\mid s_t)}.
$$

**(a) Policy ratio meaning.** What does the probability ratio $r_t(\theta)$ mean?

### Answer

The ratio compares the probability assigned to the same action by the new and old policies.

- \(r_t(\theta)=1\): the probability is unchanged.
- \(r_t(\theta)>1\): the new policy makes the action more likely.
- \(r_t(\theta)<1\): the new policy makes the action less likely.

**(b) Advantage sign.** What does the sign of the estimated advantage $\hat A_t$ mean?

### Answer

- \(\hat{A}_t>0\): the action was better than expected, so its probability should increase.
- \(\hat{A}_t<0\): the action was worse than expected, so its probability should decrease.
- \(\hat{A}_t=0\): the action was approximately as good as expected.

**(c) Clipping calculation.** Let $\epsilon=0.2$ and $r_t=1.3$. Compute $\mathrm{clip}(r_t,1-\epsilon,1+\epsilon)$.

### Answer

Given

\[
\epsilon=0.2,\qquad r_t=1.3,
\]

the clipping interval is

\[
[1-\epsilon,1+\epsilon]=[0.8,1.2].
\]

Therefore,

\[
\operatorname{clip}(1.3,0.8,1.2)=\boxed{1.2}.
\]

**(d) Objective calculation.** Now let $\hat A_t=2.0$. Compute the unclipped and clipped terms

$$
u=r_t\hat A_t,
\qquad
c=\mathrm{clip}(r_t,1-\epsilon,1+\epsilon)\hat A_t.
$$

Then compute the per-sample PPO objective

$$
L_t^{\mathrm{clip}}=\min(u,c).
$$

The minimum is taken after multiplying by the advantage, whether $\hat A_t$ is positive or negative.

### Answer

Given \(\hat{A}_t=2.0\), the unclipped term is

\[
u=r_t\hat{A}_t=1.3(2.0)=\boxed{2.6}.
\]

The clipped term is

\[
c=\operatorname{clip}(r_t,0.8,1.2)\hat{A}_t=1.2(2.0)=\boxed{2.4}.
\]

The per-sample PPO objective is

\[
L_t^{\mathrm{clip}}=\min(u,c)=\min(2.6,2.4)=\boxed{2.4}.
\]

**(e) Conceptual benefit.** How does PPO clipping compare with the KL-divergence constraint in TRPO?

### Answer

TRPO explicitly constrains the policy update using a KL-divergence condition such as

\[
\mathbb{E}\left[D_{\mathrm{KL}}\left(\pi_{\mathrm{old}}\|\pi_\theta\right)\right]\leq\delta.
\]

This gives direct trust-region control but requires a more computationally expensive constrained optimization procedure.

PPO clips the probability ratio to the interval

\[
[1-\epsilon,1+\epsilon].
\]

This discourages excessively large policy updates and is simpler to implement. However, clipping is an approximate local constraint and does not guarantee that the actual KL divergence remains below a fixed bound.

Therefore:

- **TRPO:** stronger explicit KL-divergence constraint, but more complex and expensive.
- **PPO:** simpler and cheaper clipping mechanism, but without the same strict trust-region guarantee.