# iCal file generator for BHS Calendar

creates an **.ics** file to import a school calendar (based on 6 day weeks) to google calendar / icalendar.

# Dependencies

To run the script you will need the python [icalendar](http://icalendar.readthedocs.org/) Package.

# How it works

The public holidays, breaks, training days, etc ... are declared in [dates_and_breaks.py](dates_and_breaks.py).
Each day is split in 5 periods, and the starting and end time of each period is declared in [schedule_times.py](schedule_times.py)
Each teacher / student then needs to create an excel file with their timetable and save it at [timetable_files/timetable.csv](timetable_files/timetable.csv). 

To describe the classroom or location of our class, we will use an `@` symbol.  So for example teaching physics in the physics lab will be recorded as:  `Phys Y11 @PhysicsLab`  (Note that the location needs to have no spaces.  So "`@PL`", `@ChemLab` or "`34`" are acceptable, but "`room 34`" is not.)

`bhs_calendar.py` will import the breaks and holidays, the schedules and the specific timetable.  It will then create a list of all the days
from the first day of school to the last and exclude `breaks + public_holidays + staff_induction + staff_prof_development + last_day_of_school`).  This leaves the variable `d_o_t` (*day of teaching*) only with the days when there are actual lessons.


