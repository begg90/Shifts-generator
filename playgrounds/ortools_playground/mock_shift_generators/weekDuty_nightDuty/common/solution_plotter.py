# a simple plotter for the solution

import dayplot as dp
import matplotlib.pyplot as plt
import pandas as pd


def solution_plotter(df:pd.DataFrame, file_name:str):

    fig, ax = plt.subplots()
    dp.calendar(
        dates=df["date"],
        values=df["doc"],
        legend = True,
        legend_labels= "auto",
        start_date="2026-09-01",
        end_date="2026-09-30",
        boxstyle="round",
        ax=ax,
    )
    #plt.show() # we need a gui for this (e.g. pyqt6)
    plt.tight_layout()
    plt.savefig(f"weekDuty_nightDuty/output/{file_name}.png")
    plt.close(fig)

    