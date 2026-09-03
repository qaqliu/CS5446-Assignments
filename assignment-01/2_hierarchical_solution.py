"""Assignment 1 - Problem 2 hierarchical-planning submission template.

* Group Member 1:
    - Name:
    - Matric number:

* Group Member 2:
    - Name:
    - Matric number:

* Group Member 3:
    - Name:
    - Matric number:

* Group Member 4:
    - Name:
    - Matric number:
"""

from __future__ import annotations

from itertools import islice
from numbers import Integral
from typing import Any, Sequence

from unified_planning.model.htn import HierarchicalProblem, Method
from unified_planning.shortcuts import (
    BoolType,
    Equals,
    Fluent,
    InstantaneousAction,
    Not,
    Object,
    OneshotPlanner,
    UserType,
)


# The representation below is fixed. Hidden tests change values, not the schema.
# Each request is a dictionary with exactly these five keys.
REQUEST_KEYS = {"start", "goal", "deadline", "base_utility", "late_penalty"}


def validate_config(config: dict[str, Any]) -> None:
    """Validate the public Problem 2 configuration schema."""
    required = {"num_levels", "elevator_start", "capacity", "requests"}
    if not isinstance(config, dict) or set(config) != required:
        raise ValueError(f"config must contain exactly these keys: {sorted(required)}")

    num_levels = config["num_levels"]
    elevator_start = config["elevator_start"]
    capacity = config["capacity"]
    requests = config["requests"]
    if not isinstance(num_levels, int) or isinstance(num_levels, bool) or num_levels < 1:
        raise ValueError("num_levels must be a positive integer")
    if (
        not isinstance(elevator_start, int)
        or isinstance(elevator_start, bool)
        or not 0 <= elevator_start < num_levels
    ):
        raise ValueError("elevator_start must name an existing floor")
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
        raise ValueError("capacity must be a positive integer")
    if not isinstance(requests, (list, tuple)):
        raise ValueError("requests must be a list or tuple")

    for request in requests:
        if not isinstance(request, dict) or set(request) != REQUEST_KEYS:
            raise ValueError(
                "each request must contain exactly: start, goal, deadline, "
                "base_utility, late_penalty"
            )
        for key in REQUEST_KEYS:
            value = request[key]
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError(f"request {key} must be an integer")
        if not 0 <= request["start"] < num_levels:
            raise ValueError("request start must name an existing floor")
        if not 0 <= request["goal"] < num_levels:
            raise ValueError("request goal must name an existing floor")
        if request["deadline"] < 0:
            raise ValueError("deadline must be non-negative")
        if request["base_utility"] <= 0:
            raise ValueError("base_utility must be positive")
        if request["late_penalty"] <= 0:
            raise ValueError("late_penalty must be positive")


def validate_order(config: dict[str, Any], order: Sequence[int]) -> list[int]:
    """Return a normalized passenger permutation, safely rejecting bad iterables."""
    passenger_count = len(config["requests"])
    try:
        values = list(islice(iter(order), passenger_count + 1))
    except TypeError as error:
        raise ValueError("order must be an iterable of passenger indices") from error
    if (
        len(values) != passenger_count
        or any(
            not isinstance(index, Integral) or isinstance(index, bool)
            for index in values
        )
        or sorted(int(index) for index in values) != list(range(passenger_count))
    ):
        raise ValueError("order must contain every passenger index exactly once")
    return [int(index) for index in values]


def service_batches(config: dict[str, Any], order: Sequence[int]) -> list[list[int]]:
    """Split active passengers into consecutive capacity-sized batches."""
    order = validate_order(config, order)
    active = [
        index
        for index in order
        if config["requests"][index]["start"]
        != config["requests"][index]["goal"]
    ]
    capacity = config["capacity"]
    return [active[start : start + capacity] for start in range(0, len(active), capacity)]


def evaluate_service_order(config: dict[str, Any], order: Sequence[int]) -> dict[str, Any]:
    """Replay deterministic capacity batches using the external time model.

    Moving from floor ``a`` to floor ``b`` takes ``abs(a - b)`` time units.
    For each batch, all passengers board in order before anyone exits; they then
    exit in the same order. Opening, closing, loading, and unloading each take
    one time unit. Completion is measured immediately after unloading.
    """
    validate_config(config)
    order = validate_order(config, order)
    batches = service_batches(config, order)
    passenger_count = len(config["requests"])

    current_floor = config["elevator_start"]
    current_time = 0
    total_travel = 0
    completion_times = [0] * passenger_count

    for batch in batches:
        for index in batch:
            start = config["requests"][index]["start"]
            distance = abs(current_floor - start)
            total_travel += distance
            current_time += distance + 3  # move; open, load, close
            current_floor = start

        for index in batch:
            goal = config["requests"][index]["goal"]
            distance = abs(current_floor - goal)
            total_travel += distance
            current_time += distance + 2  # move; open, unload
            completion_times[index] = current_time
            current_time += 1  # close before the next task
            current_floor = goal

    utilities = []
    for request, completion_time in zip(config["requests"], completion_times):
        lateness = max(0, completion_time - request["deadline"])
        utilities.append(
            max(0, request["base_utility"] - request["late_penalty"] * lateness)
        )

    return {
        "order": order,
        "batches": batches,
        "completion_times": completion_times,
        "utilities": utilities,
        "total_utility": sum(utilities),
        "sum_completion_time": sum(completion_times),
        "max_completion_time": max(completion_times, default=0),
        "total_travel": total_travel,
        "finish_time": current_time,
    }


# COPY-FLAG-1-START

def choose_service_order(config: dict[str, Any]) -> list[int]:
    """Return a permutation of passenger indices.

    The starter policy is deliberately valid but usually suboptimal. Replace it
    with your own policy. The quality objective is maximum total utility.
    """
    validate_config(config)
    return list(range(len(config["requests"])))

# COPY-FLAG-1-END


def generate_hierarchical(config: dict[str, Any]) -> HierarchicalProblem:
    """Build the elevator HTN for ``config`` using ``choose_service_order``."""
    validate_config(config)
    order = choose_service_order(config)
    # Validate the policy before any UP objects are constructed.
    evaluate_service_order(config, order)

    problem = HierarchicalProblem("ElevatorHTNProblem")

    Loc = UserType("Loc")
    Floor = UserType("Floor", father=Loc)
    Elevator = UserType("Elevator", father=Loc)
    Person = UserType("Person")
    Count = UserType("Count")

    floors = [Object(f"floor{i}", Floor) for i in range(config["num_levels"])]
    people = [Object(f"person{i + 1}", Person) for i in range(len(config["requests"]))]
    elevator = Object("elevator", Elevator)
    counts = [Object(f"c{i}", Count) for i in range(config["capacity"] + 1)]
    problem.add_objects(floors + people + [elevator] + counts)

    at_person = Fluent("at_person", Loc, person=Person)
    at_elevator = Fluent("at_elevator", Floor, elevator=Elevator)
    elevator_door_open = Fluent("elevator_door_open", BoolType(), elevator=Elevator)
    destination = Fluent("destination", Floor, person=Person)
    reached = Fluent("reached", BoolType(), person=Person)
    lift_count = Fluent("lift_count", BoolType(), count=Count)
    next_count = Fluent("next_count", BoolType(), current=Count, next=Count)
    problem.add_fluent(at_person)
    problem.add_fluent(at_elevator)
    problem.add_fluent(elevator_door_open)
    problem.add_fluent(destination)
    problem.add_fluent(reached, default_initial_value=False)
    problem.add_fluent(lift_count, default_initial_value=False)
    problem.add_fluent(next_count, default_initial_value=False)

    for person, request in zip(people, config["requests"]):
        problem.set_initial_value(at_person(person), floors[request["start"]])
        problem.set_initial_value(destination(person), floors[request["goal"]])
        if request["start"] == request["goal"]:
            problem.set_initial_value(reached(person), True)
    problem.set_initial_value(at_elevator(elevator), floors[config["elevator_start"]])
    problem.set_initial_value(elevator_door_open(elevator), False)
    problem.set_initial_value(lift_count(counts[0]), True)
    for index in range(config["capacity"]):
        problem.set_initial_value(next_count(counts[index], counts[index + 1]), True)

    move_elevator = InstantaneousAction(
        "move_elevator", elevator=Elevator, start=Floor, end=Floor
    )
    load = InstantaneousAction(
        "load",
        elevator=Elevator,
        person=Person,
        floor=Floor,
        current=Count,
        next=Count,
    )
    unload = InstantaneousAction(
        "unload",
        elevator=Elevator,
        person=Person,
        floor=Floor,
        previous=Count,
        current=Count,
    )
    open_door = InstantaneousAction("open_door", elevator=Elevator)
    close_door = InstantaneousAction("close_door", elevator=Elevator)

    # COPY-FLAG-2-START

    # Add the exact preconditions and effects listed in Task 2. Do not add
    # extra guards such as start != end or not reached on unload.

    # COPY-FLAG-2-END

    problem.add_actions(
        [move_elevator, load, unload, open_door, close_door]
    )

    pickup_person = problem.add_task(
        "pickup_person", person=Person, start_floor=Floor
    )
    deliver_person = problem.add_task(
        "deliver_person", person=Person, goal_floor=Floor
    )
    confirm_reached = problem.add_task(
        "confirm_reached", person=Person, goal_floor=Floor
    )

    # COPY-FLAG-3-START

    # Add the five methods using the exact signatures, preconditions, and
    # ordered decompositions listed in Task 3.

    # COPY-FLAG-3-END

    # COPY-FLAG-4-START

    # Filter initially reached passengers, split the remaining order into
    # capacity-sized batches, add all pickups followed by all deliveries for
    # each batch, append confirm_reached tasks, and totally order the network.

    # COPY-FLAG-4-END

    return problem


def solve(problem: HierarchicalProblem, verbose: bool = False):
    """Solve and return the planner result (printing it for notebook use)."""
    with OneshotPlanner(problem_kind=problem.kind) as planner:
        result = planner.solve(problem, timeout=10)
    if result.plan is not None:
        print("Plan:", repr(result.plan) if verbose else str(result.plan))
    else:
        print(result.status)
    return result


def main() -> None:
    config = {
        "num_levels": 5,
        "elevator_start": 2,
        "capacity": 2,
        "requests": [
            {"start": 0, "goal": 4, "deadline": 16, "base_utility": 100, "late_penalty": 8},
            {"start": 3, "goal": 1, "deadline": 12, "base_utility": 80, "late_penalty": 12},
            {"start": 2, "goal": 2, "deadline": 0, "base_utility": 30, "late_penalty": 5},
        ],
    }
    order = choose_service_order(config)
    print("Service order:", order)
    print("External evaluation:", evaluate_service_order(config, order))
    solve(generate_hierarchical(config))


if __name__ == "__main__":
    main()
