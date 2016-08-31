from datetime import datetime as dt
from datetime import timedelta as td
import csv, re

from bhs_calendar import *
from dates_and_breaks import *

timetable = open('timetable_files/timetable.csv', 'r',)

def days_of_teaching_sofar(days_of_teaching, adate=None):
    '''Returns the total days of teaching left
       once we remove holidays, half-days, steam-week, vacations, art & sport day.
       input: a list with the days of teaching
    '''
    if adate is None: # not for a specific date (takes today)
        d_o_t_sofar = [x for x in days_of_teaching if x <= dt.now()]
        d_o_t_left = [x for x in days_of_teaching if x > dt.now()]
        return len(d_o_t_sofar), len(d_o_t_left)
    else: # a specific date has been given to calculate days left
        d_o_t_sofar = [x for x in days_of_teaching if x <= adate]
        d_o_t_left = [x for x in days_of_teaching if x > adate]
        return len(d_o_t_sofar), len(d_o_t_left)




def get_list_of_unique_lessons(timetable):
    '''
    `input`: timetable_dict
    `output`: unique lessons, for ex:
    ['IB1 Phys', 'IB2 D.tech', 'Y10 Phys 1', 'Lunch Duties',
    'Y11 Phys 2', 'Y11 Phys 1', '9A Sc', 'IB2 Reg.']
    '''

    tt_reader = csv.reader(timetable)
    tt_headers = tt_reader.next()
    timetable_dict = {}
    for row in tt_reader:
        timetable_dict[int(row[0])] = row[1:]
    timetable.close()


    all_lessons = []

    for i in timetable_dict:
        all_lessons += timetable_dict[i]

    regex = re.compile(ur'\@[\w\-]*', re.DOTALL)
    lessons_without_location = [regex.sub('', lesson).strip() for lesson in all_lessons]
    unique_lessons = list(set(lessons_without_location))
    # remove empty lessons:
    unique_lessons = [x for x in unique_lessons if x]
    # unique_lessons.remove('Lunch Duties')
    # unique_lessons.remove('Y10C Reg.')
    unique_lessons.remove('Y11B Reg.')

    return unique_lessons



def count_lesson_occurrences(full_calendar, lesson_string, adate=None):
    '''
    Count all the lessons of a particular lesson string in the full_calendar
    for example, how many times does "IB1 Phys" appear throughout the year.
    if adate is given, then count the lesson in the year starting from that
    date
    '''
    nr_of_lessons = 0
    nr_of_lessons_taught = 0

    for x in full_calendar:
        for timetable_this_day in x[2]:
            if (x[0] >= adate) and (lesson_string in timetable_this_day):
                if ('IB2' in lesson_string) and x[0] in IB2_study_n_exams:
                    pass
                elif ('IB1' in lesson_string) and x[0] in IB1_study_n_exams:
                    pass
                elif ('Y11' in lesson_string) and x[0] in Y11_study_n_exams:
                    pass
                elif ('Y10' in lesson_string) and x[0] in Y10_study_n_exams:
                    pass
                elif (('Y9' in lesson_string) or ('Y8' in lesson_string) or
                      ('Y7' in lesson_string)) and (x[0] in Y987_study_n_exams):
                    pass
                else:
                    nr_of_lessons +=1
                    # print lesson_string, '--', timetable_day
            if (x[0] < adate) and (lesson_string in timetable_this_day):
                if ('IB2' in lesson_string) and x[0] in IB2_study_n_exams:
                    pass
                elif ('IB1' in lesson_string) and x[0] in IB1_study_n_exams:
                    pass
                elif ('Y11' in lesson_string) and x[0] in Y11_study_n_exams:
                    pass
                elif ('Y10' in lesson_string) and x[0] in Y10_study_n_exams:
                    pass
                elif (('Y9' in lesson_string) or ('Y8' in lesson_string) or \
                     ('Y8' in lesson_string)) and (x[0] in Y987_study_n_exams):
                    pass
                else:
                    nr_of_lessons_taught +=1
                    # print lesson_string, '--', timetable_day

    return nr_of_lessons_taught, nr_of_lessons
    # print 'past:', nr_of_lessons_taught, '--', 'future:', nr_of_lessons, lesson_string, '\n'




full_calendar = new_full_calendar

list_of_lessons = get_list_of_unique_lessons(timetable)


def get_lesson_count_list(list_of_lessons, adate=dt.today()):
    '''
    starts with list of unique lessons:
    ['IB2 Phys', 'Y9 Sc', etc]
    Creates a dictionary with the number
    of lessons taught and left for the year:
    {'IB2 Phys':(dt(somedate),32,43), etc}
    '''
    lessons_and_count = [adate]
    for lesson in list_of_lessons:
        lessons_and_count.append([lesson, count_lesson_occurrences(full_calendar, lesson, adate)])
    # lessons_and_count['date'] = adate

    return lessons_and_count



