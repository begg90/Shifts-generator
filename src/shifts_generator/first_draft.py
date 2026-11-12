"""an example module"""

from ortools.sat.python import cp_model

model = cp_model.CpModel()


def return_true():
    """example function to test pytest"""
    return True
