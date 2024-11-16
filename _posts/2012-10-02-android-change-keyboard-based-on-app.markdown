---
layout: post
title: "Android: Change Keyboard Based on App Using Tasker"
date: 2012-10-02
comments: false
category: android
tags: [tasker,keyboard,lastpass,swype]
---
Today I discovered that my password manager, LastPass, comes with it's own
keyboard to make it easier to fill out forms with your username and password.
The thing is, the majority of the time, I still want to use Swype but I'm too
lazy to toggle my keyboards.  In fact, there is only one app where I always
want the LastPass keyboard and that's my banking app.  The banking app won't
let me past into the login fields but the LastPass keyboard can auto fill the
forms for me.  

Well, fortunately, Tasker has come to the rescue yet again.  Note, however,
that you need a rooted device to do this stuff.  I am not going to take the
time right now to explain how to root your device sorry.  Instead I'll assume
you've rooted and you own [Tasker][tasker].  

After installing Tasker you will also need a plugin called [Secure Settings][secureSettings].  You can get it at the play store.  Ok,
before you jump into tasker first start up Secure Settings, switch to the
Helper Tab, and install the helper.  You can't do anything without the Helper;
it is what gives you access to the command to change the keyboard.  

Ok, now that your prerequisites are setup launch Tasker and do the following:  



  1. Create a new profile; I called mine "LastPass"
  2. Select the "Application" context
  3. Pick the app you want to use the special keyboard in.  I picked my banking app.
  4. Select "New Task"  I called mine "Start LastPass"
  5. Add an action; select "Plugin"
  6. Pick "Secure Settings"
  7. Edit the configuration by selecting the "Edit" button
  8. Scroll down a bit and find the "Helper Actions" section
  9. Pick the "Input Method" Helper Action.
  10. Select your special case keyboard; I picked "LastPass"
  11. Click the save icon which looks like an old school 3.5" disk in the bottom left corner.
  12. Leave the "IF" checkbox empty
  13. Click on the green checkmark or confirmation button
  14. Click on the green checkmark or confirmation button again.
  15. At this point you have a profile that has a Start Task that will start your keyboard; now you need to setup an Exit task to switch back to your normal keyboard.
  16. Long press on the start task (Start LastPass) and a menu will appear.
  17. Choose "Add Exit Task"
  18. Follow steps 4-14 but this time call your task "Start " where favorite keyboard is your favorite.  I called mine "Start Swype"
  19. Once you finish with step 14 again you'll see you have a start and exit task setup.  Close tasker.
  20. Go to your special app and launch it; see if the right keyboard is setup.
  21. Exit the app, launch any different app and make sure your normal keyboard is back.

That's it.  You're done.  Congratulations.  

These instructions are based on the set of instructions I found at [grokbase] and in the [google groups for tasker][googleGroup]


[tasker]: https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm
[secureSettings]: https://play.google.com/store/apps/details?id=com.intangibleobject.securesettings.plugin
[grokbase]: http://grokbase.com/t/gg/tasker/1292geqd8g/change-of-input-method-
keyboard-with-tasker-and-plugin-secure-settings
[googleGroup]: https://groups.google.com/forum/?fromgroups=#!topic/tasker/mAco_fbmh2c

## Comments

Anonymous

Thank you for this! This was exactly what I needed  
Great instructions and well thought out.  

**to any noobs trying this, play around with the start and end tasks if you're switching keyboards between apps.   
My quick paced setup (first try made the transition between keyboards VERY
slow. This current set up doesn't hesitate, like its changed before the app
keyboard even shows up.  
not gonna include app names, just settings and keyboards.  

MMS pop up app- Start task- Kii keyboard, End task Samsung Keyboard  

MMS stock app- Start Samsung Keyboard, End task Samsung keyboard.
