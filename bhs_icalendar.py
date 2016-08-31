#!/usr/bin/env python
from bhs_calendar import *
from icalendar import Calendar, Event, vText
import pytz
import tempfile, os

from calendar_statistics import *

########################################
##### WARNING -> Spaguetti Code ahead!!
########################################

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
        'Y11 Phys 1 @PR', '9A Sc @PL','Lunch Duties @IB'],]

        the schedule_times:
        {0: ("8:20", "8:40"), ...,'L': ("12:20","13:10")}  time of each period

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

    return events_of_the_day


###############################
# Create the iCalendar Object
#      And Populate it.
###############################


mycal = Calendar()

# for compliance with ical format:
mycal.add('prodid', '-//My BHS Calendar/afeito//')
mycal.add('version', '2.0')



for x in new_full_calendar:
    for lesson in calendar_day_2timetable(x, schedule_times):
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
    mycal.add_component(event)

# Let's add meetings

def add_meetings(mycal, secondary_meetings, staff_prof_development):
    '''
     goes through list of meetings:
     [datetime.datetime(2017, 1, 17, 15, 45), 'Secondary Staff']
     and converts them to an event string:
     ('Secondary Staff', '', datetime.datetime(2017, 1, 17, 15, 45),
     datetime.datetime(2017, 1, 17, 15, 45))
     '''
    plus_an_hour = td(hours=1, minutes=0)
    plus_a_working_day = td(hours=7, minutes=0)
    for ameeting in secondary_meetings:
        event = Event()
        event.add('summary', ameeting[1]+' meeting') # eg. 'Department meeting'
        event['location'] = ''
        event.add('dtstart', ameeting[0])
        event.add('dtend', ameeting[0]+plus_an_hour)
        datestring = "%s" % ameeting[0]
        anid = (ameeting[1] + datestring).replace(' ', '').replace(':', '').replace('-', '')
        event['uid'] = anid
        mycal.add_component(event)

    for pd_day in staff_prof_development:
        event = Event()
        event.add('summary', 'Professional Development')
        event.add('description', 'Professional Development')
        event['location'] = 'BHS'
        event.add('dtstart', pd_day)
        event.add('dtend', pd_day+plus_a_working_day)
        datestring = "%s" % pd_day
        anid = ('ProDevel' + datestring).replace(' ', '').replace(':', '').replace('-', '')
        event['uid'] = anid
        mycal.add_component(event)

def collect_monday_statistics(new_full_calendar, list_of_lessons):
    '''
    do the lesson statistics for every monday and save it
    to a list with:
    [date, [statsIB1], [statsIB2], ..etc]
    '''
    monday_stats = []
    for aday in new_full_calendar:
        if aday[0].weekday() == 0:
            daystats = get_lesson_count_list(list_of_lessons, aday[0])
            monday_stats.append(daystats)
    return monday_stats

def format_stats_description(day_done_left, amonday):
        '''
        Creates string to display on Mondays
        '''
        days_string = \
        '''You have %s days of teaching left (excluding half days, holidays, PD days) and have taught %s days so far \n\n''' \
        % (day_done_left[1], day_done_left[0])

        lesson_string =""
        for lesson in amonday[1:]:
            sub_lesson_string = '''%s: %s LESSONS TAUGHT | %s LESSONS LEFT \n\n''' % \
            (lesson[0], lesson[1][0], lesson[1][1])
            lesson_string = lesson_string + sub_lesson_string

        full_string = days_string + lesson_string + '''This excludes study leave and exams. \n\n DISCLAIMER: You may have fewer lessons than indicated here due to the usual suspects: Torch Day, Days out, trips, etc.'''

        return full_string


def add_monday_statistics(mycal, monday_stats):
    for amonday in monday_stats:
        day_done_left = days_of_teaching_sofar(d_o_t, amonday[0])

        event = Event()
        event.add('summary', 'STATS THIS WEEK') # eg. 'Department meeting'
        event['location'] = ''
        event.add('dtstart', amonday[0]+td(hours=7, minutes=0))
        event.add('dtend', amonday[0]+td(hours=8, minutes=0))

        description_string = format_stats_description(day_done_left, amonday)
        print description_string, '\n', '#####################', '\n'

        event.add('description', description_string)
        datestring = "%s" % amonday[0]
        days_string = "%s%s" % (day_done_left[0], day_done_left[1])
        anid = (datestring+days_string).replace(' ', '').replace(':', '').replace('-', '')
        event['uid'] = anid
        mycal.add_component(event)

monday_statistics = collect_monday_statistics(new_full_calendar, list_of_lessons)


add_meetings(mycal, secondary_meetings, staff_prof_development)
add_monday_statistics(mycal, monday_statistics)

# add_statistics(mycal, all_mondays_lessons_and_count)




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
f = open('BHS_Calendar_2016_afeito.ics', 'wb')
f.write(mycal.to_ical())
f.close()


# print mycal.to_ical()  # generates a string for the icl file
