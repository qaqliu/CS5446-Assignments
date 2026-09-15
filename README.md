# NUS CS5446 — Reinforcement Learning and Sequential Decision Making

[中文](#中文) · [English](#english)

---

## 中文

本仓库用于整理 NUS CS5446《Reinforcement Learning and Sequential Decision Making》（强化学习与序列决策）课程的 Tutorial、Assignment 和 Project 相关材料。

每个 Tutorial、Assignment 和 Project 均使用仓库根目录下的独立文件夹保存相关内容，例如题目说明、解答或代码、实验结果、环境配置及必要文档。具体内容会随任务类型而异。

## 目录结构

```text
.
├── tutorial-01/
├── tutorial-02/
├── tutorial-03/
├── tutorial-04/
├── ...
├── assignment-01/
├── project-01/
├── .gitignore
└── README.md
```

## 仓库使用

每个 Tutorial、Assignment 和 Project 都会在仓库根目录下使用一个独立文件夹。进入对应文件夹后，请先查看其中的解答文件、说明文档或项目文档，并在需要时按照提供的环境说明完成配置和运行。

```text
tutorial-01/
├── README.md
├── solution.md
└── ...

assignment-01/
├── README.md
├── requirements.txt
└── ...

project-01/
├── README.md
├── requirements.txt
└── ...
```

各个 Tutorial、Assignment 和 Project 文件夹中的解答文件或说明文档将酌情说明：

- 题目或项目目标
- 所需环境与依赖
- 代码运行方式
- 实验结果和提交说明

## Tutorials

### Tutorial 1 — Real World Planning and Acting

本次 Tutorial 是 NUS CS5446 的第一个作业，主题为 Real World Planning and Acting，包含与 Blocks World、Heuristic for Planning 和 Hierarchical Task Planning 相关的三个问题。

### Tutorial 2 — Rational Decision Making

本次 Tutorial 主题为理性决策，包含三个书面推理题：基于效用函数比较彩票偏好、用期望效用分析 PacBaby 的保险决策，以及通过 Allais 悖论讨论理性偏好与可替代性公理。

### Tutorial 3 — Sequential Decision Making under Uncertainty

本次 Tutorial 主题为不确定性下的序列决策，包含两道必做书面推理题和一道可选开放题：使用折扣、价值迭代和策略迭代分析 Nova 火星车的无限时域 MDP；比较 Active ADP、Monte Carlo Control、SARSA 与 Q-learning 如何利用 Aster 救援无人机的经验学习策略；以及探讨强化学习与现实世界中的人类行为、演化、心理学、神经科学或教育之间的联系。

### Tutorial 4 — Function Approximation and Policy Search

本次 Tutorial 主题为函数近似与策略搜索，包含五道书面推理题：复习线性回归、梯度下降与深度学习；推导 TD 和 Q-learning 的函数近似更新；分析 REINFORCE 的策略梯度与 baseline；并理解 PPO 的概率比、裁剪目标与其同 TRPO KL 约束的关系。。

## Assignments

### Assignment 1 — Elevator Planning

第一次 Assignment 以电梯乘客服务为背景，要求使用 Python 与规划工具完成三个部分：利用 PDDL 建模电梯规划问题并处理容量约束；使用分层任务网络（HTN）完成乘客服务规划并优化服务质量；以及一个可选的自由规划加分题。作业的环境配置、Notebook、源代码与提交说明位于 [`assignment-01/`](assignment-01/)。

## Project

课程项目相关内容将在项目主题确定后补充。

---

## English

This repository organizes materials for the Tutorials, Assignments, and Project of NUS CS5446, *Reinforcement Learning and Sequential Decision Making*.

Each Tutorial, Assignment, and Project has its own folder directly under the repository root. Depending on the task, these folders may contain the problem or project description, solutions or source code, experiment results, environment configuration, and related documentation.

## Directory Structure

```text
.
├── tutorial-01/
├── tutorial-02/
├── tutorial-03/
├── tutorial-04/
├── ...
├── assignment-01/
├── project-01/
├── .gitignore
└── README.md
```

## Repository Usage

Each Tutorial, Assignment, and Project has its own folder directly under the repository root. After entering the relevant folder, first review its solution, assignment, or project documentation, then follow any applicable environment and usage instructions.

```text
tutorial-01/
├── README.md
├── solution.md
└── ...

assignment-01/
├── README.md
├── requirements.txt
└── ...

project-01/
├── README.md
├── requirements.txt
└── ...
```

The solution or documentation in each Tutorial, Assignment, or Project folder will describe, where applicable:

- the problem or project objectives;
- the required environment and dependencies;
- how to run the code;
- experimental results and submission notes.

## Tutorials

### Tutorial 1 — Real World Planning and Acting

This is the first Tutorial for NUS CS5446 and focuses on real-world planning and acting. It contains three problems related to Blocks World, Heuristic for Planning, and Hierarchical Task Planning.

### Tutorial 2 — Rational Decision Making

This tutorial covers rational decision making through three written reasoning problems: matching lottery preferences to utility functions, analysing PacBaby's insurance decision with expected utility, and using the Allais paradox to examine rational preferences and the substitutability axiom.

### Tutorial 3 — Sequential Decision Making under Uncertainty

This tutorial covers sequential decision making under uncertainty through two required written reasoning problems and one optional open-ended problem: analysing Nova the Mars Rover's infinite-horizon MDP using discounting, value iteration, and policy iteration; comparing how Active ADP, Monte Carlo Control, SARSA, and Q-learning use Aster the rescue drone's experience to learn a policy; and investigating links between reinforcement learning and real-world human behaviour, evolution, psychology, neuroscience, or education.

### Tutorial 4 — Function Approximation and Policy Search

This tutorial covers function approximation and policy search through five written reasoning problems: reviewing linear regression, gradient descent, and deep learning; deriving function-approximation updates for TD learning and Q-learning; analysing the REINFORCE policy gradient and baselines; and understanding PPO probability ratios, clipping objectives, and their relationship to the KL-divergence constraint in TRPO.

## Assignments

### Assignment 1 — Elevator Planning

The first assignment uses an elevator passenger-service setting and consists of three parts: modelling an elevator planning problem in PDDL with capacity constraints; using a hierarchical task network (HTN) for passenger-service planning and service-quality optimisation; and an optional free-form planning bonus problem. Its environment setup, notebooks, source code, and submission instructions are in [`assignment-01/`](assignment-01/).

## Project

The course project section will be completed once the project topic has been decided.
