#!/usr/bin/env python
from bhs_calendar import *
from icalendar import Calendar, Event, vText
import pytz
import tempfile, os


def time_string_to_deltatime(time_string):
    '''
    in: time string of the form "14:29"
    out: timedelta(hours=14, minutes=29)
    '''
    hor = int(time_string.split(":")[0])
    minu = int(time_string.split(":")[1])

    return td(hours=hor, minutes=minu) # time delta


def calendar_day_2timetable(full_calendar_day, schedule_times):
    '''
        ```Input:

        full_calendar_day:
        [datetime.datetime(2016, 6, 1, 0, 0),
        4, ['IB2 Reg. @7', '','Y11 Science @PL', '',
        'Y11 Phys 1 @PR', '9A Sc @PL'],]

        the schedule_times:
        {0: ("8:20", "8:40"), ...}  time of each period

        and converts it to a list of events.
        Each event is a tuple with the location, description and
        start and end of events each day:
    '''
    events_of_the_day = []

    if len(full_calendar_day) == 4:
        # it's a special day
        if full_calendar_day[3] == 'Half Day':
            start_of_lesson = full_calendar_day[0]+ time_string_to_deltatime("8:20")
            end_of_lesson = full_calendar_day[0]+ time_string_to_deltatime("12:30")
        else:
            start_of_lesson = full_calendar_day[0]+ time_string_to_deltatime("8:20")
            end_of_lesson = full_calendar_day[0]+ time_string_to_deltatime("15:30")
        lesson_location = '@BHS'
        lesson_description = full_calendar_day[3]
        events_of_the_day.append((lesson_description, lesson_location, start_of_lesson, end_of_lesson))
    else:
        for lesson_nr, lesson in enumerate(full_calendar_day[2]):
            if lesson: # is that time period empty? or is there a lesson?
                # Does it have a location? @followed by characters [a-zA-Z,_,-] no space
                location = re.compile(ur'\@\w*', re.DOTALL).findall(lesson)
                if location:
                    lesson_location = location[0][1:]
                else:
                    lesson_location = 'unspecified location'
                if lesson_nr == 0: # if it's the registration, write the day number
                    lesson_description = "[day %01d] " % full_calendar_day[1] + lesson
                elif lesson_nr == 1: # write the day number for the first lesson too
                    lesson_description = "[day %01d] " % full_calendar_day[1] + lesson
                else:
                    lesson_description = lesson
                start_of_lesson = full_calendar_day[0] + time_string_to_deltatime(schedule_times[lesson_nr][0])
                end_of_lesson = full_calendar_day[0] + time_string_to_deltatime(schedule_times[lesson_nr][1])
                events_of_the_day.append((lesson_description, lesson_location, start_of_lesson, end_of_lesson))

    print events_of_the_day
    return events_of_the_day


mycal = Calendar()

# for compliance with ical format:
mycal.add('prodid', '-//My BHS Calendar/afeito//')
mycal.add('version', '2.0')



for x in new_full_calendar:
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
    # print x
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
