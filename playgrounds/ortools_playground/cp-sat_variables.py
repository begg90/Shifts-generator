"""
All possible cp_model VARIABLES:

IntVar 	    new_int_var (self, IntegralT lb, IntegralT ub, str name)
IntVar 	    new_int_var_from_domain (self, sorted_interval_list.Domain domain, str name)
IntVar 	    new_bool_var (self, str name)
IntVar 	    new_constant (self, IntegralT value)
pd.Series 	new_int_var_series (self, str name, pd.Index index, Union[IntegralT, pd.Series] lower_bounds, Union[IntegralT, pd.Series] upper_bounds)
pd.Series 	new_bool_var_series (self, str name, pd.Index index)
"""

from ortools.sat.python import cp_model
from ortools.sat.python import cp_model_helper
import pandas as pd

# create model
model = cp_model.CpModel()

# create integer variable
lower_boundary = 0
upper_boundary = 3
int_var = model.new_int_var(lower_boundary, upper_boundary, "a") # variable a can take values 0,1,2,3
print(int_var)
print(int_var.domain)
print(int_var.is_integer()) # is_integer() is a METHOD
print(int_var.is_boolean) # is an OBJECT???
print(int_var.model_proto) # summary of all
print(int_var.index) # returns the index of the variable: 0

# create integer variable from domain (a domain is a domain in the mathematical sense! So, an interval in connected, but a domain can be non-connected)
# IntVar 	new_int_var_from_domain (self, sorted_interval_list.Domain domain, str name)
int_var_domain = model.new_int_var_from_domain(cp_model.Domain.from_intervals([[1,2],[5,6]]),"b")
print(int_var_domain)
print(int_var_domain.domain)
print(int_var_domain.is_integer())
print(int_var_domain.is_boolean)
print(int_var_domain.model_proto) # this is a summary of ALL variables, not this one only
print(int_var_domain.index) # returns the index of the variable: 1

# create boolean variable
bool_var = model.new_bool_var("c")
print(bool_var)
print(bool_var.domain)
print(bool_var.is_integer()) # TRUE!!! [0,1]
print(bool_var.is_boolean) # TRUE
print(bool_var.model_proto)
print(bool_var.index) # returns the index of the variable: 2

# create a constant integer
# NB. some methods only take IntVar! E.g. model.AddAllowedAssignments
const_var = model.new_constant(8)
print(const_var)
print(const_var.domain)
print(const_var.is_integer())
print(const_var.is_boolean) # FALSE
print(const_var.model_proto)
print(const_var.index) # returns the index of the variable: 3

# create a series of integer variables
# these variables are pandas Series
int_series_var = model.new_int_var_series("d", pd.Index([1, 2, 3]), [0,0,1], [7,8,9])
print(int_series_var)
"""
1    d[1]
2    d[2]
3    d[3]
dtype: object
"""
#print(int_series_var.domain) # 'Series' object has no attribute 'domain'
#print(int_series_var.is_integer()) # 'Series' object has no attribute 'is_integer'
#print(int_series_var.is_boolean) # 'Series' object has no attribute 'is_boolean'
#print(int_series_var.model_proto) # 'Series' object has no attribute 'model_proto'
print(int_series_var.index) # returns Index([1, 2, 3], dtype='int64')

# create a series of boolean variables
# these variables are pandas Series
bool_series_var = model.new_bool_var_series("e", pd.Index(["a", "b", "c"]))
print(bool_series_var)
"""
a    e[a]
b    e[b]
c    e[c]
dtype: object
"""
print(bool_series_var.index) # returns Index(['a', 'b', 'c'], dtype='str')

# create a series of variables in a dataframe that is similar to the one we need
# NOTE: the intex contains only the dimensions we are deciding over: doctor, day, shift_type, for example.
# Seniority, vacation/availability should go somewhere else
doctors = ["eenie",
           "meenie",
           "miney",
           "moe"]
shift_types = [" day_duty","night_duty","day_AROS","night_AROS","night_on_call","24h_on_call"] # the internet told me that a "guardia" is a "duty doctor"
dates = [1,2,3] # only three days here, will contain dates
index = pd.MultiIndex.from_product(
    [doctors, dates, shift_types],
    names = ["doctor", "date", "shift"]
)
assign = model.new_bool_var_series(name = "assign", index=index)
print(assign)

