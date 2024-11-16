---
layout: post
title: "Ubuntu Auto Shutdown Due To High CPU Temp"
date: 2008-11-03
comments: false
categories:
 - acpi
 - critical trip point
 - unsafe temperature
 - linux
 - ubuntu
---
I use a Dell XPS m170 laptop at work. I have it dual booting into either XP or
Ubuntu 8.1 (Ibex); however, while in Ubuntu at times the CPU temp gets really
hot and the system automatically shuts down. This would be fine if it were a
rare event but it happens pretty frequently and it is entirely annoying. The
syslog showed the following error:





```sh
ACPI: Critical trip point

Critical temperature reached (100 C), shutting down.


```




I know it is a safety feature, but really, I can't afford to keep having the system shutdown because a page on Firefox is intensive to load.  My fans are working but for whatever reason my CPU temp exceeds the critical threshold of 99C.  On some systems you can see what your threshold is within the BIOS and even edit it but not on this one.  So what's a frustrated developer supposed to do?  Well, it turns out you can tell you system to ignore the high temp threshold and to just keep on chugging along.  NOTE: This isn't the best advice I ever gave, if you do this then fry your CPU don't come bitching to me.


First you need to add a setting to you're system by following these instructions:



```sh

 _{in a terminal enter:}_ gksudo gedit /etc/modprobe.d/options

 _{add this line to the end of the file}_ options thermal nocrt=1

 _{save and close the file}_


```




Once you have this option set you need to reconfigure the kernel to pick up these changes, in a terminal window again enter the following:





```sh
 sudo dpkg-reconfigure linux-image-$(uname -r)


```




This will update your kernel and then tell you to restart when it is done.  Once you restart you can go back to a terminal window and type:




```sh
 cat /proc/acpi/thermal_zone/*/*


 _{gives you a result similar to this}_


 <setting not supported>

 <polling disabled>

 state:                   ok

 temperature:             52 C

 critical (S5):           99 C <disabled>


```




Now your system won't restart when the critical heat point is passed.  Again, don't blame me if you hurt your machine by doing this.




