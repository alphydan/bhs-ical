#!/usr/bin/env python
from bhs_calendar import *
from icalendar import Calendar, Event, vText
import pytz
import tempfile, os


mycal = Calendar()

# for compliance with ical format:
mycal.add('prodid', '-//My BHS Calendar/afeito//')
mycal.add('version', '2.0')


for x in full_calendar:
    for lesson in calendar_day_2timetable(x, schedule_times):
        # print lesson
        event = Event()
        event.add('summary', lesson[0])
        event['location'] = vText(lesson[1])
        event.add('dtstart', lesson[2])
        event.add('dtend', lesson[3])
        datestring = "%s" % lesson[3]
        anid = (lesson[0] + datestring).replace(' ', '').replace(':', '').replace('-', '')
        event['uid'] = anid

        mycal.add_component(event)

    event = Event()
    event.add('summary', '[day %01d]' % x[1])
    event.add('dtstart', x[0])
    event.add('dtend', x[0]) # all day event (will appear at start of day)
    print x
    mycal.add_component(event)




# Create a [day n] event (full day event at the top of the calendar)
# Create an overview of "days left" inside the description of that day
# Add half days (registration + big period until mid-day)

# event = Event()
# event.add('summary', 'IB2 Reg. @7')

# event.add('dtstart', dt(2015, 12, 12, 8, 20, 0, tzinfo=pytz.utc))
# event.add('dtend', dt(2015, 12, 12, 8, 50, 0, tzinfo=pytz.utc))
# event.add('dtstamp', dt(2015, 12, 12, 0, 50, 0, tzinfo=pytz.utc))

# event['location'] = vText('PL')
# event['uid'] = '2015910820/IB2Reg@7'




# Write to file
f = open('example.ics', 'wb')
f.write(mycal.to_ical())
f.close()


# print mycal.to_ical()  # generates a string for the icl file
