# Tutorial 4

[中文](#中文) · [English](#english)

## 中文

### 作业简介

本目录用于整理 NUS CS5446《Reinforcement Learning and Sequential Decision Making》的 Tutorial 4：**Function Approximation and Policy Search**。本次作业包含五道书面推理题：

1. **Review**：简要解释线性回归与损失函数优化、梯度下降，以及神经网络中的深度学习。
2. **Approximating TD Learning**：在连续或大规模导航状态空间中，以坐标与目标距离为特征，推导线性状态效用近似器的一步 TD 参数更新。
3. **Approximating Q-Learning**：比较表格型 Q-learning 与简单线性动作价值近似器的两步更新，并讨论表示能力对最终性能的影响。
4. **Persy the Mars Rover Learns by REINFORCE**：解释 REINFORCE 策略梯度、baseline 与状态价值的作用，并计算给定轨迹的折扣回报。
5. **PPO and the Spacecraft Attitude Controller**：解释 PPO 的策略概率比、优势函数符号、裁剪目标，以及 PPO 裁剪和 TRPO KL 散度约束的关系。

本次 Tutorial 为第 6 周的书面推理练习，不涉及代码实现、编程文件、代码提交或实验环境配置。具体原题与答题区请见 [`solution.md`](solution.md)。

### 目录结构

```text
tutorial-04/
├── README.md
└── solution.md  # 原题与答题占位区
```

### 作业 TODO

- [ ] 完成并检查 solution.md 中 Problem 1–5 的全部解答。

## English

### Tutorial overview

This directory contains Tutorial 4, **Function Approximation and Policy Search**, for NUS CS5446 *Reinforcement Learning and Sequential Decision Making*. It contains five written reasoning problems:

1. **Review**: Briefly explain linear regression and loss-function optimisation, gradient descent, and deep learning in neural networks.
2. **Approximating TD Learning**: Derive a one-step TD parameter update for a linear state-utility approximator that uses coordinates and distance to the goal as features.
3. **Approximating Q-Learning**: Compare two tabular Q-learning updates with updates using a simple linear action-value approximator, then discuss representational capacity.
4. **Persy the Mars Rover Learns by REINFORCE**: Explain the REINFORCE policy gradient, baselines, and state values, then calculate discounted returns for a given episode.
5. **PPO and the Spacecraft Attitude Controller**: Explain PPO probability ratios, advantage signs, clipping objectives, and the relationship between PPO clipping and the KL-divergence constraint in TRPO.

This is a Week 6 written-reasoning tutorial. It does not require code implementation, programming files, code submission, or an experimental environment. The original questions and answer spaces are available in [`solution.md`](solution.md).

### Directory structure

```text
tutorial-04/
├── README.md
└── solution.md  # Original questions and answer placeholders
```

### Tutorial TODO

- [ ] Complete and review all solutions to Problems 1–5 in solution.md.
