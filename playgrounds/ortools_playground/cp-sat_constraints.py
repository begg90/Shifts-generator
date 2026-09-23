"""
All of the possible cp-sat CONSTRAINTS:

Constraint 	add_linear_constraint (self, LinearExprT linear_expr, IntegralT lb, IntegralT ub)
Constraint 	add_linear_expression_in_domain (self, LinearExprT linear_expr, sorted_interval_list.Domain domain)
Constraint 	add (self, Union[BoundedLinearExpression, bool, np.bool_] ct)
Constraint 	add_all_different (self, Iterable[LineaexprrExprT] essions)
Constraint 	add_all_different (self, *LinearExprT expressions)
 	        add_all_different (self, *expressions)
Constraint 	add_element (self, LinearExprT index, Sequence[LinearExprT] expressions, LinearExprT target)
Constraint 	add_circuit (self, Sequence[ArcT] arcs)
Constraint 	add_multiple_circuit (self, Sequence[ArcT] arcs)
Constraint 	add_allowed_assignments (self, Sequence[LinearExprT] expressions, Iterable[Sequence[IntegralT]] tuples_list)
Constraint 	add_forbidden_assignments (self, Sequence[LinearExprT] expressions, Iterable[Sequence[IntegralT]] tuples_list)
Constraint 	add_automaton (self, Sequence[LinearExprT] transition_expressions, IntegralT starting_state, Sequence[IntegralT] final_states, Sequence[tuple[IntegralT, IntegralT, IntegralT]] transition_triples)
Constraint 	add_inverse (self, Sequence[VariableT] variables, Sequence[VariableT] inverse_variables)
Constraint 	add_reservoir_constraint (self, Sequence[LinearExprT] times, Sequence[LinearExprT] level_changes, int min_level, int max_level)
Constraint 	add_reservoir_constraint_with_active (self, Sequence[LinearExprT] times, Sequence[LinearExprT] level_changes, Sequence[LiteralT] actives, int min_level, int max_level)
 	        add_map_domain (self, IntVar var, Iterable[IntVar] bool_var_array, IntegralT offset=0)
Constraint 	add_implication (self, LiteralT a, LiteralT b)
Constraint 	add_bool_or (self, Iterable[LiteralT] literals)
Constraint 	add_bool_or (self, *LiteralT literals)
 	        add_bool_or (self, *literals)
Constraint 	add_at_least_one (self, Iterable[LiteralT] literals)
Constraint 	add_at_least_one (self, *LiteralT literals)
 	        add_at_least_one (self, *literals)
Constraint 	add_at_most_one (self, Iterable[LiteralT] literals)
Constraint 	add_at_most_one (self, *LiteralT literals)
Constraint 	add_at_most_one (self, *literals)
Constraint 	add_exactly_one (self, Iterable[LiteralT] literals)
Constraint 	add_exactly_one (self, *LiteralT literals)
 	        add_exactly_one (self, *literals)
Constraint 	add_bool_and (self, Iterable[LiteralT] literals)
Constraint 	add_bool_and (self, *LiteralT literals)
 	        add_bool_and (self, *literals)
Constraint 	add_bool_xor (self, Iterable[LiteralT] literals)
Constraint 	add_bool_xor (self, *LiteralT literals)
 	        add_bool_xor (self, *literals)
Constraint 	add_min_equality (self, LinearExprT target, Iterable[LinearExprT] expressions)
Constraint 	add_min_equality (self, LinearExprT target, *LinearExprT expressions)
Constraint 	add_min_equality (self, target, *expressions)
Constraint 	add_max_equality (self, LinearExprT target, Iterable[LinearExprT] expressions)
Constraint 	add_max_equality (self, LinearExprT target, *LinearExprT expressions)
Constraint 	add_max_equality (self, target, *expressions)
Constraint 	add_division_equality (self, LinearExprT target, LinearExprT num, LinearExprT denom)
Constraint 	add_abs_equality (self, LinearExprT target, LinearExprT expr)
Constraint 	add_modulo_equality (self, LinearExprT target, LinearExprT expr, LinearExprT mod)
Constraint 	add_multiplication_equality (self, LinearExprT target, *Union[Iterable[LinearExprT], LinearExprT] expressions)

Service constraints for the add_no_overlap constraint
IntervalVar 	new_interval_var (self, LinearExprT start, LinearExprT size, LinearExprT end, str name)
pd.Series 	    new_interval_var_series (self, str name, pd.Index index, Union[LinearExprT, pd.Series] starts, Union[LinearExprT, pd.Series] sizes, Union[LinearExprT, pd.Series] ends)
IntervalVar 	new_fixed_size_interval_var (self, LinearExprT start, IntegralT size, str name)
pd.Series 	    new_fixed_size_interval_var_series (self, str name, pd.Index index, Union[LinearExprT, pd.Series] starts, Union[IntegralT, pd.Series] sizes)
IntervalVar 	new_optional_interval_var (self, LinearExprT start, LinearExprT size, LinearExprT end, LiteralT is_present, str name)
pd.Series 	    new_optional_interval_var_series (self, str name, pd.Index index, Union[LinearExprT, pd.Series] starts, Union[LinearExprT, pd.Series] sizes, Union[LinearExprT, pd.Series] ends, Union[LiteralT, pd.Series] are_present)
IntervalVar 	new_optional_fixed_size_interval_var (self, LinearExprT start, IntegralT size, LiteralT is_present, str name)
pd.Series 	    new_optional_fixed_size_interval_var_series (self, str name, pd.Index index, Union[LinearExprT, pd.Series] starts, Union[IntegralT, pd.Series] sizes, Union[LiteralT, pd.Series] are_present)

Constraint 	add_no_overlap (self, Iterable[IntervalVar] intervals)
Constraint 	add_no_overlap_2d (self, Iterable[IntervalVar] x_intervals, Iterable[IntervalVar] y_intervals)
Constraint 	add_cumulative (self, Iterable[IntervalVar] intervals, Iterable[LinearExprT] demands, LinearExprT capacity)
"""

from ortools.sat.python import cp_model
from ortools.sat.python import cp_model_helper
import pandas as pd

# create model
model = cp_model.CpModel()

# create variables to use to test the constraints
x = model.new_int_var(0,10,"x")
y = model.new_int_var(0,10,"y")
#print(y.model_proto)

# add a linear constraint
lower_boundary = 0
upper_boundary = 10
model.add_linear_constraint( x+y , lower_boundary, upper_boundary)
#print(model)

# add a constraint that is a linear expression in a domain
model.add_linear_expression_in_domain(2*x+y, cp_model.Domain.from_intervals([[1,2],[5,6]]))
#print(model)

# add a constraint tahat is a BOUNDED LINEAR expression
model.add(x+3*y == 4)
model.add(x!=y)
#print(model)

# add a constraint that requires all given expressions to have different values
model.add_all_different( 2*x+3*y, 3*x+2*y )
#print(model)

# add an element constraint -- in the sense that you add a constraint which is a (linear) function of your variable(s)
# add_element(index, expression, target) enforces expression[index] == target
# this the contraint you use when "which entry do I look up" is part of the decision
# might be worth inspecting, because it can be used similarly to add_allowed_assignment
# NB: the solver chooses the index
# e.g., I have machines (index) that runs for different amount of time (expression) 
# and I would like the durantion of a run to be within some interval of time (target)
# index and expressions must be the same length
# each parameter of add_element can be a linear expression in which each term must be IntVar (hence a constant number must be a new_constant)
# EXAMPLE for our problem:
# we have juniors/seniors that can take different roles. The seniority could be the index, the role could be the expression. 
# The target could be... I don't know, something, e.g. coverage.
index = model.new_int_var(0, 3, "machine")
expressions = [3, 7, 2, 5]
target = model.new_int_var(0, 10, "duration")
model.add_element(index, expressions, target)
#print(model)


# add a circuit as a list of arcs that form a graph
# probably more suited for route planning
# an arc is a tuple (source_node, destination_node, boolean literal)
route1 = model.new_bool_var("route1")
route2 = model.new_bool_var("route2")
route3 = model.new_bool_var("route3")
list_of_arcs = [(0,1,route1),(1,2,route2),(2,3,route3)]
model.add_circuit(list_of_arcs)
#print(model)

# add a proper route made of graphs
# will not test it because probably not in our scope
# model.add_multiple_circuit(sequence_of_arcs)

# add allowed assignments
# takes in a list of linear expressions and a list of admissible tuples (which cannot be linear expressions)
# e.g.: only seniors are allowed to do the 24h on call shift
# e.g.: only seniors are allowed to do the night on call
# not entirely sure how to use it properly with new_bool_var_series as variables
# NB: this type of constraint should be used for rules that cannot be broken up in simpler pieces
# NBB: This is NOT the way we will create our variables
senior1 = model.new_bool_var("senior1")
senior2 = model.new_bool_var("senior2")
junior1 = model.new_bool_var("junior1")
junior2 = model.new_bool_var("junior2")
doctors = [senior1,senior2,junior1,junior2]
allowed_24h_on_call = [(1,0,0,0),(0,1,0,0)]
model.add_allowed_assignments(doctors, allowed_24h_on_call)
#print(model)

# add forbidden assignments
# A ForbiddenAssignments constraint is a constraint on an array of affine
# expressions where the list of impossible combinations is provided in the
# tuples list.
# e.g. A doctor cannot work the day before and after a night AROS shift
# NB: this type of constraint should be used for rules that cannot be broken up in simpler pieces
# only use these table-type contraints (add_forbidden_assignment, add_allowed_assignment) when there is not logical rule,
# or there is no way to break up the rule in simpler pieces. These constraints do not scale well, 
# because they carry tables in memory (see print(model))!
# Only use them when there is no way around it. 
# NOTE TO SELF: this might be the case for "there should always be a senior with a junior doing day duty"


#add_automaton
#add_inverse
#add_reservoir_constraint
#add_reservoir_constraint_with_active
#add_map_domain

# add implication: "works_AROS_night_shift" implies "is_off_next_day"
# this is a better way to make sure that who works a night shift (AROS, not on call!) does not work the day before and after
works_AROS_night_shift = model.new_bool_var("works_AROS_night_shift")
is_off_next_day = model.new_bool_var("is_off_next_day")
model.add_implication(works_AROS_night_shift, is_off_next_day)
#print(model)

# add_bool_or: At least one is true
# Adds `Or(literals) == true`: sum(literals) >= 1.
var1 = model.new_bool_var("var1")
var2 = model.new_bool_var("var2")
model.add_bool_or([var1,var2])
#print(model)
# THESE are similar, not going to test them
# add_bool_and: all are true
# Adds `And(literals) == true`.
# add_bool_xor
# does not support .only_enforce_if().

# add_at_least_one: Same as `add_bool_or`: `sum(literals) >= 1`.
# add_at_most_one: Adds `AtMostOne(literals)`: `sum(literals) <= 1`.
# add_exactly_one: Adds `ExactlyOne(literals)`: `sum(literals) == 1`.


# add_min_equality: Adds `target == Min(expressions)`.
# add_max_equality: Adds `target == Max(expressions)`.

# No need to go through ALL possible constraint in this setting
