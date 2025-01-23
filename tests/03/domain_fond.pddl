(define (domain testdomain)
	(:requirements :strips :non-deterministic)
	(:predicates
		(p)
		(q)
		(r) ;; irrelevant proposition
	)

	;; make q true or no-op
	(:action ndset_q
		:parameters ()
		:precondition (p)
		:effect (oneof (q) (and) (r))
	)

	;; deterministically touch r
	(:action unset_r
		:parameters ()
		:precondition ()
		:effect (not (r))
	)

)