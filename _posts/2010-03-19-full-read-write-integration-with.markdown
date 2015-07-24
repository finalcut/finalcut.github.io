---
layout: post
title: "Full Read-Write Integration with Thunderbird and Google Calendar"
date: 2010-03-19
comments: false
categories:
 - caldav
 - lightning
 - thunderbird
 - calendar
 - google
---
For a while I've wanted to get Thunderbird working to the point where events I
accept in it are automatically written to my Google Calendar; but not my
primary Google calendar - a sub cal for work events only. Today, I think, I
achieved that goal and it was surprisingly easy.  
  
First off I am using [Thunderbird 3.0.1](http://www.mozillamessaging.com/en-
US/thunderbird/) with the [Lightning
addon](http://www.mozilla.org/projects/calendar/lightning/). As of yesterday
lightning didn't work with a newer version of Thunderbird so I haven't
upgraded yet.  
  
Before you start with the tricky stuff you need to go into Thunderbird and in
the menu select "Tools | Options | Advanced Tab" On that tab click the "config
editor" button. Once in there you can search for
"calendar.google.enableEmailInvitations" find that and make sure it is set to
true. Then close the little window.  
  
Also, if you already have a calendar of any kind in Thunderbird right click on
it and pick "properties" then set the "E-Mail" field to "None" and now the
field is set for you to tie Google Calendar seamlessly into Thunderbird.  
  
In order to accomplish this melding of two great products you need to do a
little bit of url manipulation as follows:  

  1. First use this URL as a template: https://www.google.com/calendar/dav/account@info/events  

  

  2. Then go to google calendars and pick the calendar you want to put your events on and click the 'calendar settings' option in that calendars menu
  

  3. Once on the settings screen look at the bottom at the private addresses and click on the html button (MAKE SURE YOU PICK PRIVATE)
  

  4. A little overlay will popup - copy the url that pops up and paste it in your favorite text editor (notepad perhaps)
  

  5. This part is a little tricky. Look at the url for the = sign, it will look like this: http://www.google.com/calendar/embed?src= - you want to start copying the text from the URL starting just after the equals sign until you reach a % sign. Stop copying on the last character before the % sign. That is your private authenticated read/write key to happiness  
  
  
NOTE: If you are pointing to your default calendar it will just be your gmail
email address like bob@gmail.com and you don't need to do the next step.  
  

  

  6. paste that key on another line then affix @group.calendar.google.com after it. You'll end up with something crazy looking like this: 9adfkaf9342adas2932@group.calendar.google.com (no that isn't my key; it's just a fake made up one).
  

  7. Next take that key email address you just created and replace account@info in the first url I provided you so that you get something that looks like this: https://www.google.com/calendar/dav/9adfkaf9342adas2932@group.calendar.google.com/events
  
  
At this point you've done the hard work. Now go into Thunderbird and get to
your calendar (Events and Tasks | Calendar) Then create a new calendar (File |
New | Calendar) using these initial settings:  

  * On the Network > click next
  * Select CalDav
  * In the location box paste the url you just made (https://www.google.com/calendar/dav/9adfkaf9342adas2932@group.calendar.google.com/events) and click next
  * Enter a name, pick a color
  * Select the Email Address you Want to associate with this calendar and hit next.
  *   
  
Once you're finished setting it up the calendar will pull down any events
already on the google server and it won't ask you for a login prompt to do it.
That's becuase you provided that secret key before. Don't tell anyone that key
or else they will be able to write on your calendar.  
  
NOTE: IF you used your default calendar you will actually have to provide your
gmail login info. Also note that just because someone knows your email address
they CAN NOT write on your default calendar.  
  
  
Now, in the future when you get an invitation to an event and you accept it
your google calendar will update automatically.

## Comments

Dave

I'm not able to test it until I get access to outlook somewhere. But [ this
thread ](http://www.google.com/support/forum/p/Calendar/thread?tid=120732d111b
e2e52&hl=en) (and the mozilla bug referenced therein) strongly suggests that
the spam invitation problem is not easy to fix.

Bill

I haven't noticed that problem. At least, nobody who has invited me has
mentioned that they received a new invitation to their event from me.  
  
I use it with my work calendar and so my boss would most likely have mentioned
it if I was doing something that might make us look bad.

Dave

Does this still suffer the problem that the invitation becomes a new
invitation from google calendar's viewpoint and thus re-sends invitations to
the whole list?

Bill

Yes that is exactly what it does. That's why I called it "full read-write"
integration. My instructions are tailored more for using a secondary calendar
so, if you use them with your primary google calendar, make sure you note the
special instructions for that.

Tim

Hi, not clear if this is what I'm looking for. By using lightning and
provider, I can accept invitations sent to my gmail.  
  
However, when I receive them sent to my work email address which I am reading
through IMAP, I cannot add them to my google calendar.  
  
Does your solution address that

