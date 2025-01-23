; p1: easy should have both strong and strong-cyclic solutions - just do sq and get the goal
(define (domain testdomain)
	(:requirements :strips)
	(:predicates
		(p)
		(q)
		(r)	;; totally irrelevant predicate
	)

	;; deterministically make q true
	(:action set_q
		:parameters ()
		:precondition (p)
		:effect (q)
	)

	;; deterministically make r false (touch r)
	(:action unset_r
		:parameters ()
		:precondition ()
		:effect (not (r))
	)
)