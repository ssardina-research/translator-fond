(define (domain testdomain)
    (:requirements :strips)
    (:predicates (p) (q) (r))
    (:action ndset_q_DETDUP_1
        :parameters ()
        :precondition (p)
        :effect (q)
    )
     (:action ndset_q_DETDUP_2
        :parameters ()
        :precondition (p)
        :effect (and )
    )
     (:action unset_r
        :parameters ()
        :precondition (and)
        :effect (not (r))
    )
)