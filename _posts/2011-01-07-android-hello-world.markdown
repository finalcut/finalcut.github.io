---
layout: post
title: "Android - Hello World"
date: 2011-01-07
comments: false
categories:
 - android
---
Yesterday I downloaded and installed Eclipse and the Android SDK. I then tried
to run the simple [Hello
Android](http://developer.android.com/resources/tutorials/hello-world.html)
program that is on the developer.android.com site. The code compiled but the
application wouldn't deploy to the emulator properly. Instead I got some weird
errors as follows:




```
[2011-01-07 12:47:04 - HelloAndroid] Failed to install HelloAndroid.apk on device 'emulator-5554!

[2011-01-07 12:47:04 - HelloAndroid] (null)

[2011-01-07 12:47:05 - HelloAndroid] Launch canceled!


```



It was pretty annoying because no matter how much I searched online and found other people with similar problems I couldn't seem to get the damn app to work on the emulator.  To make matters worse the Emulator takes FOREVER to start.  I was almost ready to give up before I began considering how annoying of a time I was having with something as simple as Hello World.


Eventually I found a post at Stack Overflow that mentioned that I shouldn't launch the emulator from within Eclipse.  Instead I should create a batch file with the following contents and start the emulator with it.




```sh
emulator.exe -cpu-delay 0 -no-boot-anim -avd my_avd


```



I made the batch file and the emulator did start MUCH faster (still slow) but, sadly, the app still wouldn't deploy to the emulator properly and I kept getting the same errors.  I saw a bunch of suggestions that I look in the "logcat" but, of course, the tutorials I'd gone through didn't mention how to do that anywhere and none of the posts suggesting it gave the steps to do that either but eventually I found those too.   Here's how you view the logcat in Eclipse:




  1. In Eclipse go to the Window Menu

  2. Show View

  3. Other

  4. Expand Android

  5. Select LogCat


Unfortunately the logcat info was useless and I wasn't seeing anything that would explain why I was still getting my errors.  Then, I found a post that was tangentially related to my problem but where someone was seeing an error that mentioned something about a lack of memory or space or something.  I don't really remember.  However, the advice given to fix that problem also fixed mine.  I had to modify my batch file to include the -partition-size directive.  The advice suggested 514 as the value to use but I decided to use 1028 instead.  So now my batch file for starting the emulator looks like this:



```sh

emulator.exe -cpu-delay 0 -partition-size 1028 -no-boot-anim -avd my_avd


```



This final batch file fixed everything and I was good to go.  Hope it helps some others get going.





## Comments











Anonymous






I have the same problem, and I am new to this as well. It would be very helpful if you could let us know how to modify the batch file.











Anonymous






This shows a lack of documentation and obscurity. I am frustrated at not being able to run even a "Hello, World" app in a reasonable amount of time.


Your suggested solution just launches the emulator eventually and does not load the app.


I am using the latest SDK for Windows on November 25, 2011. It does not have options -no-boot and -anim.











Anonymous






Great article!


Sorry, kind of a newb. How do you modify/execute the batch file? I'm having the same issue.











Anonymous






Thanks a lot!! I had the same problem. This was the only solution that worked for me











Jake Munson






Assuming you have an Android phone, you should consider developing with that.  Your app will boot a LOT faster on your phone than in the emulator.  I would just use the emulator to test different versions of Android.











Anonymous






THANK YOU!!!











Anonymous






THANK YOU!!!!


-Mike










