import argparse
import itertools
import logging
import os
import coloredlogs

from pddl.logic.effects import AndEffect
from pddl.logic.base import And, OneOf
from pddl import parse_domain
from pddl.core import Domain, Action
from pddl.formatter import domain_to_string


def fond2allout(fond_domain_file: str):
    """
    Translate APP to FOND and save the FOND problem in the output directory

    Note: the code inside _get_fond comes from pypddl parser
    """
    fond_domain: Domain = parse_domain(fond_domain_file)

    # Uncomment if having problem parsing the domain and APP problem
    # print("Domain name:", domain.name)
    # print("Problem name:", problem.name)
    # exit(1)

    new_actions = []
    for act in fond_domain.actions:
        # collect all oneof effect of act in a list of lists oneof_effects
        # an action should start with an AndEffect (which may have OneOf blocks) or directly with a single OneOf
        if isinstance(act.effect, AndEffect):
            operands = act.effect.operands
        elif isinstance(act.effect, OneOf):
            operands = [act.effect]
        else:
            print("Found an action effect that is not an AND or a OneOf. Type of effect:", type(act.effect))
            print(act.effect)
            exit(1)
        det_effects = []
        oneof_effects = []
        nd_action = False
        for e in operands:
            if not isinstance(e, OneOf):
                det_effects.append(e)
                continue
            nd_action = True
            oneof_effects.append(list(e.operands))

        print(oneof_effects)
        # build deterministic actions for act
        if nd_action:
            for i, one_effect in enumerate(list(itertools.product(*oneof_effects))):
                print(i)
                new_effect = det_effects + list(one_effect)
                a = Action(f"{act.name}_DETDUP_{i}",
                    parameters=act.parameters,
                    precondition=act.precondition,
                    effect=And(*new_effect))
                new_actions.append(a)
        else:
            new_actions.append(act)

    # finally, build the domain
    allout_domain = Domain(f"{fond_domain.name}_ALLOUT",
                    requirements=fond_domain.requirements,
                    types=fond_domain.types,
                    constants=fond_domain.constants,
                    predicates=fond_domain.predicates,
                    actions=new_actions)

    return allout_domain


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Translate APP to FOND problem (domain + problem files)')
    parser.add_argument("domain",
                        nargs="?",
                        help="domain PDDL file.")
    parser.add_argument('--print',
                        action='store_true',
                        default=False,
                        help='dump encoding to terminal too (Default: %(default)s)')

    args = parser.parse_args()

    base_name, _ = os.path.splitext(os.path.basename(args.domain))
    fond_domain_file = f"{base_name}-allout.pddl"

    allout_domain = fond2allout(os.path.abspath(args.domain), fond_domain_file)

    if args.print:
        print(domain_to_string(allout_domain))
