import json
from itertools import product
from pathlib import Path
from random import choices, randint
from subprocess import PIPE, Popen

import pytest
from faker import Faker

COMPETENCES = [
    "python",
    "java",
    "rust",
    "DevOps",
    "Agile",
    "SQL",
    "English",
    "French",
    "Dutch",
    "Git",
    "TDD",
    "Jira",
    "Confluence",
    "Machine Learning",
]
NAME_GENERATOR = Faker()


def consultant_generator(consultant_nb=10):
    for n in range(consultant_nb):
        yield {
            "id": str(n),
            "name": NAME_GENERATOR.name(),
            "competences": list(set(choices(COMPETENCES, k=randint(1, 10)))),
        }


def mission_generator(mission_nb=10):
    for n in range(mission_nb):
        yield {
            "id": str(n),
            "client": NAME_GENERATOR.company(),
            "competences": list(set(choices(COMPETENCES, k=randint(1, 10)))),
            "rate": 12 * randint(10, 80),
        }


def input_data_generator(consultant_nb=10, mission_nb=10):
    return {
        "consultants": list(consultant_generator(consultant_nb)),
        "missions": list(mission_generator(mission_nb)),
    }


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
    competence_nb = len(
        [c for c in consultant["competences"] if c in mission["competences"]]
    )
    return competence_nb / len(mission["competences"]) * mission["rate"]


def compute_money(data, attributions):
    consultants = data["consultants"]
    missions = data["missions"]
    money = 0
    for consultant_id, mission_id in attributions.items():
        consultant = next(c for c in consultants if c["id"] == consultant_id)
        mission = next(m for m in missions if m["id"] == mission_id)
        money += get_money(consultant, mission)
    return money


def generate_result(input_data, executable=Path("python/cbtw.py")):
    p = Popen([executable], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    output_json = p.communicate(input=input_data)[0]
    return json.loads(output_json)


@pytest.mark.parametrize("input_file", Path("tests/inputs/").glob("*json"))
def test_deterministic_solution(input_file):
    with open(input_file) as fd:
        content = fd.read()
    input_data = json.loads(content)
    output = generate_result(content.encode())
    solution_money = compute_money(input_data, output)
    naive_solution = get_naive_matches(
        input_data["consultants"], input_data["missions"]
    )
    naive_money = compute_money(input_data, naive_solution)
    msg = (
        f"With input \n{content}\nyou could have made {naive_money}"
        f" with\n{naive_solution}"
    )
    assert solution_money >= naive_money, msg
    assert len(output.values()) == len(
        set(output.values())
    ), "cannot put a consultant in multiple missions"


@pytest.mark.parametrize("execution_number", range(10))
def test_random_inputs(execution_number):
    input_data = input_data_generator(randint(1, 50), randint(1, 50))
    content = json.dumps(input_data)
    output = generate_result(content.encode())
    solution_money = compute_money(input_data, output)
    naive_solution = get_naive_matches(
        input_data["consultants"], input_data["missions"]
    )
    naive_money = compute_money(input_data, naive_solution)
    msg = (
        f"With input \n{content}\nyou could have made {naive_money}"
        f" with\n{naive_solution}"
    )
    assert solution_money >= naive_money, msg
    assert len(output.values()) == len(
        set(output.values())
    ), "cannot put a consultant in multiple missions"
