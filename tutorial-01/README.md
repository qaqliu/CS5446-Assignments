# Tutorial 1

[中文](#中文) · [English](#english)

## 中文

### 作业简介

本目录用于整理 NUS CS5446《Reinforcement Learning and Sequential Decision Making》的 Tutorial 1：**Real World Planning and Acting**。本次作业主要包含以下三个规划问题：

1. **Blocks World**：使用 PDDL 描述一个需要将积木 B 从积木 A 和 C 之间移到桌面上的规划问题，并完成 forward search 搜索树和一个有效行动序列。
2. **Heuristic for Planning**：解释在目标和动作前置条件均为正文字面量时，移除所有 negative effects 为什么可以得到 relaxed problem；同时分析当允许 negative preconditions 或 negative goals 时是否仍然成立。
3. **Hierarchical Task Planning**：根据给定的 fluents（A–E）和 primitive actions（P1–P10），定义高层动作 H1、H2、H3 的前置条件、效果和可能实现，并判断从初始状态 $\neg A \land B$ 到目标状态 $E$ 的有效 HLA action sequences。

具体题目和解答请见 [`solution.md`](solution.md)。

### 目录结构

```text
tutorial-01/
├── README.md
├── solution.md
└── pictures/  # 存放 solution.md 中使用的插图
```

### 作业 TODO

- [ ] 完成并检查 solution.md 中 Problem 1–3 的全部解答。

## English

### Assignment Overview

This directory contains Tutorial 1, **Real World Planning and Acting**, for NUS CS5446 *Reinforcement Learning and Sequential Decision Making*. It covers the following three planning problems:

1. **Blocks World**: Express a problem in which block B is removed from between blocks A and C and placed on the table using PDDL, then provide the forward-search tree and a valid action sequence.
2. **Heuristic for Planning**: Explain why removing all negative effects produces a relaxed problem when goals and action preconditions are positive literals, and analyze whether this remains true when negative preconditions or negative goals are allowed.
3. **Hierarchical Task Planning**: Given the fluents A–E and primitive actions P1–P10, define the preconditions, effects, and possible implementations of the higher-level actions H1, H2, and H3, then determine which HLA action sequences achieve goal E from the initial state $\neg A \land B$.

The questions and solutions are available in [`solution.md`](solution.md).

### Directory Structure

```text
tutorial-01/
├── README.md
├── solution.md
└── pictures/  # Figures used in solution.md
```

### Assignment TODO

- [ ] Complete and review all solutions to Problems 1–3 in solution.md.