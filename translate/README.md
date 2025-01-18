# SAS-based Determinizer for FOND domains

This repo contains a SAS-based translator for planning tasks that were derived from determinizing a FOND planning task.

The main script is [translate.py](translate.py).

Example run:

```shell
$ python translate.py problems/blocksworld-ipc08/domain.pddl problems/blocksworld-ipc08/p01.pddl
```

By default, it generates a file `output.sas` with the SAS encoding of the determinization of the original non-deterministic problem. An alternative SAS filename can be given via `--sas-file` option.

As with the original translator for deterministic problems, the translator requires _both_ a domain as well as the specific problem instance file.

The only difference with the original translator is that it does not drop operators resulting from all-outcome determnization; see below for more explanation.

> [!IMPORTANT]
> The current codebase is based on the SAS translator found in [**release 24.06**](https://github.com/aibasel/downward/tree/release-22.12.0) (June 2024) of the Downward system. Note that Downward's translator has changed significantly since the 2011 version that is used by other non-deterministic planners (e.g., PRP or FOND-SAT).


> [!WARNING]
> This translator requires a classical _deterministic_ domain. Determinization should have hapened before this translator is used.

## Changes to original SAS translator

The only difference with the original translator is that this version does not simplify operators that are the result of FOND determinization. The original translator will drop an action if it is not useful, for example, if it is a no-op action. However, a no-op action that corresponds to one of the effects of a non-deterministic operator should indeed be taken into account when performing FOND planning.

So, this translator will keep any operator whose name contains the string `DETUP`, which signals that is an action corresponding to one of the many `oneof` effects of the original non-deterministic action.

All the changes were documented with the string `# CHANGE FOND`

## Contributors

The codebase is a modification/extension of the translators found in [Downard](https://github.com/aibasel/downward) library (which ships the SAS translation).

- Sebastian Sardina (ssardina@gmail.com)
- Nitin Yadav (nitin.yadav@unimelb.edu.au)

