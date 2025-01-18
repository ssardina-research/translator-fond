# FOND All-outcome SAS-based Determinizer

This repo contains a SAS-based all-outcome determinizer that takes a full FOND planning problem specification (i.e., domain + problem instance) and yields a SAS all-outcome _determinization_ encoding of the problem. Since it is a FOND PDDL problem, it may mention `oneof` clauses.

The main script is [translate.py](translate.py).

Example run:

```shell
$ python translate.py problems/blocksworld-ipc08/domain.pddl problems/blocksworld-ipc08/p01.pddl
```

By default, it generates a file `output.sas` with the SAS encoding of the determinization of the original non-deterministic problem. An alternative SAS filename can be given via `--sas-file` option.

Note this translator requires both a domain as well as the specific problem instance file, as it does much more than the determinization perse, it also does static reasoning and simplifications.

The translator-determinizer is in fact a extension of the SAS translator that ships with the [Downward](https://github.com/aibasel/downward) system for classical planning, which converts a classical PDDL into SAS format (so no handling non-deterministic actions), to perform all-outcome determinization. 

> [!IMPORTANT]
> The current codebase is based on the SAS translator found in [**release 22.12**](https://github.com/aibasel/downward/tree/release-22.12.0) (December 2012) of the Downward system. Note that Downward's translator has changed significantly since the 2011 version that is used by other non-deterministic planners (e.g., PRP or FOND-SAT).

## SAS-based determinization

This translator basically does two things:

1. First, it translates all non-deterministic actions, into a collection of deterministic actions, each corresponding to one deterministic effect of the original non-deterministic action. Each resulting deterministic action has suffix `_DETDUP_<n>`, with `n` being an integer; for example `walk-on-beam_DETDUP_2` is the third deterministic action of non-deterministic action `walk-on-beam`.
2. It then runs the original SAS translator from [Downard](https://github.com/aibasel/downward/tree/main/src/translate) system for classical deterministic planning problems.
   - The translation has been slightly modified to avoid dropping any of the derived non-deterministic `_DETDUP_` actions. The original SAS translator may drop actions if they are statically found not to be relevant for the goal. This is OK in classical planning, but not when used for FOND, as those actions do represent effects that may ensue when executing the corresponding non-deterministic effect.

> [!NOTE]
> This SAS-based determinization encoding has been used by various planners (albeit one based on Downward translator from 2011), such as FIP, [PRP](https://github.com/ssardina-planning/planner-for-relevant-policies), [FOND-SAT](https://github.com/ssardina-planning/FOND-SAT), and [FOND-ASP](https://github.com/idrave/FOND-ASP). Note other FOND planners, like [myND](https://github.com/ssardina-planning/myND) and [Paladinus](https://github.com/ramonpereira/paladinus), also use translation of non-deterministic domains to SAS, but with a very different determinization approach that do not create new actions with suffixes (e.g., `_DETUP1`), but they modify existing actions with new arguments.

## Changes to original SAS translator

The original translator that ships with Downward system only performs a SAS encoding of a classical PDDL planning domain and problem. This encoding also includes static optimisations that may result in propositions or actions dropped when found not relevant to achieving the goal (e.g., a no-op action).

The following changes have been implemented to such translator:

- Allow the parsing of `oneof` effects to handle FOND problems (already done in 2011 PRP planner).
- Determinization of non-deterministic actions (those containing `oneof`) to yield corresponding deterministic versions of the action (with suffix `_DETUP_<n>`), one per effect (already done in 2011 PRP planner).
- Fix to avoid dropping any action that corresponds to a non-deterministic effect.

The changes done were documented in issue [#9](https://github.com/ssardina-research/translator-fond/issues/9)

## Oneof effect format

For different formats on how `oneof` clauses may be used, refer to this paper:

* Jussi Rintanen: [Expressive Equivalence of Formalisms for Planning with Sensing](https://gki.informatik.uni-freiburg.de/papers/Rintanen03expr.pdf). ICAPS 2003: 185-194

For a lifted determinization of a FOND domain, please check [fond2allout](https://github.com/ssardina-research/fond2allout) or [fond-utils](https://github.com/AI-Planning/fond-utils) repos.

## Contributors

The codebase is a modification/extension of the translators found in [Downard](https://github.com/aibasel/downward) library (which ships the SAS translation) and [PRP](https://github.com/QuMuLab/planner-for-relevant-policies) planner (which added determinization to the original SAS translation).

- Sebastian Sardina (ssardina@gmail.com)
- Nitin Yadav (nitin.yadav@unimelb.edu.au)

