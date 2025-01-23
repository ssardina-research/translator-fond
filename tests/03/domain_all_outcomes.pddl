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
     (:action ndset_q_DETDUP_3
        :parameters ()
        :precondition (p)
        :effect (r)
    )
     (:action unset_r
        :parameters ()
        :precondition ()
        :effect (not (r))
    )
)