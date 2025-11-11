---
firstprop: first
layout: post-with-discussion
title: Google Calendar Recurring Events on the Middle and Last Workday Days of Every Month
category: utility
tags:
  - calendar
  - ical
  - events
description: How I used ical standard to create recurring events on my google calendar.
blueskyPostURL: https://bsky.app/profile/rawlinson.us/post/3m5f3twnxjn2w
---
Why I needed this isn't important.  This isn't a cooking blog where you need a backstory!

I have created a couple calendar entries in Google Calendar to help me remember to do things 2 times a month as the title of this post suggests. The problem is Google Calendar doesn't have any native support for these rules.

Fortunately, there is a workaround.  You have to create an ical file then import it into Google Calendar via "Settings->Calendars->Import Calendar".

Here is the calendar definition for the mid-month paycheck reminder thanks to a [post on a Google forum](https://productforums.google.com/d/msg/calendar/FQfiYgLkeco/3kZB1tPcIVkJ):

```
BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20160315T190000Z
DTEND:20120415T191500Z
RRULE:FREQ=MONTHLY;BYDAY=FR;BYMONTHDAY=14
RRULE:FREQ=MONTHLY;BYDAY=MO;BYMONTHDAY=16
RRULE:FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYMONTHDAY=15
SUMMARY: WHATEVER YOUR RECURRING EVENT NAME IS; Change Me!
END:VEVENT
END:VCALENDAR
```

I have to do two separate imports.  Here is the one for the last day weekday of the month.  I based this off of a [post on Stack Overflow](http://webapps.stackexchange.com/a/17531)

```
BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20160331T190000Z
DTEND:20120430T191500Z
RRULE:FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1;WKST=MO;
SUMMARY: WHATEVER YOUR RECURRING EVENT NAME IS; Change Me!
END:VEVENT
END:VCALENDAR
```
