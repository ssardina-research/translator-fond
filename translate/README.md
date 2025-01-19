# SAS-based Determinizer for FOND domains

This repo contains a minor variant of the original SAS-based translator shipped with [downard](https://github.com/aibasel/downward/) for planning domains that are determinizations of FOND planning task.

> [!IMPORTANT]
> **Current SAS translator version:** commit [`113fe1a`](https://github.com/aibasel/downward/tree/113fe1a626176f0c34888c645d4c25e7c31db372) for release 24.06 - June 2024.

The main script is [translate.py](translate.py), which requires both domain and problem instance:

```shell
$ python translate.py problems/blocksworld-ipc08/domain.pddl problems/blocksworld-ipc08/p01.pddl
```

By default, it generates a file `output.sas` with the SAS encoding of the determinization of the original non-deterministic problem. An alternative SAS filename can be given via `--sas-file` option.

The only difference with the original translator is that it does not drop operators resulting from all-outcome determnization; see below for more explanation.

> [!WARNING]
> This translator does not accept FOND planning domains, it has to be deterministic planning problems (but these would typically be determinizations of original FOND domains!).

## Changes to original SAS translator

The only difference with the original translator is that this version **does not simplify operators that are the result of FOND determinization**. The original translator will drop an action if it is not useful ot the goal in the problem instance, for example, if it is a no-op action. However, a no-op action that corresponds to one of the effects of a non-deterministic operator should indeed be taken into account when performing FOND planning.

So, this translator will keep any operator whose name contains the string `DETUP`, which signals that is an action corresponding to one of the many `oneof` effects of the original non-deterministic action.

All the changes were documented with the string `# CHANGE FOND` and affect the following giles:

```shell
$ diff -qr translate translate-fond -x '__pycache__'
Files translate/pddl/actions.py and translate-fond/pddl/actions.py differ
Files translate/pddl_parser/parsing_functions.py and translate-fond/pddl_parser/parsing_functions.py differ
Files translate/simplify.py and translate-fond/simplify.py differ
Files translate/translate.py and translate-fond/translate.py differ
Files translate/variable_order.py and translate-fond/variable_order.py differ
```

## Update workflow

From time to time, the SAS translator is updated and improved and we may want to bring those changes to the FOND version. To do so:

1. Get the new `src/translate` folder from [downward](https://github.com/aibasel/downward/). Maybe save the release under [../../](../original-translators/). 
2. The new downward release may or may not have updated the translator wrt the current version. If no changes were done on the translator, nothing else needs to be done, the current translator here is up to date. To check, you can use `meld` or `diff`:

    ```shell
    $ meld ../original-translators/downward-release-24.06.0/src/translate translate/
    ```

3. Otherwise, using `diff` and `mend` and the documented changes above, build an updated translator under `translate/` folder here. Dependign how much the translator changed, this may require manual work. 😲
4. Produce the patch file that can be used to patch the original translator:

    ```shell
    $ diff -crB -x "__pycache__" translate translate-fond > translate-fond-3c8a65b.patch
    ```

5. Push the changes to the remote.

## Contributors

The codebase is a modification/extension of the translators found in [Downard](https://github.com/aibasel/downward) library (which ships the SAS translation).

- Sebastian Sardina (ssardina@gmail.com)
- Nitin Yadav (nitin.yadav@unimelb.edu.au)

