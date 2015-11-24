---
layout: post
title: "Android: Turn of Lock Screen When Using Certain Apps with Tasker"
date: 2013-07-11
comments: false
category: android
tags: [tasker,endomondo,easy-scorecard-pro,discgolf,screen-lock]
---
Recently I've been running a lot and when running I use Endomondo to track my
time/distance details.  However, it's kind of a pain to grab my phone, unlock
it, and then hit the pause/stop button at the end of an exhausting run.  I
seem to just end up adding 15 seconds to my overall time as I fidget with my
phone.  

Yeah, I know, first world problem.  

I also play a lot of disc golf.  I use Easy Score Card pro to track our scores
on each hole.  The course we mostly play is 19 holes long so I am unlocking
the phone 19 times during the round while walking on less than smooth terrain.
It's a bit of a pain.  

Yep, another first world problem.  

Anyway, I decided to make my life easier by creating a simple Tasker Profile
that will turn off my screen lock when either of those two applications are
running.  I call it "Screen Lock Off" and here is how I created it.  

NOTE: you have to have the secure settings helper installed to get this to
work.  



  1. In Tasker, first thing to do is create a "Task" callled "Turn off Lockscreen"
  2. Add action -> Select "PLUGIN"
  3. Select "Secure Settings"
  4. A fairly unhelpful screen appears.  Click "Edit" in the configuration box.
  5. Scroll down to Password/Pin and select it
  6. Select "Enter Password once before unlocking"
  7. Make sure the "Enabled/Disabled" button says "Disabled"
  8. Touch the "diskette" icon to save the configuration
  9. You're now back at the unhelpful screen but it should also say "Clear Password/Wait for Unlock"
  10. Touch the "back arrow" to go back to the tasks screen.

Now we need to create a second task to turn the lock screen back on.

  1. Repeat steps 1-6 from before but name this one "Turn on Lockscreen"
  2. Make sure the "Enabled/Disabled" button says "Enabled"
  3. Pick either Pin or Password
  4. Enter the Pin/Password you want your lockscreen to use
  5. Confirm your Pin/Password
  6. Repeat steps 8-10 above.

Now that both tasks are created to go the Profiles tab and we'll create the
profile.

  1. Click the "+" to create a new profile
  2. Pick "Application"
  3. select any applications you want to fire off the "Turn off Lockscreen" task
  4. After you've selected some apps, click the back arrow in the top left of the screen
  5. When prompted pick the "Turn off Lockscreen" task
  6. The profile now exists
  7. Long press on the profile to put it in edit mode.
  8. Long press on the "Turn off lockscreen" task under the profile
  9. Select "Add Exit Task"
  10. Select the "Turn on Lockscreen" task

That's it - you're done.  



NOTE: Each time you update your ROM you'll have to reinstall the secure
settings helper plugin .. You can do that easily from within the secure
settings app that remains installed.
