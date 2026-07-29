This folder contains all ortools knowledge.
(`domain/` should not know about it, in the sense that it should not need the library).
Here are defined variables and contraints.
With them, the problem is built. 
With the problem, the solver is invoked.
So all these belong together but should be independent from each other (i.e. can be tested separately).
