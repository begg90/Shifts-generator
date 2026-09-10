The domain level is general. It does not handle data, it does not use ORTools.
Here we define classes that will be passed to the solver level.
It can contain employee, shifts, schedule, constraint (abstract)
This way it can be tested without invoking the solver.

BEA's notes:
- how important is it to freeze the classes right away?
- what level of abstraction for the contraints?
- do we really need an enums.py file or can we do without and create it when
we find out we have more of that type of data?
- I am ok with enums.py being here, in general, because it contains domain knowledge
- is `domain/` a good name for this folder or would `model/` be more suitable?

