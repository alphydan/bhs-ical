
// If you need to delete a series of events on the calendar
// go to https://script.google.com and copy the script below
// Changing the appropriate  sections

function delete_events()
{
  //take care: Date function starts at 0 for the month (January=0)
  var fromDate = new Date(2015,7,14,0,0,0); //This is August 1, 2014
  var toDate = new Date(2016,6,30,0,0,0);   //This is March 1, 2016 at 00h00'00"
  var calendarName = '_your_calendar_name'; // often your gmail email

// Comment or Un-comment the strings or sub-strings you want to delete
  var toRemove = 'IB1 Phys @26';
  var toRemove = '9A Sc @CL';
  var toRemove = 'IB2 D.tech @IB2';
  var toRemove = 'IB2 D.tech @PL';
  var toRemove = 'IB1 Phys @PL';
  // var toRemove = 'Lunch Duties @IBCR';
  // var toRemove = 'Y10 Phys 1 @38';
  // var toRemove = '9A Sc @PL';
  // var toRemove = '[day 1]';
  // var toRemove = '[day 2]';
  // var toRemove = '[day 3]';
  // var toRemove = '[day 4]';
  // var toRemove = '[day 5]';
  // var toRemove = '[day 6]';
  var toRemove = 'IB2 D.tech';
  var toRemove = 'Y10 Phys';





  var calendar = CalendarApp.getCalendarsByName(calendarName)[0];
  var events = calendar.getEvents(fromDate, toDate,{search: toRemove});
  for(var i=0; i<events.length;i++)
  {
    var ev = events[i];
    if(ev.getTitle()==toRemove) //check if the title matches
    {
      Logger.log('Item '+ev.getTitle()+' found on '+ev.getStartTime()); // show event name and date in log
      // ev.deleteEvent(); //uncomment this line to actually do the delete !
    }
    str = ev.getTitle()
    if (str.indexOf(toRemove) > -1) { // check if string is inside
      Logger.log('item '+ toRemove + ' found in ' + str);
      // ev.deleteEvent();  // uncomment this line to delete events containing the sub-string
    }

  }
}
