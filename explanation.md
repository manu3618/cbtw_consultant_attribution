# generalities

This solution is presented in python. We will use the representations suggested
by the provided boilerplate:

* a consultant is represented by a dict:

```python
consultant0 = {
    "id": "0",
    "name": "Andrew Williams",
    "skills": ["python", "java", "rust"],
}
```

* a mission is also represented by a dict:
```python
mission0 = {
    "id": "0",
    "client": "Sanchez-Lopez",
    "skills": ["French", "Dutch", "TDD", "python", "java", "rust"],
    "rate": 276,
}
```

* given the solution format, we will only manipulate mission and consultant ids.
A simple way to retrieve a consultant (resp. a mission) given its mission is to
create a generator. We trust the input data (should be checked in real world)
to have at most one consultant (resp. one mission) for a given id. Thus the following
comprehension list  should contain at most one element:

```python
# consultants is a list (or any iterable) of consultants
consultant_id = "0"
[c for c in consultants if c["id"] == consultant_id]
```

Then to retrieve a consultant (resp. a mission), we only need the first value
of a generator

```python
consultant = next(c for c in consultants if c["id"] == consultant_id)
```

**WARNING**: this code can raise a `StopIteration` if there is no consultant
with the desired id.


# naive solution

Let's simplify the problem

## One attribution allowed

What if we can only attribute one mission to one consultant?
This problem is quite easy: For all possible couple `(consultant, mission)`,
take the one that maximize revenue.

Let's first compute the revenue for a match

```python
def get_money(consultant, mission):
    """Compute the money given the consultant and the mission"""
    skill_nb = len([c for c in consultant["skills"] if c in mission["skills"]])
    return skill_nb / len(mission["skills"]) * mission["rate"]
```

Then, given a list (or any iterable) of consultants and a list (or iterable)
of mission, let's write a function that get the best match:

```python
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
```

__Note__: any solution giving a positive revenue is OK to pass the first step


## Multiple attributions allowed

Let's reduce the problem the the previous one.
What if get the best match, then remove the corresponding consultant and mission
and begin again? We can stop when there is no more consultant or mission available.
Let's code this euristic:

```python
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
```

__Note__: Giving a solution at least a good as this one is enough to pass the
second step.


# Better solution


There are some cases where the naive solution is not the optimal one.
For example, with the following input data:

```
consultants = [
    {
        "id": "0",
        "name": "Andrew Williams",
        "skills": ["python", "java", "rust", "French"],
    },
    {
        "id": "1",
        "name": "Andrew Williams",
        "skills": ["python", "java", "English"],
    },
]
missions = [
    {
        "id": "0",
        "client": "Sanchez-Lopez",
        "skills": ["python", "java", "rust", "French"],
        "rate": 4,
    },
    {
        "id": "1",
        "client": "Sanchez-Lopez",
        "skills": ["French", "rust"],
        "rate": 3,
    },
]
```

The naive solution (`{"0": "0", "1": "1"}`) gives 4 while the other solution
(`{"0": "1", "1": "0"}`) gives 5.

Thus, given a solution, one improvment is to try to swap two randomly choosen
consultants.
I decided to try to do it a fixed number of time (1000 times).


```python
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
```


I think this problem can also be modeled by a mathematical programming. Given
there is no time limit, this solution may be a valid one, and may give better
solution in complicated cases. I didn't took time to try this approach.
