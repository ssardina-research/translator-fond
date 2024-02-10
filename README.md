# FOND All-outcome Determinizers

This repo contains scripts to determinize a PDDL FOND planning domain (with `oneof` clauses) or problem. In the all-outcome determinization, each non-deterministic action is replaced with a set of deterministic actions, each encoding one possible effect outcome of the action. A solution in the deterministic version amounts to a weak plan solution in the original FOND problem.

There are currently two scripts, one producing a SAS encoding and one a lifted PDDL encoding of the determinized version.

## SAS problem determinizer

The folder [sas_translate/](sas_translate/) contains an all-outcome determinizer that takes a full FOND planning problem specification (i.e., domain + problem) and yields a SAS all-outcome _determinization_ encoding of the problem. The main script is [sas_translate/translate.py](sas_translate/translate.py).

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


## Lifted determinizer

The script [fond2allout.py](fond2allout.py) produces a _lifted_ all-outcome determinization of a FOND PDDL domain. The script relies on the [pddl](https://github.com/AI-Planning/pddl) parser, which can be installed via `pip install pddl`.

A simple example run is as follows:

```shell
$ python fond2allout.py problems/blocksworld-ipc08/domain.pddl
```

This will save the all-outcome deterministic PDDL version in file `domain-allout.pddl`. Deterministic versions of non-deterministic actions will be indexed with term `_DETDUP_<n>` as done by PRP's  original determinizer. The name of the determinize domain will be the original name with suffix `_ALLOUT`.

To change the suffix use option `--suffix`, to change the output file use `--save`, and to get the resulting PDDL printed on console use `--print`:

```lisp
$ python fond2allout.py problems/blocksworld-ipc08/domain.pddl --print --suffix "VER" --save output.pddl                                                                    ─╯
(define (domain blocks-domain_ALLOUT)
    (:requirements :equality :typing)
    (:types block)
    (:predicates (clear ?b - block)  (emptyhand) (holding ?b - block)  (on ?b1 - block ?b2 - block)  (on-table ?b - block))
    (:action pick-tower
        :parameters (?b1 - block ?b2 - block ?b3 - block)
        :precondition (and (emptyhand) (on ?b1 ?b2) (on ?b2 ?b3))
        :effect (and (holding ?b2) (clear ?b3) (not (emptyhand)) (not (on ?b2 ?b3)))
    )
     (:action pick-up-from-table
        :parameters (?b - block)
        :precondition (and (emptyhand) (clear ?b) (on-table ?b))
        :effect (and (holding ?b) (not (emptyhand)) (not (on-table ?b)))
    )
     (:action pick-up_VER_0
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (holding ?b1) (clear ?b2) (not (emptyhand)) (not (clear ?b1)) (not (on ?b1 ?b2)))
    )
     (:action pick-up_VER_1
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2)))
    )
     (:action put-down
        :parameters (?b - block)
        :precondition (holding ?b)
        :effect (and (on-table ?b) (emptyhand) (clear ?b) (not (holding ?b)))
    )
...
```

Note this resulting PDDL domain is now deterministic and can then be used as input to the original [Fast-Downard](https://github.com/aibasel/downward) SAS translator.

### Format allowed on effects

The determinizer accepts effects that are a single top-level `oneof` clause or mentioned as clauses in the top-level `And` effect. As such, `oneof` should not be mentioned inside other `oneof` clauses or internal `and` clauses.

If the effect is just one `oneof` clause, then it corresponds to the Unary Nondeterminism (1ND) Normal Form without conditionals in:

* Jussi Rintanen: [Expressive Equivalence of Formalisms for Planning with Sensing](https://gki.informatik.uni-freiburg.de/papers/Rintanen03expr.pdf). ICAPS 2003: 185-194

However, the translator is able to handle more flexible formats, like:

- Single predicate effect, like `:effect (door_unlocked ?r)`
- Single oneof effect, like `:effect (oneof (and (on-table ?b) (emptyhand)) (and (on ?b ?c) (emptyhand)))`
- And-effect with many `oneof` clauses, like
    `:effect (and (f1) (f2) (oneof ......) (f3) (oneof .....) (f4) (oneof ....))`

When there are many `oneof` clauses in a top-level `and` effect, the cross-product of all the `oneof` clauses will determine the deterministic actions.






## Contributors

The codebase is a modification/extension of the translators found in [Fast-Downard](https://github.com/aibasel/downward) and [PRP](https://github.com/QuMuLab/planner-for-relevant-policies).

- Nitin Yadav (nitin.yadav@unimelb.edu.au)
- Seastian Sardina (ssardina@gmail.com)

