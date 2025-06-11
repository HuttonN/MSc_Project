(define
	(problem trainpddl)
	(:domain trainpddl)
	(:objects
		branch1 branch2 - branch
		junction2 - junction
		station7 station15 station20 - station
		tn - train
	)
	(:init (isAt tn branch1) (isBranch station7 branch1) (isBranch station15 branch1) (isBranch station20 branch2) (connected junction2 branch1 branch2))
	(:goal (and (visited tn station15) (visited tn station7)))
)
