#!/usr/bin/env python
from datetime import datetime as dt
from datetime import timedelta as td

current_yr = 2015

# training, induction, professional development
staff_induction = [dt(current_yr, 8, 27),
                   dt(current_yr, 8, 28)]

# Professional development days for staff
staff_prof_development = [dt(current_yr, 8, 31),
                          dt(current_yr, 9, 1),
                          dt(current_yr, 9, 2),
                          dt(current_yr, 9, 3),
                          dt(current_yr, 9, 4),
                          dt(current_yr+1, 1, 4),
                          dt(current_yr+1, 4, 11)]

# half-days
half_days = [dt(current_yr, 12, 18),
             dt(current_yr+1, 3, 24),
             dt(current_yr+1, 6, 30)]

# Holidays and mid-term, winter, spring breaks
_breaks = [(dt(current_yr, 10, 26), dt(current_yr, 10, 30)), # public holiday
           (dt(current_yr, 12, 18), dt(current_yr+1, 1, 4)), # Mid-Term
           (dt(current_yr+1, 2, 8), dt(current_yr+1, 2, 12)),
           (dt(current_yr+1, 3, 24), dt(current_yr+1, 4, 11)),
           (dt(current_yr+1, 6, 30), dt(current_yr+1, 7, 1))]

public_holidays = [
           (dt(current_yr, 11, 11), dt(current_yr, 11, 11)), # Remembrance Day
           (dt(current_yr+1, 4, 15), dt(current_yr+1, 4, 15)), # Agri-exhibition
           (dt(current_yr+1, 5, 24), dt(current_yr+1, 5, 24)), # BDA Day
           (dt(current_yr+1, 6, 20), dt(current_yr+1, 6, 20)),
]


first_day = [dt(current_yr, 9, 8)]
last_day = [dt(current_yr+1, 7, 1)]


# Define the full list of break days
breaks = []
a_day = td(days=1)  # timedelta of a day

for br in _breaks:
    if br[0] == br[1]:  # single day holiday
        breaks.append(br[0])
    else:  # multi-day holiday
        breaks.append(br[0])
        next_day = br[0] + a_day
        while next_day != (br[1] + a_day):
            breaks.append(next_day)
            next_day = next_day + a_day

print breaks
