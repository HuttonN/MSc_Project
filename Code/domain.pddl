(define
	(domain trainpddl)
	(:requirements :strips :typing)
	(:types
		station
		branch
		junction
		train
	)
	(:predicates
		(connected )
		(isAt )
		(visited )
		(isBranch )
	)
	(:action stop
		:parameters (?tn ?s1 ?b1)
		:precondition (and 
			(isAt ?tn ?b1) 
			(isBranch ?s1 ?b1)
		)
		:effect (visited ?tn ?s1)
	)
	(:action switchBranch
		:parameters (?tn ?j ?b1 ?b2)
		:precondition (and 
			(isAt ?tn ?b1) 
			(connected ?j ?b1 ?b2)
		)
		:effect (and
			(isAt ?tn ?b2) 
			(not
				(isAt ?tn ?b1)
			)
		)
	)

	(:action returnBranch
		:parameters (?tn ?j ?b1 ?b2)
		:precondition (and 
			(isAt ?tn ?b1) 
			(connected ?j ?b2 ?b1)
		)
		:effect (and
			(isAt ?tn ?b2) 
			(not
				(isAt ?tn ?b1)
			)
		)
	)
)