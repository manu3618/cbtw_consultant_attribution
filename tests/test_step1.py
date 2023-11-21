import json
from pathlib import Path
from subprocess import PIPE, Popen

import pytest


@pytest.mark.parametrize("input_file", Path("tests/inputs/").glob("*json"))
def test_solution(input_file):
    with open(input_file) as fd:
        content = fd.read()
    input_data = json.loads(content)
    output = generate_result(content.encode())
    assert compute_money(input_data, output) > 0, (
        f"No money made with input\n{content}" f"\nand output\n{output}"
    )


def generate_result(input_data, executable=Path("python/cbtw.py")):
    p = Popen([executable], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    output_json = p.communicate(input=input_data)[0]
    return json.loads(output_json)


def compute_money(data, attributions):
    consultants = data["consultants"]
    missions = data["missions"]
    money = 0
    for consultant_id, mission_id in attributions.items():
        consultant = next(c for c in consultants if c["id"] == consultant_id)
        mission = next(m for m in missions if m["id"] == mission_id)
        competence_nb = len(
            [c for c in consultant["skills"] if c in mission["skills"]]
        )
        money += competence_nb / len(mission["skills"]) * mission["rate"]
    return money
