#!/bin/env python3

import json
import sys
from itertools import product
from random import choices


def get_naive_matches(consultants, missions):
    """Naive solution."""
    matches = {}
    consultants = consultants.copy()
    missions = missions.copy()
    while consultants and missions:
        consultant, mission = get_max_match(consultants, missions)
        matches[consultant["id"]] = mission["id"]
        consultants.remove(consultant)
        missions.remove(mission)

    return matches


def get_max_match(consultants, missions):
    """return best mission attribution if only one attribution can be made"""
    value = 0
    consultant = consultants[0]
    mission = missions[0]
    for c, m in product(consultants, missions):
        if get_money(c, m) > value:
            consultant = c
            mission = m
            value = get_money(c, m)
    return consultant, mission


def get_money(consultant, mission):
    """Compute the money given the consultant and the mission"""
    skill_nb = len([c for c in consultant["skills"] if c in mission["skills"]])
    return skill_nb / len(mission["skills"]) * mission["rate"]


def compute_money(data, attributions):
    consultants = data["consultants"]
    missions = data["missions"]
    money = 0
    for consultant_id, mission_id in attributions.items():
        consultant = next(c for c in consultants if c["id"] == consultant_id)
        mission = next(m for m in missions if m["id"] == mission_id)
        money += get_money(consultant, mission)
    return money


def get_match(data):
    consultants, missions = data["consultants"], data["missions"]
    solution = get_naive_matches(consultants, missions)
    money = compute_money(data, solution)
    for _ in range(1000):
        swaps = choices(list(solution.keys()), k=2)
        prop = solution.copy()
        prop[swaps[0]], prop[swaps[1]] = solution[swaps[1]], solution[swaps[0]]
        prop_money = compute_money(data, prop)
        if prop_money > money:
            print(f"better solution, earn {prop_money}", file=sys.stderr)
            solution = prop.copy()
            money = prop_money
    return solution


if __name__ == "__main__":
    data = json.loads(input())
    solution = get_match(data)
    print(json.dumps(solution, indent=2))
