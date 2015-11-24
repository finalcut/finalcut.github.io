---
layout: post
title: "Tasker: Fall to Sleep to Music"
date: 2013-08-29 20:35
comments: true
category: android
tags: [tasker]
---
Lately I've gotten in the habit of listening to music via some bluetooth speakers before I fall asleep.  I setup a very simple tasker profile that would turn the music off at a certain time but, really, that isn't sufficient.

I don't always go to bed at the same time and thus I don't always want the music to turn off at the same time.  Basically, I want the music to turn off thirty minutes after I get in bed.  So, how can I get tasker to do that?

I'm pretty sure this is the last update I'm going to provide for this.  I've settled on a single profile that starts when you launch the music app of your choice.  The task that it fires off waits to do anything else until it is after 9:45pm.  At which point it sets the future shut off time of 30 minutes.  Thus, if i start my music every night before 9:45 my shut off time will always be around 10:15pm.  The task then waits until that future time is passed then it shuts off the music app.

2. create a task called "Sleep to Music"
	1. Create an Action to determine if it is late enough at night to do auto turn off the music.
		1. pick "task"
		2. pick "if"
		3. set the left side of the condition to %TIMES
		4. set the operator to maths: greater than
		5. set the right side of the condition to 21.59 for 9:59pm.  It uses military time with a decimal instead of colons to represent time.
		6. finish
	2. Create an Action to determine if the music app is turned on.
		1. pick "task"
		2. pick "if"
		3. set the left side to %PlayMusicOn
		4. set the operator to maths: equals
		5. set the right side to 1
		6. finish
	3. Create an Action to define the 30 minute threshold
		1. pick "variables"
		2. pick "variables set"
		3. set name to "%ShutOffMusicTime"
		4. set to as %TIMES + (60*30)  -- 60 seconds, 30 minutes.. %TIMES is the number of seconds since some date in 1970 so we are computing 30 minutes worth of seconds beyond the current moment.
		5. check "Do Maths"
		6. finish
	4. Create an Action that will occassionally poll to see if the 30 minute threshold has been reached.
		1. pick "task"
		2. pick "wait"
		3. set the "seconds" to 10
		4. set the until (at the very bottom) values
			1. left side to %ShutOffMusicTime
			2. operator to maths: less than
			3. right side to %TIMES
		5. finish
	5. Create an Action to kill the music app
		1. pick "app"
		2. pick "kill app"
		3. pick your music app
		4. finish
	6. Create an Action to reset the 30 minute treshold
		1. pick "variables"
		2. pick "variables set"
		3. set name to "%ShutOffMusicTime"
		4. set to as 999999999 which represents some impossible time in the future..
		5. finish
	6. Create an Action to reset the music playing flat
		1. pick "variables"
		2. pick "variables set"
		3. set name to "%PlayMusicOn"
		4. set to 0 (zero) which indicates the music app isn't running
		5. finish
	7. Create an Action to close out the first IF check
		1. pick "task"
		2. pick "End If"
		3. finish
	8. Create an Action to close out the second IF check
		1. pick "task"
		2. pick "End If"
		3. finish
3. Create a new Profile
	1. pick "App"
	2. pick "your music app"
	5. Attach the "Start Music App" task
4. Create a new Profile
	1. Select "Event"
	2. Select "Display"
	3. Select "Display Off"
	4. Attach the "Sleep to Music" task

Bada Bing, Bada Boom - the two tasks will work in harmony to turn off your music when you want it to.  Customize it for your needs and hopefully you'll fall asleep o the soothing sounds of your favorite music without worrying about it waking you up during the night.

This is the third version of this - the prior two wouldn't work when the screen turned off and the phone went to sleep.  Hopefully you'll have good success converting this for your needs.
