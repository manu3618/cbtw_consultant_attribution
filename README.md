# CBTW coding challenge 2: Consultant - mission matching


Let's imagine a (almost) hypothetical situation where:

 * lots of consultants are waiting to be attributed to a mission
 * business managers are flooded with mission requests
 * once a business manager decide to attribute a mission to a consultant, the
   consultant begin its mission immediatly (no client inteview, no time to
   prepare contract, ...)

Given a list of mission and consultants, the goal is to maximize CBTW's revenue.
The consultants are represented by a list of skills.
The missions are repesented by a nominal daily rate and a list of wanted skills.
For each mission, the earned money is the pourcentage of wanted skills
the consultant possess multiply by the nominal daily rate.

For example, if there is only 1 mission with 5 required skills and
only 1 consultant with 4 of those skills, the client will pay 80% of the nominal
daily rate.


## I/O description

The program takes a JSON as input (from stdin) and output a JSON (to stdout)

### input

The input looks like:

```JSON
{
    "consultants": [
        {
            "id": "0",
            "name": "Andrew Williams",
            "skills": [
                "python",
                "java",
                "rust"
            ]
        },
        {
            "id": "1",
            "name": "Robert Graham DVM",
            "skills": [
                "Git"
            ]
        },
        {
            "id": "2",
            "name": "Jason Russell",
            "skills": [
                "java",
                "rust",
                "Git"
            ]
        }
    ],
    "missions": [
        {
            "id": "0",
            "client": "Sanchez-Lopez",
            "skills": [
                "French",
                "TDD",
                "python",
            ],
            "rate": 276
        },
        {
            "id": "1",
            "client": "Spencer and Sons",
            "skills": [
                "Dutch",
                "SQL",
                "rust"
            ],
            "rate": 552
        },
    ]
}
```

### output

The output contains a mapping `{consultant_id: mission_id}`

```JSON
{
  "0": "0",
  "2": "4"
}
```

## solution testing

Boiler plate is provided for python.
Complete the file `python/cbtw.py`.
If you use another language, contact me
and I'll add the corresponding boiler plate.
Github actions run tests for you when you push your code.
See the github actions to know how your code performed.

Several steps have to be achieved:

* step 1: have a valid solution, i.e. make money.
* step 2: make as much money as possible.
