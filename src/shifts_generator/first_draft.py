"""an example module"""

from ortools.sat.python import cp_model
import numpy as np

model = cp_model.CpModel()


def return_true():
    """example function to test pytest"""
    return True

def create_variables(num_employees, num_days, num_shifts):
    return True