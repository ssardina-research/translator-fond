# FOND Translators

This is a Python script that takes a non-deterministic PDDL (with `oneof` clauses) and yields a SAS one-outcome _determinization_ encoding of the problem.

Example run:

```shell
$ python translate.py tests/acrobatics/domain.pddl tests/acrobatics/p1.pddl
```

By default, it generates a file `output.sas` with the SAS encoding of the determinization of the original non-deterministic problem. An alternative SAS filename can be given via `--sas-file` option.

The translator is a extension of the SAS translator that comes with [Fast-Downard](https://github.com/aibasel/downward) for classical planning to read and determinize non-deterministic actions. The current codebase is based on the translator found in [release 22.12](https://github.com/aibasel/downward/tree/release-22.12.0) of Fast-Downard. Note that Fast-Downard's translator has changed significantly since the 2011 version that is used by other non-deterministic planners (e.g., PRP or FOND-SAT).

This translator basically does two things:

1. First, it translates all non-deterministic actions, into a collection of deterministic actions, each corresponding to one deterministic effect of the original non-deterministic action. Each resulting deterministic action has suffix `_DETDUP_<n>`, with `n` being an integer; for example `walk-on-beam_DETDUP_2` is the third deterministic action of non-deterministic action `walk-on-beam`.
2. It then runs the original SAS translator from [FastDownard](https://github.com/aibasel/downward/tree/main/src/translate) system for classical deterministic planning problems.

This determinization SAS encoding has been used by various planners (albeit one based on Fast-Downward translator from 2011), such as FIP, [PRP](https://github.com/ssardina-planning/planner-for-relevant-policies), [FOND-SAT](https://github.com/ssardina-planning/FOND-SAT), and [FOND-ASP](https://github.com/idrave/FOND-ASP). NNote other FOND planners, like [myND](https://github.com/ssardina-planning/myND) and [Paladinus](https://github.com/ramonpereira/paladinus), also use translation of non-deterministic domains to SAS, but with a very different determinization approach that do not create new actions with suffixes (e.g., `_DETUP1`), but they modify existing actions with new arguments.


## Contributors

The codebase is a modification/extension of the translator found in [Fast-Downard](https://github.com/aibasel/downward).

- Nitin Yadav (nitin.yadav@unimelb.edu.au)
- Seastian Sardina (ssardina@gmail.com)

