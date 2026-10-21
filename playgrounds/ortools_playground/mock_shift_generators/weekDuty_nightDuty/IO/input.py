# ruff: noqa

from ..common.local_enums import SeniorityLevel
from ..common.calendar_manager import CalendarManager

def get_data(year,month):
    # personnel
    doctors = [{"name":"eenie","seniority":SeniorityLevel.SENIOR.name},
               {"name":"meenie","seniority":SeniorityLevel.SENIOR.name},
               {"name":"miney","seniority":SeniorityLevel.SENIOR.name},
               {"name":"moe","seniority":SeniorityLevel.SENIOR.name},
               {"name":"tom","seniority":SeniorityLevel.SENIOR.name},
               {"name":"jerry","seniority":SeniorityLevel.SENIOR.name},
               {"name":"mini1","seniority":SeniorityLevel.JUNIOR.name},
               {"name":"mini2","seniority":SeniorityLevel.JUNIOR.name},
               {"name":"mini3","seniority":SeniorityLevel.JUNIOR.name}]

    cal = CalendarManager(year,month)
    days_cal = cal.dates() # complete month,
    dutyWeek_cal = cal.duty_weeks() # weeks 
    
    return doctors, days_cal, dutyWeek_cal