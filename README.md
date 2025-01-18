# FOND SAS Translators

This repo contains SAS-based translators for FOND domains. Both are modifications of the [SAS translator](https://www.fast-downward.org/TranslatorOutputFormat) shipped with the [Downard](https://github.com/aibasel/downward/) planning framework.

Two translators are provided in this repo:

- [`translate`](translate/): this version is a slight variant of the original translator that does not simplify any action that was the result of determinizing a FOND problem. These are actions whose names include the string "`DETDUP`": they will always be kept, even if they are "no-op" actions with no effects.
- [`translate-allout`](translate-allout/): this version first computes the all-outcome determinization for FOND domains and then performs the SAS translation. It is based on the 2011 [PRP](https://github.com/ssardina-planning/planner-for-relevant-policies) version but updated to a newer version.

Please refer to the corresponding README files for each version.

## Contributors

The codebase is a modification/extension of the translators found in [Downard](https://github.com/aibasel/downward) library (which ships the SAS translation) and [PRP](https://github.com/QuMuLab/planner-for-relevant-policies) planner (which added determinization to the original SAS translation).

- Sebastian Sardina (ssardina@gmail.com)
- Nitin Yadav (nitin.yadav@unimelb.edu.au)

