"""Assignment 1 - Problem 2 hierarchical-planning submission template.

* Group Member 1:
    - Name: Zhang Jiazheng
    - Matric number:A0314707H

* Group Member 2:
    - Name: Phyo Han
    - Matric number:A0196680R

* Group Member 3:
    - Name: Wang Shiyu
    - Matric number:A0354696L

* Group Member 4:
    - Name: Liu Hengyan
    - Matric number:A0350634J

* Group Member 5:
    - Name: Cui Yi
    - Matric number:A0353244J

* Collaborators: None

* Sources: None
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
    if (
        not isinstance(num_levels, int)
        or isinstance(num_levels, bool)
        or num_levels < 1
    ):
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
        if config["requests"][index]["start"] != config["requests"][index]["goal"]
    ]
    capacity = config["capacity"]
    return [
        active[start : start + capacity] for start in range(0, len(active), capacity)
    ]


def evaluate_service_order(
    config: dict[str, Any], order: Sequence[int]
) -> dict[str, Any]:
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

from itertools import permutations
from time import monotonic

# Each policy call runs in its own process and is killed at 10 seconds.
_TIME_BUDGET = 7.0
# States retained per dynamic-programming layer. Ten active passengers need
# roughly 1,200, so this bound only engages on out-of-spec inputs.
_BEAM = 20000


def choose_service_order(config: dict[str, Any]) -> list[int]:
    """Return a permutation of passenger indices maximizing total utility.

    Enumerating permutations is factorial, but under the fixed batching protocol
    the utility still obtainable depends only on which passengers have already
    been served, the floor the lift finished on, and the clock. That collapses
    the search into a dynamic program over served-passenger subsets, keeping for
    each (subset, exit floor) the Pareto frontier of (clock, utility) pairs.
    """
    validate_config(config)
    budget = monotonic() + _TIME_BUDGET
    requests = config["requests"]
    total = len(requests)
    active = [i for i in range(total) if requests[i]["start"] != requests[i]["goal"]]
    reached = [i for i in range(total) if requests[i]["start"] == requests[i]["goal"]]
    # Passengers already at their goal complete at t = 0 and therefore always
    # earn full base utility, so their position in the permutation is irrelevant
    # to the score. Optimize over the rest and append them afterwards.
    if not active:
        return list(range(total))
    return _best_active_order(config, active, budget) + reached


def _best_active_order(
    config: dict[str, Any], active: list[int], budget: float
) -> list[int]:
    """Order the passengers that actually need service, by subset DP."""
    capacity = config["capacity"]
    count = len(active)
    start = [config["requests"][i]["start"] for i in active]
    goal = [config["requests"][i]["goal"] for i in active]
    terms = [
        (
            config["requests"][i]["base_utility"],
            config["requests"][i]["late_penalty"],
            config["requests"][i]["deadline"],
        )
        for i in active
    ]
    batch_cache: dict[tuple[int, tuple[int, ...]], Any] = {}

    def effect(floor: int, batch: tuple[int, ...]):
        """Time cost, per-passenger completion offsets, and exit floor."""
        hit = batch_cache.get((floor, batch))
        if hit is None:
            here, elapsed = floor, 0
            for member in batch:  # pick every passenger up, in order
                elapsed += abs(here - start[member]) + 3  # move, open, load, close
                here = start[member]
            offsets = []
            for member in batch:  # then drop them all off, same order
                elapsed += abs(here - goal[member]) + 2  # move, open, unload
                offsets.append(elapsed)  # completion is measured here
                elapsed += 1  # close
                here = goal[member]
            hit = (elapsed, offsets, here)
            batch_cache[(floor, batch)] = hit
        return hit

    def gained(batch: tuple[int, ...], offsets: list[int], clock: int) -> int:
        """Utility this batch earns when it starts at time ``clock``."""
        earned = 0
        for position, member in enumerate(batch):
            base, penalty, due = terms[member]
            late = clock + offsets[position] - due
            earned += base if late <= 0 else max(0, base - penalty * late)
        return earned

    def rank(item) -> int:
        """Admissible bound: utility banked plus every unserved base utility."""
        (mask, _floor), frontier = item
        spare = sum(terms[m][0] for m in range(count) if not (mask >> m) & 1)
        return max(utility for utility, _back in frontier.values()) + spare

    layers = [{(0, config["elevator_start"]): {0: (0, None)}}]
    served = 0
    while served < count:
        size = min(capacity, count - served)
        current = layers[-1]
        if len(current) > 1:
            # Expand best-first so an early bail keeps the promising states; once
            # the budget is spent a beam of one finishes the order greedily.
            beam = _BEAM if monotonic() < budget else 1
            current = sorted(current.items(), key=rank, reverse=True)[:beam]
        else:
            current = list(current.items())

        successors: dict[tuple[int, int], dict[int, tuple[int, Any]]] = {}
        for key, frontier in current:
            if successors and monotonic() > budget:
                break
            mask, floor = key
            remaining = [m for m in range(count) if not (mask >> m) & 1]
            for batch in permutations(remaining, size):
                elapsed, offsets, exit_floor = effect(floor, batch)
                new_mask = mask
                for member in batch:
                    new_mask |= 1 << member
                slot = successors.setdefault((new_mask, exit_floor), {})
                for clock, (utility, _back) in frontier.items():
                    banked = utility + gained(batch, offsets, clock)
                    arrival = clock + elapsed
                    seen = slot.get(arrival)
                    if seen is None or seen[0] < banked:
                        slot[arrival] = (banked, (key, clock, batch))

        # Prune dominated points: a later arrival survives only if it banked
        # strictly more utility, because every future completion time shifts by
        # the same amount and so future utility never rises with the clock.
        layer = {}
        for key, slot in successors.items():
            kept, best = {}, None
            for clock in sorted(slot):
                utility, back = slot[clock]
                if best is None or utility > best:
                    best = utility
                    kept[clock] = (utility, back)
            layer[key] = kept
        layers.append(layer)
        served += size

    best_utility, best_key, best_clock = -1, None, None
    for key, frontier in layers[-1].items():
        for clock, (utility, _back) in frontier.items():
            if utility > best_utility:
                best_utility, best_key, best_clock = utility, key, clock

    batches = []
    key, clock = best_key, best_clock
    for index in range(len(layers) - 1, 0, -1):
        _utility, back = layers[index][key][clock]
        key, clock, batch = back
        batches.append(batch)
    batches.reverse()
    return [active[member] for batch in batches for member in batch]


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

    # 1. move_elevator
    # elevator at `start`
    move_elevator.add_precondition(
        Equals(at_elevator(move_elevator.elevator), move_elevator.start)
    )
    # door closed
    move_elevator.add_precondition(Not(elevator_door_open(move_elevator.elevator)))
    # elevator at `end`
    move_elevator.add_effect(at_elevator(move_elevator.elevator), move_elevator.end)

    # 2. load
    # elevator and person at `floor`;
    load.add_precondition(Equals(at_elevator(load.elevator), load.floor))
    load.add_precondition(Equals(at_person(load.person), load.floor))
    # door open;
    load.add_precondition(elevator_door_open(load.elevator))
    # `lift_count(current)`;
    load.add_precondition(lift_count(load.current))
    # `next_count(current,next)`;
    load.add_precondition(next_count(load.current, load.next))
    # person not reached
    load.add_precondition(Not(reached(load.person)))

    # person at elevator;
    load.add_effect(at_person(load.person), load.elevator)
    # current count false;
    load.add_effect(lift_count(load.current), False)
    # next count true
    load.add_effect(lift_count(load.next), True)

    # 3. unload
    # elevator at `floor`;
    unload.add_precondition(Equals(at_elevator(unload.elevator), unload.floor))
    # person at elevator;
    unload.add_precondition(Equals(at_person(unload.person), unload.elevator))
    # door open;
    unload.add_precondition(elevator_door_open(unload.elevator))
    # person's destination is `floor`;
    unload.add_precondition(Equals(destination(unload.person), unload.floor))
    # `lift_count(current)`;
    unload.add_precondition(lift_count(unload.current))
    # `next_count(previous,current)`
    unload.add_precondition(next_count(unload.previous, unload.current))
    # person at floor;
    unload.add_effect(at_person(unload.person), unload.floor)
    # reached true;
    unload.add_effect(reached(unload.person), True)
    # current count false;
    unload.add_effect(lift_count(unload.current), False)
    # previous count true
    unload.add_effect(lift_count(unload.previous), True)

    # 4. open_door
    # door closed
    open_door.add_precondition(Not(elevator_door_open(open_door.elevator)))
    # door open
    open_door.add_effect(elevator_door_open(open_door.elevator), True)

    # 5. close_door
    close_door.add_precondition(elevator_door_open(close_door.elevator))
    close_door.add_effect(elevator_door_open(close_door.elevator), False)

    # COPY-FLAG-2-END

    problem.add_actions([move_elevator, load, unload, open_door, close_door])

    pickup_person = problem.add_task("pickup_person", person=Person, start_floor=Floor)
    deliver_person = problem.add_task("deliver_person", person=Person, goal_floor=Floor)
    confirm_reached = problem.add_task(
        "confirm_reached", person=Person, goal_floor=Floor
    )

    # COPY-FLAG-3-START

    # Add the five methods using the exact signatures, preconditions, and
    # ordered decompositions listed in Task 3.

    # --- pickup_person, lift on a DIFFERENT floor: move / open / load / close
    pickup_other = Method(
        "method_pickup_from_other_floor",
        elevator=Elevator,
        person=Person,
        elevator_floor=Floor,
        start_floor=Floor,
        current=Count,
        next=Count,
    )
    pickup_other.set_task(pickup_person, pickup_other.person, pickup_other.start_floor)
    pickup_other.add_precondition(
        Equals(at_person(pickup_other.person), pickup_other.start_floor)
    )
    pickup_other.add_precondition(
        Equals(at_elevator(pickup_other.elevator), pickup_other.elevator_floor)
    )
    pickup_other.add_precondition(Not(elevator_door_open(pickup_other.elevator)))
    pickup_other.add_precondition(next_count(pickup_other.current, pickup_other.next))
    pickup_other.add_precondition(Not(reached(pickup_other.person)))
    pickup_other.add_precondition(
        Not(Equals(pickup_other.elevator_floor, pickup_other.start_floor))
    )
    pickup_other_move = pickup_other.add_subtask(
        move_elevator,
        pickup_other.elevator,
        pickup_other.elevator_floor,
        pickup_other.start_floor,
    )
    pickup_other_open = pickup_other.add_subtask(open_door, pickup_other.elevator)
    pickup_other_load = pickup_other.add_subtask(
        load,
        pickup_other.elevator,
        pickup_other.person,
        pickup_other.start_floor,
        pickup_other.current,
        pickup_other.next,
    )
    pickup_other_close = pickup_other.add_subtask(close_door, pickup_other.elevator)
    pickup_other.set_ordered(
        pickup_other_move, pickup_other_open, pickup_other_load, pickup_other_close
    )
    problem.add_method(pickup_other)

    # --- pickup_person, lift already there: open / load / close
    pickup_here = Method(
        "method_pickup_from_current_floor",
        elevator=Elevator,
        person=Person,
        start_floor=Floor,
        current=Count,
        next=Count,
    )
    pickup_here.set_task(pickup_person, pickup_here.person, pickup_here.start_floor)
    pickup_here.add_precondition(
        Equals(at_person(pickup_here.person), pickup_here.start_floor)
    )
    pickup_here.add_precondition(
        Equals(at_elevator(pickup_here.elevator), pickup_here.start_floor)
    )
    pickup_here.add_precondition(Not(elevator_door_open(pickup_here.elevator)))
    pickup_here.add_precondition(next_count(pickup_here.current, pickup_here.next))
    pickup_here.add_precondition(Not(reached(pickup_here.person)))
    pickup_here_open = pickup_here.add_subtask(open_door, pickup_here.elevator)
    pickup_here_load = pickup_here.add_subtask(
        load,
        pickup_here.elevator,
        pickup_here.person,
        pickup_here.start_floor,
        pickup_here.current,
        pickup_here.next,
    )
    pickup_here_close = pickup_here.add_subtask(close_door, pickup_here.elevator)
    pickup_here.set_ordered(pickup_here_open, pickup_here_load, pickup_here_close)
    problem.add_method(pickup_here)

    # --- deliver_person, goal on a DIFFERENT floor: move / open / unload / close
    deliver_other = Method(
        "method_deliver_to_other_floor",
        elevator=Elevator,
        person=Person,
        elevator_floor=Floor,
        goal_floor=Floor,
        previous=Count,
        current=Count,
    )
    deliver_other.set_task(
        deliver_person, deliver_other.person, deliver_other.goal_floor
    )
    deliver_other.add_precondition(
        Equals(at_person(deliver_other.person), deliver_other.elevator)
    )
    deliver_other.add_precondition(
        Equals(destination(deliver_other.person), deliver_other.goal_floor)
    )
    deliver_other.add_precondition(
        Equals(at_elevator(deliver_other.elevator), deliver_other.elevator_floor)
    )
    deliver_other.add_precondition(Not(elevator_door_open(deliver_other.elevator)))
    deliver_other.add_precondition(
        next_count(deliver_other.previous, deliver_other.current)
    )
    deliver_other.add_precondition(
        Not(Equals(deliver_other.elevator_floor, deliver_other.goal_floor))
    )
    deliver_other_move = deliver_other.add_subtask(
        move_elevator,
        deliver_other.elevator,
        deliver_other.elevator_floor,
        deliver_other.goal_floor,
    )
    deliver_other_open = deliver_other.add_subtask(open_door, deliver_other.elevator)
    deliver_other_unload = deliver_other.add_subtask(
        unload,
        deliver_other.elevator,
        deliver_other.person,
        deliver_other.goal_floor,
        deliver_other.previous,
        deliver_other.current,
    )
    deliver_other_close = deliver_other.add_subtask(close_door, deliver_other.elevator)
    deliver_other.set_ordered(
        deliver_other_move,
        deliver_other_open,
        deliver_other_unload,
        deliver_other_close,
    )
    problem.add_method(deliver_other)

    # --- deliver_person, lift already at the goal: open / unload / close
    deliver_here = Method(
        "method_deliver_at_current_floor",
        elevator=Elevator,
        person=Person,
        goal_floor=Floor,
        previous=Count,
        current=Count,
    )
    deliver_here.set_task(deliver_person, deliver_here.person, deliver_here.goal_floor)
    deliver_here.add_precondition(
        Equals(at_person(deliver_here.person), deliver_here.elevator)
    )
    deliver_here.add_precondition(
        Equals(destination(deliver_here.person), deliver_here.goal_floor)
    )
    deliver_here.add_precondition(
        Equals(at_elevator(deliver_here.elevator), deliver_here.goal_floor)
    )
    deliver_here.add_precondition(Not(elevator_door_open(deliver_here.elevator)))
    deliver_here.add_precondition(
        next_count(deliver_here.previous, deliver_here.current)
    )
    deliver_here_open = deliver_here.add_subtask(open_door, deliver_here.elevator)
    deliver_here_unload = deliver_here.add_subtask(
        unload,
        deliver_here.elevator,
        deliver_here.person,
        deliver_here.goal_floor,
        deliver_here.previous,
        deliver_here.current,
    )
    deliver_here_close = deliver_here.add_subtask(close_door, deliver_here.elevator)
    deliver_here.set_ordered(
        deliver_here_open, deliver_here_unload, deliver_here_close
    )
    problem.add_method(deliver_here)

    # --- confirm_reached: empty decomposition
    confirm = Method("method_confirm_reached", person=Person, goal_floor=Floor)
    confirm.set_task(confirm_reached, confirm.person, confirm.goal_floor)
    confirm.add_precondition(reached(confirm.person))
    confirm.add_precondition(Equals(at_person(confirm.person), confirm.goal_floor))
    confirm.add_precondition(Equals(destination(confirm.person), confirm.goal_floor))
    problem.add_method(confirm)

    # COPY-FLAG-3-END

    # COPY-FLAG-4-START

    # Filter initially reached passengers, split the remaining order into
    # capacity-sized batches, add all pickups followed by all deliveries for
    # each batch, append confirm_reached tasks, and totally order the network.

    requests = config["requests"]
    network = problem.task_network
    subtasks = []

    # Per batch: every pickup in order, then every delivery in the same order.
    for batch in service_batches(config, order):
        for index in batch:
            subtasks.append(
                network.add_subtask(
                    pickup_person, people[index], floors[requests[index]["start"]]
                )
            )
        for index in batch:
            subtasks.append(
                network.add_subtask(
                    deliver_person, people[index], floors[requests[index]["goal"]]
                )
            )

    # Initially reached passengers, in their relative policy order.
    for index in order:
        request = requests[index]
        if request["start"] == request["goal"]:
            subtasks.append(
                network.add_subtask(
                    confirm_reached, people[index], floors[request["goal"]]
                )
            )

    if len(subtasks) > 1:
        network.set_ordered(*subtasks)

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
            {
                "start": 0,
                "goal": 4,
                "deadline": 16,
                "base_utility": 100,
                "late_penalty": 8,
            },
            {
                "start": 3,
                "goal": 1,
                "deadline": 12,
                "base_utility": 80,
                "late_penalty": 12,
            },
            {
                "start": 2,
                "goal": 2,
                "deadline": 0,
                "base_utility": 30,
                "late_penalty": 5,
            },
        ],
    }
    order = choose_service_order(config)
    print("Service order:", order)
    print("External evaluation:", evaluate_service_order(config, order))
    solve(generate_hierarchical(config))


if __name__ == "__main__":
    main()
