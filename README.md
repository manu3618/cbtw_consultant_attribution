CBTW challenge


Let's imagine a (almost) hypothetical situation where:

 * lots of consultants are waiting to be attributed to a mission
 * business managers are flooded with mission requests
 * once a business manager decide to attribute a missiion to a consultant, the
   consultant begin its mission immediatly (no client inteview, no time to
   prepare contract, ...)

Given a list of mission and consultants, the goal is to maximize CBTW's revenue.
The consultants are represented by a list of skills.
The missions are repesented by a nominal daily rate and a list of wanted skills.
For each mission, the earned money is the poucentage of wanted skills the consultant possess.

For example, if there is only  1 mission with 5 required skills and
only 1 consultant with 4 of those skills, the client ill pay 80% of the nominal
daily rate.


## I/O description

The program takes a JSON as input (from stdin) and output a JSON (to stdout)

The input looks like:

```JSON


```

The output looks lie

```JSON
```

## solution testing

Whatever the language, the solution should be an executable file put in
`/solution`
See `/build_solution.sh` for more information
