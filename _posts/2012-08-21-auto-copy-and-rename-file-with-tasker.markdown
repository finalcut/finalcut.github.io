---
layout: post
title: "Auto Copy and Rename a File With Tasker on Android"
date: 2012-08-21
comments: false
categories:
 - easy-scorecard-pro
 - tasker
 - copy-file
 - disc-golf
 - android
---
I play disc golf quite a bit and I use a great app, Easy Scorecard Pro, to
keep my score each round.  However, it has a glaring problem that the
developer won't rectify - I can't share the generated scorecard directly to
Google+ from within the app.  I can share it to facebook but not G+ because,
for whatever reason, G+ will only let you share images that are in your
gallery and therefore the image is not attached to my G+ post from within the
app.  That kind of sucks.

Today I came up with a workaround.  It still is kind of clunky but it is a
hell of a lot better than going through ES File Explorer and renaming the
scorecard.png to something unique and then copying the image to my gallery.
Then I had to switch to the G+ app and then I could post it to my disc golf
circle.

Instead I'm using Tasker to take care of the grunt work and now I just opent
he G+ app and post to my circle.  Here are the basic steps:



  1. Create a new profile - I called mine "Scorecard"
  2. Add an event to watch for.  I'm watching for a file to be modified

* select the file at data/com.mydroidsoft.easyscorecard/scorecard.png
  3. Create a new task - I called mine "Copy to Gallery"
  4. Pick action "Copy File"

* In the from field put data/com.mydroidsoft.easyscorecard/scorecard.png

* In the to field put DCIM/Camera/scorecard%DATE%TIME.png

That's it.  Just make sure your "Scorecard" profile is active and then, when
you next go into Easy Scorecard Pro and create a scorecard image to share (I
share to facebook) the scorecard.png will be modified at which point it will
be copied to your gallery.  Then, after posting it to facebook you can launch
the G+ app and post the image from the listing - it will be the first image
shown.

At first I didn't realize I could add the name of the file into the "To" field
so I was happy to see that it worked as I needed it to.

