# Test cases

We explain here some interesting test cases, comparing the original FD translator with the two modifications in this repo.

## Test 01: static predicate and `--keep-unimportant-variables`

Predicate `r` is irrelevant but:

- in `p1` it is fully static and so it will _always_ be removed.
- in `p2` it is in the initial state, so it will be unimportant. If the keep option is sated it will be kept.

```shell
$ python original-translators/downward-release-24.06.0/src/translate/translate.py tests/01/domain.pddl tests/01/p02.pddl --keep-unimportant-variables ; cat output.sas

begin_version
3
end_version
begin_metric
0
end_metric
2
begin_variable
var0
-1
2
Atom r()                    <------------- KEPT!!
NegatedAtom r()
end_variable
begin_variable
var1
-1
2
Atom q()
NegatedAtom q()
end_variable
0
begin_state
0
1
end_state
begin_goal
1
1 0
end_goal
2
begin_operator
set_q
0
1
0 1 -1 0
1
end_operator
begin_operator
unset_r
0
1
0 0 -1 1
1
end_operator
0
```

## Test 02: no-op non-determinism

Determinize the domain first:

```shell
$ fond-utils determinize --input tests/02/domain_fond.pddl --suffix-domain "" --output tests/02/domain_all_outcomes.pddl
```

Next translate with FD translator:

```shell
$ python original-translators/downward-release-24.06.0/src/translate/translate.py --keep-unimportant-variables tests/02/domain_all_outcomes.pddl tests/02/p1.pddl ; cat output.sas

begin_version
3
end_version
begin_metric
0
end_metric
1
begin_variable
var0
-1
2
Atom q()
NegatedAtom q()
end_variable
0
begin_state
1
end_state
begin_goal
1
0 0
end_goal
1
begin_operator
ndset_q_detdup_1
0
1
0 0 -1 0
1
end_operator
0
```

See `r` is gone because it is unimportant, and so action `unset_r` is gone too (because it only affects `r`). Also, action `ndset_q_detdup_2` because it is a no-op (no effects!).

Let's use `--keep-unimportant-variables`:

```shell
$ python original-translators/downward-release-24.06.0/src/translate/translate.py --keep-unimportant-variables tests/02/domain_all_outcomes.pddl tests/02/p1.pddl ; cat output.sas

begin_version
3
end_version
begin_metric
0
end_metric
2
begin_variable
var0
-1
2
Atom r()
NegatedAtom r()
end_variable
begin_variable
var1
-1
2
Atom q()
NegatedAtom q()
end_variable
0
begin_state
0
1
end_state
begin_goal
1
1 0
end_goal
2
begin_operator
ndset_q_detdup_1
0
1
0 1 -1 0
1
end_operator
begin_operator
unset_r
0
1
0 0 -1 1
1
end_operator
0
```

Now `r` is kept and so is action `unset_r`.

However, operator `ndset_q_detdup_2` is still gone, because it was originally a no-op.

Now let's use the modified `translate` script for FOND:

```shell
$ python ./translate/translate/translate.py tests/02/domain_all_outcomes.pddl tests/02/p1.pddl ; cat output.sas

begin_version
3
end_version
begin_metric
0
end_metric
1
begin_variable
var0
-1
2
Atom q()
NegatedAtom q()
end_variable
0
begin_state
1
end_state
begin_goal
1
0 0
end_goal
2
begin_operator
ndset_q_detdup_1
0
1
0 0 -1 0
1
end_operator
begin_operator
ndset_q_detdup_2
0
0
1
end_operator
0
```

So, `r` and its associated action `unset_r` are simplified, BUT operator `ndset_q_detdup_2` is kept because it comes from determinization. So we get the benefits of simplification from FD translator, while keeping all non-deterministic effect-related actions.

## Test 03

Same as Test 02 but the ND action `ndset_q` has a third nd effect to make `r` true.

So, when we run the FD translator with option `--keep-unimportant-variables`, both `r` and the nd operator `ndset_q_detdup_3` that sets it to true are kept, but as before `ndset_q_detdup_2` is dropped because it is already a no-op action from the start.

```shell
$ python original-translators/downward-release-24.06.0/src/translate/translate.py --keep-unimportant-variables tests/03/domain_all_outcomes.pddl tests/03/p1.pddl ; cat output.sas

begin_version
3
end_version
begin_metric
0
end_metric
2
begin_variable
var0
-1
2
Atom r()
NegatedAtom r()
end_variable
begin_variable
var1
-1
2
Atom q()
NegatedAtom q()
end_variable
0
begin_state
0
1
end_state
begin_goal
1
1 0
end_goal
3
begin_operator
ndset_q_detdup_1
0
1
0 1 -1 0
1
end_operator
begin_operator
ndset_q_detdup_3
0
1
0 0 -1 0
1
end_operator
begin_operator
unset_r
0
1
0 0 -1 1
1
end_operator
0
```

Now consider running the modified translator for FOND:

```shell
$ python translate/translate/translate.py tests/03/domain_all_outcomes.pddl tests/03/p1.pddl ; cat output.sas                         ─╯

begin_version
3
end_version
begin_metric
0
end_metric
1
begin_variable
var0
-1
2
Atom q()
NegatedAtom q()
end_variable
0
begin_state
1
end_state
begin_goal
1
0 0
end_goal
3
begin_operator
ndset_q_detdup_1
0
1
0 0 -1 0
1
end_operator
begin_operator
ndset_q_detdup_2
0
0
1
end_operator
begin_operator
ndset_q_detdup_3
0
0
1
end_operator
0
```

Here we can see we get it all: we simplify unimportant variables (`r` and its `unset_r` operator), but we keep all actions that are effect determinziation. See how `ndset_q_detdup_3` has become no-op because `r` is gone! 👍


Finally, we can get the same result in one shot on the original FOND domain if we use the `translate-allout` modified translator. Such translator has significant modifications as it also does the determinization. Note how the numbering of DETDUP actions start with 0 (rather than 1):

```
$ python translate-allout/translate/translate.py tests/03/domain_fond.pddl tests/03/p1.pddl ; cat output.sas 

begin_version
3
end_version
begin_metric
0
end_metric
1
begin_variable
var0
-1
2
Atom q()
NegatedAtom q()
end_variable
0
begin_state
1
end_state
begin_goal
1
0 0
end_goal
3
begin_operator
ndset_q_DETDUP_0 
0
1
0 0 -1 0
1
end_operator
begin_operator
ndset_q_DETDUP_1 
0
0
1
end_operator
begin_operator
ndset_q_DETDUP_2 
0
0
1
end_operator
0
```