# How to Start

## Set Up the Environment
```bash
pip install -r requirements.txt
```

## Usage on Colab
If you want to work entirely on Colab, please upload the solution package folder to your Google Drive. Then, copy the folder name ```YourSolutionPackageFolderName``` and add the following snippet at the beginning of each .ipynb file that requires loading module ```EleEnv```:

```bash
from google.colab import drive
drive.mount('/content/drive')

!cd /content/drive/MyDrive/YourSolutionPackageFolderName && ls -R
```

You can install the dependency on Colab by (with an additional exclamation point):
```bash
!pip install -r requirements.txt
```

## Problem 1: AI Use and Evaluation (2 points)

Problem 1 explicitly permits and encourages AI assistance. You may use any AI
tool, make as many requests as useful, and ask it to generate, critique, test,
or revise PDDL. Prompt transcripts and prompt-writing style are not graded. You
are responsible for checking the technical correctness of the submitted model.

The foundational problem generator uses this fixed configuration schema:

```python
config = {
    "num_levels": 5,
    "elevator_start": 2,
    "requests": [(0, 4), (4, 1), (2, 2)],
}
```

Each request is `(start_floor, goal_floor)` for one passenger. Multiple people
may share a start or goal, and a person may already be at their goal.

The capacity extension adds exactly one field:

```python
capacity_config = {
    "num_levels": 5,
    "elevator_start": 2,
    "capacity": 2,
    "requests": [(0, 4), (0, 1), (2, 2)],
}
```

It uses a `c0 -> ... -> cC` count chain, static destinations, and `reached`.
Passengers already at their destination are reached initially and cannot board
again.

Problem 1 is worth 2 points. The foundational domain and foundational problem
generator are formative and ungraded, but they must still be completed for the
notebook's end-to-end foundational examples and checks to run. The
destination/capacity domain and the capacity-aware problem generator are worth
1 point each.

Hidden tests use only the input classes documented in the notebook. The
AI-audit questions are guided learning activities and carry no separate marks;
the optional `optional_ai_audit_notes` field in `1_PDDL_solution.py` gives you
space to keep brief answers, but the autograder does not read it and leaving it
blank has no effect on your score. No AI usage record is graded.

## Problem 2: Hierarchical Planning and Service Quality (8 points)

Problem 2 uses the same generalized passenger setting, extended with service
priorities. Its fixed configuration schema is:

```python
config = {
    "num_levels": 5,
    "elevator_start": 2,
    "capacity": 2,
    "requests": [
        {"start": 0, "goal": 4, "deadline": 16,
         "base_utility": 100, "late_penalty": 8},
    ],
}
```

`requests[i]` belongs to `person{i + 1}`, exactly as in Problem 1. Every service order must contain all
passenger indices exactly once. Shared starts or goals, passengers already at
their goal, arbitrary elevator starts, zero passengers, and one-floor buildings
are all valid.

After filtering initially reached passengers, the policy order is split into
consecutive batches of at most `capacity`. Every passenger in a batch is picked
up in order before anyone in that batch is delivered; deliveries use the same
order. Only then does the next batch begin.

The HTN deliberately carries forward Problem 1's `destination`, `reached`,
`c0 -> ... -> cC`, `lift_count`, and `next_count` representation. The supplied
type hierarchy, objects, fluents, and initial state are fixed. A submission must
contain exactly five primitive actions (`move_elevator`, `load`, `unload`,
`open_door`, `close_door`), three abstract tasks, and five specified methods;
extra schema elements lose structure credit.

The HTN uses instantaneous actions, but quality is evaluated externally:

- moving from floor `a` to `b` costs `abs(a - b)` time units;
- opening, closing, loading, and unloading cost one time unit each;
- completion time is measured immediately after a passenger unloads;
- passengers already at their goal have completion time zero.

```python
lateness = max(0, completion_time - deadline)
utility = max(0, base_utility - late_penalty * lateness)
```

The quality objective is maximum total utility. Completion times and travel are
reported by the evaluator but do not contribute separate marks. Grading uses ten
equally weighted configurations with capacities from 1 through 3. The active
passenger counts are distributed as follows:

| Active passengers | Share of quality configurations |
| --- | ---: |
| 1--5 | 20% |
| 6--7 | 20% |
| 8--9 | 30% |
| 10 | 30% |

Each policy call runs in a separate process with a hard 10-second limit; an
overrunning process is terminated. Each Aries solve also has a 10-second limit.

Problem 2 is worth 8 points: primitive actions (1), five HTN methods (1), the
ordered initial task network (1), solvability and independent plan replay (3),
and plan quality (2). Replay credit is averaged across the correctness
configurations. Quality is scored continuously between the minimum and
maximum attainable utility for each configuration. For each configuration,
`q = clip((U_student - U_min) / (U_max - U_min), 0, 1)` (or `q = 1` when
`U_min == U_max`), and the quality score is `2 * mean(q)`. Thus a fully correct
fixed HTN and replay earn 6 points, with up to 2 further quality points. The grader independently
replays the returned primitive plan, so changing the supplied evaluator cannot
change a score. No AI prompt transcript or iteration record is graded.

Here, `U_min` and `U_max` are the exact minimum and maximum total utilities over
all valid passenger permutations for that configuration. A quality case
receives utility credit only if the submitted HTN builds the required task
network, Aries returns a plan, and the plan passes independent replay;
otherwise that case receives zero quality credit.

## Problem 3: Free-form Planning (Optional, 2 Bonus Points)

Problem 3 removes the fixed HTN representation but keeps Problem 2's
configuration schema, passenger-index mapping, capacity batching, timing model,
and utility function. Its twenty bonus configurations include larger instances
and use a stricter 2-second hard limit for each hidden case. Implement `choose_service_order(config)` in
`3_freeform_planning_solution.py` using any finite algorithm. Passengers do not
walk or change queues.

Hidden bonus configurations use 12--20 floors, capacities from 1 through 3,
and at most 18 total requests. Deadlines lie between 18 and 140, base utilities
between 120 and 260, and late penalties between 3 and 12. The scale table below
counts active passengers after initially completed requests are filtered.

The grading environment provides the Python standard library and the packages
listed in `requirements.txt`, including NumPy, SciPy, OR-Tools, and PuLP. LLM
tools may be used to develop and debug the algorithm, but a submitted policy
should not call a live LLM API during grading: network access and credentials
are not provided, and any such call would remain inside the hard time limit.

| Active passengers | Share of bonus configurations |
| --- | ---: |
| 9--10 | 10% |
| 12--13 | 20% |
| 14--16 | 40% |
| 17--18 | 30% |

The bonus is worth at most 2 points. Bonus points fill in points lost in
Problems 1 and 2, with the final assignment grade capped at 10 points. Each of
the twenty hidden configurations is
worth 0.1 point and is accepted only when the returned value is a valid
permutation that attains at least 98% of the optimal total utility within 2 seconds. Runtime
below 2 seconds is not ranked and creates no additional score; completion time
and travel are diagnostic only.

## Generative AI Usage & Declaration

The use of Generative AI tools (such as ChatGPT, Claude, Copilot, etc.) is permitted for this assignment in accordance with course guidelines.

- Declaring AI usage is not graded (AI usage records, prompts, and audit notes will not impact your score).
- If you wish to document or declare your AI tool usage, prompt logs, or reflections for transparency, you may do so by filling out `ai_usage.md`.
- Students remain solely responsible for the technical correctness and understanding of all submitted code and models.
