---
layout: post
title: "Google Calendar Recurring Events on the Middle and Last Day of Every Month"
description:
headline:
date: 2016-04-29 15:51:43 -0400
category: personal
tags: [calendar,ical]
imagefeature:
mathjax:
chart:
comments: true
featured: true
---
I love my job and the company I work for but I do have one nagging problem there - a lack of direct deposit.  Instead, we get a paper check at 3pm on the 15th and last day of each month.  Unless those days fall on a weekend.  If payday would be a Saturday we get it on the Friday before and if it is on a Sunday we get it on the following Monday.  It's a real pain in the ass.  To make matters worse the paycheck is put in our mail folder in a common room and we aren't sent an email when the paycheck is put there; so you have to actively remember if it is payday or not, what time it is, and then go grab your check and carry it to the bank (or mobile deposit it if that's your style).

It really screws with me and I often forget it's payday until it's too late in the day to deposit my check (via the walk to the bank).  So I have created a couple calendar entries in Google Calendar to help me remember. The problem is Google Calendar doesn't have any native support for the paycheck rules I previously mentioned.

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
SUMMARY: Deposit Paycheck
END:VEVENT
END:VCALENDAR
```

I have to do two separate imports.  Here is the one for the last day of the month.  I based this off of a [post on Stack Overflow](http://webapps.stackexchange.com/a/17531)

```
BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART:20160331T190000Z
DTEND:20120430T191500Z
RRULE:FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1;WKST=MO;
SUMMARY: Deposit Paycheck
END:VEVENT
END:VCALENDAR
```

The end of month one doesn't go forward in time.  So if payday would be on a Sunday I still get the reminder on the preceeding Friday. I suspect I could tweak it fairly easily to get it to push the reminder to Monday by repurposing the logic in the event for the 15th.
