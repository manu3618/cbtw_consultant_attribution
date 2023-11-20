#!/bin/env python3

import json

if __name__ == "__main__":
    data = json.loads(input())
    solution = {
        "0": "0",
    }
    print(json.dumps(solution, indent=2))
