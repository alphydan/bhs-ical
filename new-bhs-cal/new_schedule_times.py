#!/usr/bin/env python

# definition of when the class periods begin and end
from datetime import timedelta as td

reg = td(hours=8, minutes=20)  # registration
l1 = td(hours=8, minutes=40)   # 1st period
l2 = td(hours=10, minutes=05)  # 2nd period
l3 = td(hours=11, minutes=15)  # 3rd period
l4 = td(hours=13, minutes=15)  # 4th period
l5 = td(hours=14, minutes=20)  # 5th period
lunch = td(hours=12, minutes=20)  # lunch

plus_a_registration = td(hours=0, minutes=20)
plus_half_an_hour = td(hours=0, minutes=30)
plus_a_lunch = td(hours=0, minutes=50)
plus_an_hour = td(hours=1, minutes=0)
plus_a_lesson = td(hours=1, minutes=5)
plus_half_a_day = td(hours=4, minutes=0)
plus_a_working_day = td(hours=7, minutes=0)

timetable_name = raw_input("What is the name of the timetable file? (without .csv ): ")
timetable_path_n_file = '../timetable_files/' + str(timetable_name) + '.csv'
# timetable_file = open(path_n_file, 'r',)
