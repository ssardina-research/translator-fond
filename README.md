# FOND All-outcome SAS-based Determinizer

This repo contains a SAS-based all-outcome determinizer that takes a full FOND planning problem specification (i.e., domain + problem instance) and yields a SAS all-outcome _determinization_ encoding of the problem. Since it is a FOND PDDL problem, it may mention `oneof` clauses.

The main script is [sas_translate/translate.py](sas_translate/translate.py).

Example run:

```shell
$ python sas_translate/translate.py problems/blocksworld-ipc08/domain.pddl problems/blocksworld-ipc08/p01.pddl
```

By default, it generates a file `output.sas` with the SAS encoding of the determinization of the original non-deterministic problem. An alternative SAS filename can be given via `--sas-file` option.

Note this translator requires both a domain as well as the specific problem, as it does much more than the determinization perse.

The translator is a extension of the SAS translator that comes with [Fast-Downard](https://github.com/aibasel/downward) for classical planning to read and determinize non-deterministic actions. The current codebase is based on the translator found in [release 22.12](https://github.com/aibasel/downward/tree/release-22.12.0) of Fast-Downard. Note that Fast-Downard's translator has changed significantly since the 2011 version that is used by other non-deterministic planners (e.g., PRP or FOND-SAT).

This translator basically does two things:

1. First, it translates all non-deterministic actions, into a collection of deterministic actions, each corresponding to one deterministic effect of the original non-deterministic action. Each resulting deterministic action has suffix `_DETDUP_<n>`, with `n` being an integer; for example `walk-on-beam_DETDUP_2` is the third deterministic action of non-deterministic action `walk-on-beam`.
2. It then runs the original SAS translator from [FastDownard](https://github.com/aibasel/downward/tree/main/src/translate) system for classical deterministic planning problems.

This determinization SAS encoding has been used by various planners (albeit one based on Fast-Downward translator from 2011), such as FIP, [PRP](https://github.com/ssardina-planning/planner-for-relevant-policies), [FOND-SAT](https://github.com/ssardina-planning/FOND-SAT), and [FOND-ASP](https://github.com/idrave/FOND-ASP). NNote other FOND planners, like [myND](https://github.com/ssardina-planning/myND) and [Paladinus](https://github.com/ramonpereira/paladinus), also use translation of non-deterministic domains to SAS, but with a very different determinization approach that do not create new actions with suffixes (e.g., `_DETUP1`), but they modify existing actions with new arguments.

For different formats on how `oneof` clauses may be used, refer to this paper:

* Jussi Rintanen: [Expressive Equivalence of Formalisms for Planning with Sensing](https://gki.informatik.uni-freiburg.de/papers/Rintanen03expr.pdf). ICAPS 2003: 185-194

For a lifted determinization of a FOND domain, please check [fond2allout](https://github.com/ssardina-research/fond2allout) repo.

## Contributors

The codebase is a modification/extension of the translators found in [Fast-Downard](https://github.com/aibasel/downward) and [PRP](https://github.com/QuMuLab/planner-for-relevant-policies).

- Nitin Yadav (nitin.yadav@unimelb.edu.au)
- Seastian Sardina (ssardina@gmail.com)

