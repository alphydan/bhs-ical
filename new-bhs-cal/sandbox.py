from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch,cm
from reportlab.platypus import Image, Paragraph

from datetime import timedelta as td

from print_planner import total_weekly_lessons, \
                          weekly_lesson_configurations, \
                          weeks_dict,full_schedule_by_year, \
                          cal_list, all_weeks

from import_fun_and_stats import short_statistics

c = canvas.Canvas("hello.pdf", pagesize=letter)
c.setAuthor("Alvaro Feito Boirac")
width, height = letter

top_margin = 1*inch
left_margin = 0.93*inch
left_margin = 1.2*inch
right_margin = 0.88*inch
right_margin = 0.68*inch
bottom_margin = 0.45*inch



# First class Pages
def create_class(class_string):
    ''' list of students
    '''
    pass
    # do this in excel!


# BHS & Date Header
def create_header(c, aweek, size="Large"):
    c.drawImage('../img/bhs_CMYK.tif', width-2.1*inch, height - 0.85 * inch, 89,30)
    # canvas.drawImage(self, image, x,y, width=None,height=None,mask=None)
    if size == "Large":
        c.setFont("Helvetica", 20)
        c.drawString(width/2-3*cm, height-0.8*inch, aweek)
    if size == "Small":
        c.setFont("Helvetica", 12)
        c.drawString(left_margin+0.7*cm, height-0.8*inch, aweek)

# Draw margins:
def draw_margins(c):
    '''Draws Margins for printing
    '''
    c.line(left_margin, 0, left_margin, height)  # left_margin
    c.line(0, bottom_margin, width, bottom_margin)  # bottom
    c.line(width-right_margin, 0, width-right_margin, height)  # right
    c.line(0, height-top_margin, width, height-top_margin)  # top


    c.setStrokeColorRGB(1, 0.1, 0.1)  # red
    c.line(0.88*inch, 0, 0.88*inch, height)  # left_margin
    c.line(0, 0.31*inch, width, 0.31*inch)  # bottom
    c.line(width-0.88*inch, 0, width-0.88*inch, height)  # right
    c.line(0, height-0.31*inch, width, height-0.31*inch)  # top

#################
# Lesson Boxes  #
#################
def create_columns(lessons, side='L'):

        '''
        Creates boxes for Y8, Y10, Y11(1), Y11(6) (left)
        or for IB1, IB2, Lab requisitions (right)
        side can be 'L' or 'R'
        '''
        c.setLineWidth(2)
        c.setStrokeColorRGB(0.4, 0.4, 0.4)

        height_for_boxes = height-top_margin-bottom_margin
        c.setFont("Helvetica", 12)

        lesson_title = {'L': ['Y8A', 'Y10(1)', 'Y11(1)', 'Y11(6)'],
                        'R': ['IB1', 'IB2', 'Lab.']}

        if sum(lessons) == 0:
            pass
        else:
            bx_height_unit = height_for_boxes/sum(lessons)
            box_width = (width-left_margin-right_margin)/2
            round_corner = 8

            for i, x in enumerate(lessons):
                height_of_box = bx_height_unit*x
                position_of_box = bx_height_unit*sum(lessons[0:(i+1)])
                if side == 'L':
                    box_left_margin = left_margin
                    text_left_margin = left_margin+box_width-1.3*cm
                else:
                    box_left_margin = left_margin + box_width
                    text_left_margin = width - right_margin - 1*cm
                c.roundRect(box_left_margin, height-top_margin-position_of_box,
                            box_width, height_of_box, round_corner)
                if x != 0: # there are lessons
                        c.drawString(text_left_margin,
                                     height-top_margin-position_of_box+
                                     height_of_box-0.5*cm, lesson_title[side][i])


###################################
### Calendar Boxes (RIGHT page) ###
###################################

def draw_calendar_boxes():
    '''
    Draw the structure in which we will place the lesson
    information
    '''
    c.setFont("Helvetica", 12)
    date_margin = 0.9*cm
    box_height = (height-top_margin-bottom_margin)/5
    box_width = width-left_margin-right_margin-date_margin
    for i in range(0, 5):
        c.setStrokeColorRGB(0.1*i, 0.1*i, 0.1*i) # blue
        c.roundRect(left_margin+date_margin-1.5*cm, bottom_margin+box_height*i, box_width, box_height, 8)

    for i in range(1, 5):
        c.line(left_margin+i*box_width/5+date_margin-1.5*cm, bottom_margin, left_margin +
               i*box_width/5+date_margin-1.5*cm, height-top_margin) # bottom

    week_day = {0: 'M', 1: 'T', 2: 'W', 3: 'Th', 4: 'Fr'}
    for key, value in week_day.iteritems():
        c.drawString(left_margin-1.2*cm,
                 height-top_margin-box_height*key-box_height/2,
                 value)



def place_lesson_strings_on_L_canvas(canvas, monday, year_group_index,
                                     lessons_L, box_unit_height_L):
    '''
    calculates the position where strings should be placed for different
    year groups
    `year_group_index`: 0: Y8, 1: Y10, 2: Y11, 3: Y11(6)
    '''
    year_group_lessons = full_schedule_by_year[monday][year_group_index]
    for i, group_l in enumerate(year_group_lessons):
        date_string = group_l[0].strftime("%a %d")
        room_string = group_l[2].split('@')[1]
        canvas.drawString(left_margin+0.1*cm,
                          height-top_margin - 0.5*cm -
                          box_unit_height_L * \
                          (i+sum(lessons_L[0:year_group_index])),
                          date_string+' @'+room_string)

def place_lesson_strings_on_R_canvas(canvas, monday, year_group_index,
                                     lessons_R, box_unit_height_R):
    '''
    calculates the position where strings should be placed for different
    year groups
    `year_group_index`: 4: IB1, 5: IB2
    '''
    year_group_lessons = full_schedule_by_year[monday][year_group_index]
    for i, group_l in enumerate(year_group_lessons):
        date_string = group_l[0].strftime("%a %d")
        room_string = group_l[2].split('@')[1]
        # IB1 & IB2
        canvas.drawString(width/2+0.8*cm, # 0.2 for normal margin
                          height-top_margin - 0.5*cm -
                          box_unit_height_R * \
                          (i+sum(lessons_R[:year_group_index-4])),
                          date_string+' @'+room_string)
    # # LAB:
    # canvas.drawString(width/2 + 0.2*cm, 0.5*cm -
    #                   box_unit_height_R * \
    #                   (1+sum(lessons_R[3:year_group_index])),
    #                     "Lab Req.")



def add_lesson_details(canvas, full_schedule_by_year, all_weeks):
    ''' Add lesson details (date, where, which lesson) to the canvas
        input: crazy dict of dicts with lists of lists (see print_planner.py)
               (full_schedule_by_year)
        output: None (writing to canvas)
    '''
    for aweek in all_weeks:



        ###############################
        #    Common Definitions

        monday = aweek[1][0]
        friday = aweek[1][0] + td(days=4)
        week_dates_string = "%s - %s" % (monday.strftime("%d %b"), \
                                        friday.strftime("%d %b"))

        lessons_L = [len(full_schedule_by_year[monday][0]),
                     len(full_schedule_by_year[monday][1]),
                     len(full_schedule_by_year[monday][2]),
                     len(full_schedule_by_year[monday][3])]
        lessons_R = [len(full_schedule_by_year[monday][4]),
                     len(full_schedule_by_year[monday][5]),
                     1]

        # How many left-column lessons this week? Y8, Y10, Y11(1), Y11(6)
        nr_L_column_lessons = sum(lessons_L)
        nr_R_column_lessons = sum(lessons_R)


        ###############################
        #    FIRST PAGE (Calendar)

        create_header(canvas, week_dates_string, size="Small")
        draw_calendar_boxes()
        box_unit_width = (width-right_margin-left_margin)/5
        box_unit_height = (height-top_margin-bottom_margin)/5
        c.setFont("Helvetica", 10)
        for aday in cal_list:
            if aday[1].date == monday:
                if len(aday[1].all_lessons) > 0:

                    # for i, le in enumerate(aday[1].all_lessons):
                    #     c.drawString(left_margin+0.8*cm+box_unit_width*i*0.98,
                    #         height-top_margin-0.5*cm, le)

                    # Extra info: Statistics
                    if len(aday[1].stats) > 0:
                        short_stats = short_statistics(aday[1])
                        for i, ss in enumerate(short_stats):
                            if i < 3:
                                c.drawString(left_margin+1.75*inch+i*2.5*cm,
                                         height-1.5*cm, ss )
                            else:
                                c.drawString(left_margin+1.75*inch+(i-3)*2.5*cm,
                                         height-2*cm, ss )

            # lessons in each box of the weekly calendar
            for add_day in range(0, 5):
                if aday[1].date == (monday+td(days=add_day)):
                    if len(aday[1].all_lessons) > 0:
                        for i, le in enumerate(aday[1].all_lessons):
                            c.drawString(left_margin-0.2*cm+box_unit_width*i*0.93,
                                         height-top_margin-0.5*cm -
                                         box_unit_height*add_day,
                                         le)


                            # day number left of the boxes:
                            c.drawString(left_margin-1.2*cm,
                                height-top_margin-0.5*cm-box_unit_height*(add_day+0.5),
                                aday[1].date.strftime("%d"))


        c.showPage() # finish page and move to next one

        ###############################
        #    SECOND PAGE (Planning)


        create_header(canvas, week_dates_string)
        # draw_margins(c)



        if nr_L_column_lessons > 0:
            box_unit_height_L = (height-top_margin-bottom_margin)/ \
                                 nr_L_column_lessons
            c.setFont("Helvetica", 12)

            place_lesson_strings_on_L_canvas(c, monday, 0,
                                             lessons_L, box_unit_height_L)
            place_lesson_strings_on_L_canvas(c, monday, 1,
                                             lessons_L, box_unit_height_L)
            place_lesson_strings_on_L_canvas(c, monday, 2,
                                             lessons_L, box_unit_height_L)
            place_lesson_strings_on_L_canvas(c, monday, 3,
                                             lessons_L, box_unit_height_L)

            create_columns(lessons_L, 'L')
            create_columns(lessons_R, 'R')

        if nr_R_column_lessons > 0:
            box_unit_height_R = (height-top_margin-bottom_margin)/nr_R_column_lessons

            place_lesson_strings_on_R_canvas(c, monday, 4,
                                              lessons_R, box_unit_height_R)
            place_lesson_strings_on_R_canvas(c, monday, 5,
                                              lessons_R, box_unit_height_R)

        # Additional Information
        tuesday = monday + td(days=1)
        for aday in cal_list:
            if aday[1].date == tuesday:
                if aday[1].meeting:
                    c.rotate(90)
                    meeting_string = "%s meeting on %s" % \
                                     (aday[1].meeting, aday[1].date.strftime("%a %d"))
                    c.drawString(height/2, -width+1.2*cm, meeting_string) # 1.5cm for normal width
            if aday[1].date == monday:
                leave = [aday[1]._789_leave, aday[1].y10_leave,
                         aday[1].y11_leave, aday[1].ib1_leave,
                         aday[1].ib2_leave]
                if len(leave) > 0:
                    leave_dict = {0: 'Y8', 1: 'Y10', 2: 'Y11', 3: 'IB1', 4: 'IB2' }
                    whosonleave = [leave_dict[i] for i, Bool in enumerate(leave) if Bool == True]
                    if len(whosonleave) > 0:
                        leave_string = 'ON LEAVE: ' + ' - '.join(whosonleave)
                        c.drawString(height/6, -width+1.2*cm, leave_string) # 1.5cm for normal width
            c.rotate(-90)



        c.showPage()








add_lesson_details(c, full_schedule_by_year, all_weeks)




# c.rect(5*cm, cm, 10*cm, 10*cm, fill=1)
# c.rect(inch, inch, 6*inch, 9*inch, fill=1)
# make text go straight up
c.rotate(-90)
# change color
c.setFillColorRGB(0.77, 0, 0.77)
# say hello (note after rotate the y coord needs to be negative!)
# c.drawString(3*inch, -3*inch, "Hello World")
c.showPage()



# Second Page
c.setStrokeColorRGB(0.1, 0.1, 1) # blue
# draw_margins(c)

### Header ###
create_header(c, "Sept 11 - Sept 15")



c.save()

# coordinates: (x,y) (from left bottom corner)

# The  showPage  method causes the  canvas  to stop drawing on the current page
# and any further operations will draw on a subsequent page (if there are any
# further operations -- if not no new page is created).
# choose some colors
# c.setStrokeColorRGB(0.2, 0.5, 0.3)
# c.setFillColorRGB(0, 0, 0)

# # Chose size of stroke
# c.setLineWidth(1)
# c.setStrokeColorRGB(0.1, 0.1, 1) # blue

# def when_is_this_lesson(year_lesson_substring, day_data):
#     '''
#     input: string like 'Y8' or 'Y10'
#     outpt: Lesson number when it's taught or False
#     '''

#     is_lesson_taught = [L for L in day_data.all_lessons
#                         if year_lesson_substring in L]
#     if len(is_lesson_taught) == 0:
#         return False
#     else:
#         indx = [i+1 for i, L in enumerate(day_data.all_lessons)
#                 if year_lesson_substring in L][0]
#         lesson = is_lesson_taught
#         return indx, lesson


