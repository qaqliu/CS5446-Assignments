# Tutorial 3

[中文](#中文) · [English](#english)

## 中文

### 作业简介

本目录用于整理 NUS CS5446《Reinforcement Learning and Sequential Decision Making》的 Tutorial 3：**Sequential Decision Making under Uncertainty**。本次作业主要包含以下两道必做书面推理题和一道可选开放题：

1. **Nova the Mars Rover**：将 Nova 火星车的充电状态与节能/高功率模式建模为无限时域 MDP，讨论折扣因子的作用与最优策略变化，并使用价值迭代和策略迭代求解。
2. **Aster's Rescue Route—Comparing Active RL Methods**：根据 Aster 救援无人机的观测经验，分别分析 Active ADP、Monte Carlo Control、SARSA 和 Q-learning 的模型或价值更新、策略改进与探索需求。
3. **Reinforcement Learning in the Real World**（可选）：调研强化学习如何建模人类行为和决策，以及其与演化、行为心理学、神经科学或教育的联系。

本次 Tutorial 为第 5 周的书面推理练习，不涉及代码实现、编程文件、代码提交或实验环境配置。具体原题与答题占位区请见 [`solution.md`](solution.md)。

### 目录结构

```text
tutorial-03/
├── README.md
└── solution.md  # 原题与答题占位区
```

### 作业 TODO

- [x] 完成并检查 solution.md 中 Problem 1–2 的全部解答。
- [ ] （可选）完成 Problem 3 的调研与书面回答。

## English

### Assignment Overview

This directory contains Tutorial 3, **Sequential Decision Making under Uncertainty**, for NUS CS5446 *Reinforcement Learning and Sequential Decision Making*. It covers the following two required written reasoning problems and one optional open-ended problem:

1. **Nova the Mars Rover**: Model Nova's battery state and eco/boost operating modes as an infinite-horizon MDP, discuss the role of discounting and changes in the optimal policy, then solve the MDP with value iteration and policy iteration.
2. **Aster's Rescue Route—Comparing Active RL Methods**: Use Aster the rescue drone's observed experience to analyse model or value updates, policy improvement, and exploration for Active ADP, Monte Carlo Control, SARSA, and Q-learning.
3. **Reinforcement Learning in the Real World** (optional): Investigate how reinforcement learning models human behaviour and decision making, and its connections to evolution, behavioural psychology, neuroscience, or education.

This is a Week 5 written-reasoning tutorial. It does not require code implementation, programming files, code submission, or an experimental environment. The original questions and answer placeholders are available in [`solution.md`](solution.md).

### Directory Structure

```text
tutorial-03/
├── README.md
└── solution.md  # Original questions and answer placeholders
```

### Assignment TODO

- [x] Complete and review all solutions to Problems 1–2 in solution.md.
- [ ] (Optional) Complete the research and written response for Problem 3.
