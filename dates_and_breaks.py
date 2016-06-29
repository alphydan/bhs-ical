#!/usr/bin/env python
from datetime import datetime as dt
from datetime import timedelta as td
from collections import OrderedDict  # to remove duplicates from list

current_yr = 2015

# training, induction, professional development
staff_induction = [dt(current_yr, 8, 27),
                   dt(current_yr, 8, 28)]

# Secondary Meetings
secondary_meetings = [[dt(current_yr, 12, 15, 15, 45), "IB"],
      [dt(current_yr+1, 1, 5, 15, 45), "HoD and HoY"],
      [dt(current_yr+1, 1, 12, 15, 45), "Dept. Meeting"],
      [dt(current_yr+1, 1, 19, 15, 45), "T&L Prof. Learning Groups"],
      [dt(current_yr+1, 1, 26, 15, 45), "IB"],
      [dt(current_yr+1, 2, 2, 15, 45),  "Whole School Planning - Vertical"],
      [dt(current_yr+1, 2, 16, 15, 45), "PTC Yr 9"],
      [dt(current_yr+1, 2, 23, 15, 45), "Dept. Meeting"],
      [dt(current_yr+1, 3, 1, 15, 45), "HoD and HoY"],
      [dt(current_yr+1, 3, 8, 15, 45), "PTC IB1"],
      [dt(current_yr+1, 3, 15, 15, 45), "Dept. Meeting"],
      [dt(current_yr+1, 3, 22, 15, 45), "T&L Professional Learning Groups"],
      ]


# Professional development days for staff
staff_prof_development = [dt(current_yr, 8, 31),
                          dt(current_yr, 9, 1),
                          dt(current_yr, 9, 2),
                          dt(current_yr, 9, 3),
                          dt(current_yr, 9, 4),
                          dt(current_yr+1, 1, 4),]
                          # dt(current_yr+1, 4, 11)] # IS THIS Prof. Dev. or not?

# half-days
half_days = [dt(current_yr, 12, 18),
             dt(current_yr+1, 3, 24),
             dt(current_yr+1, 6, 30)]

# Holidays and mid-term, winter, spring breaks
# list of tuples with (start_date, end_date)
_breaks = [(dt(current_yr, 10, 26), dt(current_yr, 10, 30)),  # public holiday
           (dt(current_yr, 12, 18), dt(current_yr+1, 1, 4)),  # X-mas
           (dt(current_yr+1, 2, 8), dt(current_yr+1, 2, 12)),  # Mid-Term
           (dt(current_yr+1, 3, 24), dt(current_yr+1, 4, 10)),  # Spring Break
           (dt(current_yr+1, 6, 30), dt(current_yr+1, 7, 1))]   # last day

public_holidays = [
                  dt(current_yr, 11, 11),  # Remembrance Day
                  dt(current_yr+1, 3, 25),  # Good Friday
                  dt(current_yr+1, 4, 15),  # Agri-exhibition
                  dt(current_yr+1, 5, 24),  # BDA Day
                  dt(current_yr+1, 6, 20),  # National Heroes
                  ]


first_day = [dt(current_yr, 9, 8)]
last_day = [dt(current_yr+1, 7, 1)]

# Define the full list of break days
breaks = []
a_day = td(days=1)  # timedelta of a day

for br in _breaks:
    if br[0] == br[1]:  # single day break
        breaks.append(br[0])
    else:  # multi-day holiday
        breaks.append(br[0])
        next_day = br[0] + a_day
        while next_day != (br[1] + a_day):
            breaks.append(next_day)
            next_day = next_day + a_day


# Let's make a list with the days which are not teaching days (no lessons)
# we can combine the lists of induction, prof. dev., breaks
# half days and last day

no_teaching = breaks + public_holidays + staff_induction + \
            staff_prof_development + last_day + half_days

# remove duplicates, keep order
unique_no_teaching = list(OrderedDict.fromkeys(no_teaching))
no_teaching = unique_no_teaching
