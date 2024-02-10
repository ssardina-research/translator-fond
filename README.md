# FOND All-outcome Determinizers

This repo contains scripts to determinize a PDDL FOND planning domain (with `oneof` clauses) or problem.

## Lifted determinizer

The script [fond2allout.py](fond2allout.py) produces a _lifted_ all-outcome determinization of a FOND PDDL domain. For example:

```shell
$ python fond2allout.py problems/blocksworld-ipc08/domain.pddl --print
```




## SAS problem determinizer

The folder [sas_translate/](sas_translate/) contains an all-outcome determinizer that takes a full FOND planning problem specification (i.e., domain + problem) and yields a SAS all-outcome _determinization_ encoding of the problem. The main script is [sas_translate/translate.py](sas_translate/translate.py).

Example run:

```shell
$ python sas_translate/translate.py problems/blocksworld-ipc08/domain.pddl problems/blocksworld-ipc08/p01.pddl
```

By default, it generates a file `output.sas` with the SAS encoding of the determinization of the original non-deterministic problem. An alternative SAS filename can be given via `--sas-file` option.

Note this translator requires both a domain as well as the specific problem, as it does much more than the determinization per se.

The translator is a extension of the SAS translator that comes with [Fast-Downard](https://github.com/aibasel/downward) for classical planning to read and determinize non-deterministic actions. The current codebase is based on the translator found in [release 22.12](https://github.com/aibasel/downward/tree/release-22.12.0) of Fast-Downard. Note that Fast-Downard's translator has changed significantly since the 2011 version that is used by other non-deterministic planners (e.g., PRP or FOND-SAT).

This translator basically does two things:


1. First, it translates all non-deterministic actions, into a collection of deterministic actions, each corresponding to one deterministic effect of the original non-deterministic action. Each resulting deterministic action has suffix `_DETDUP_<n>`, with `n` being an integer; for example `walk-on-beam_DETDUP_2` is the third deterministic action of non-deterministic action `walk-on-beam`.
2. It then runs the original SAS translator from [FastDownard](https://github.com/aibasel/downward/tree/main/src/translate) system for classical deterministic planning problems.

This determinization SAS encoding has been used by various planners (albeit one based on Fast-Downward translator from 2011), such as FIP, [PRP](https://github.com/ssardina-planning/planner-for-relevant-policies), [FOND-SAT](https://github.com/ssardina-planning/FOND-SAT), and [FOND-ASP](https://github.com/idrave/FOND-ASP). NNote other FOND planners, like [myND](https://github.com/ssardina-planning/myND) and [Paladinus](https://github.com/ramonpereira/paladinus), also use translation of non-deterministic domains to SAS, but with a very different determinization approach that do not create new actions with suffixes (e.g., `_DETUP1`), but they modify existing actions with new arguments.


## Contributors

The codebase is a modification/extension of the translator found in [Fast-Downard](https://github.com/aibasel/downward).

- Nitin Yadav (nitin.yadav@unimelb.edu.au)
- Seastian Sardina (ssardina@gmail.com)

