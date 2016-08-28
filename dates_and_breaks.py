#!/usr/bin/env python
from datetime import datetime as dt
from datetime import timedelta as td
from collections import OrderedDict  # to remove duplicates from list

current_yr = 2016

first_day = [dt(current_yr, 9, 7)]
last_day = [dt(current_yr+1, 6, 29)]

# training, induction, professional development
staff_induction = [dt(current_yr, 8, 29),
                   dt(current_yr, 8, 30),
                   ]

# Professional development days for staff
staff_prof_development = [dt(current_yr, 8, 31),
                          dt(current_yr, 9, 1),
                          dt(current_yr, 9, 2),
                          dt(current_yr, 9, 6),
                          dt(current_yr+1, 1, 3),
                          dt(current_yr+1, 4, 17),
                          ]



# Secondary Meetings
secondary_meetings = [
                     [dt(current_yr, 8, 30, 8, 30), "Secondary Staff"],
                     [dt(current_yr, 8, 31, 8, 45), "All Staff"],
                     [dt(current_yr, 8, 31, 10, 45), "Secondary Staff"],
                     [dt(current_yr, 9, 2, 10, 30), "IB"],
                     [dt(current_yr, 9, 13, 15, 45), "Secondary Staff"],
                     [dt(current_yr, 9, 20, 15, 45), "HoD and HoY"],
                     [dt(current_yr, 9, 27, 15, 45), "Dept."],
                     [dt(current_yr, 10, 4, 15, 45), "Secondary Staff"],
                     [dt(current_yr, 10, 18, 15, 45), "Dept."],
                     [dt(current_yr, 11, 1, 15, 45), "HoD and HoY"],
                     [dt(current_yr, 11, 15, 15, 45), "Secondary Staff"],
                     [dt(current_yr, 11, 29, 15, 45), "IB"],
                     [dt(current_yr, 12, 6, 15, 45), "HoD and HoY"],
                     [dt(current_yr, 12, 13, 15, 45), "Dept."],

                     [dt(current_yr+1, 1, 10, 15, 45), "Dept."],
                     [dt(current_yr+1, 1, 17, 15, 45), "Secondary Staff"],
                     [dt(current_yr+1, 1, 24, 15, 45), "HoD and HoY"],
                     [dt(current_yr+1, 1, 31, 15, 45), "Dept."],
                     [dt(current_yr+1, 2, 7, 15, 45), "Secondary Staff"],
                     [dt(current_yr+1, 2, 21, 15, 45), "HoD and HoY"],
                     [dt(current_yr+1, 2, 28, 15, 45), "Dept."],
                     [dt(current_yr+1, 3, 7, 15, 45), "Secondary Staff"],
                     [dt(current_yr+1, 3, 14, 15, 45), "HoD and HoY"],
                     [dt(current_yr+1, 3, 21, 15, 45), "IB"],
                     [dt(current_yr+1, 3, 28, 15, 45), "Dept."],

                     [dt(current_yr+1, 4, 18, 15, 45), "Dept."],
                     [dt(current_yr+1, 4, 25, 15, 45), "Secondary Staff"],
                     [dt(current_yr+1, 5, 2, 15, 45), "HoD and HoY"],
                     [dt(current_yr+1, 5, 9, 15, 45), "Dept."],
                     [dt(current_yr+1, 5, 16, 15, 45), "Secondary Staff"],
                     [dt(current_yr+1, 5, 23, 15, 45), "Secondary Staff"],
                     [dt(current_yr+1, 6, 6, 15, 45), "HoD and HoY"],
                     [dt(current_yr+1, 6, 13, 8, 45), "All Staff"],
                     [dt(current_yr+1, 6, 20, 15, 45), "IB"],
                     ]

# half-days
half_days = [dt(current_yr, 12, 16),  # end of Term 1
             dt(current_yr+1, 3, 31),  # end of Term 2
             dt(current_yr+1, 6, 29),  # end of school
             ]

sports_day = [dt(current_yr+1, 3, 10)]

performing_arts_day = [dt(current_yr+1, 6, 28)]

# Holidays and mid-term, winter, spring breaks
# list of tuples with (start_date, end_date)
_breaks = [
          (dt(current_yr, 10, 24), dt(current_yr, 10, 28)),  # Half Term
          (dt(current_yr, 12, 19), dt(current_yr+1, 1, 2)),  # X-mas
          (dt(current_yr+1, 2, 13), dt(current_yr+1, 2, 17)),  # Mid-Term
          (dt(current_yr+1, 4, 3), dt(current_yr+1, 4, 14)),  # Spring Break
          ]

public_holidays = [
                  dt(current_yr, 9, 5),  # Labour Day
                  dt(current_yr, 11, 11),  # Remembrance Day
                  # dt(current_yr+1, 4, 14),  # Good Friday
                  # dt(current_yr+1, 4, 21),  # Agri-exhibition
                  dt(current_yr+1, 5, 24),  # BDA Day
                  dt(current_yr+1, 6, 19),  # National Heroes
                  ]

steam_week = [
              dt(current_yr+1, 6, 22),
              dt(current_yr+1, 6, 23),
              dt(current_yr+1, 6, 26),
              dt(current_yr+1, 6, 27),
              ]

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
            staff_prof_development + last_day + half_days # + \
            # performing_arts_day + steam_week


special_days = staff_induction + half_days + sports_day +\
               performing_arts_day + steam_week +\
               staff_prof_development


# remove duplicates, keep order
unique_no_teaching = list(OrderedDict.fromkeys(no_teaching))
unique_special_days = list(OrderedDict.fromkeys(special_days))

no_teaching = unique_no_teaching
special_days = unique_special_days
