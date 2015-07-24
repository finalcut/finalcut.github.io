---
layout: post
title: "Mount Samba Share on MAC to a Location of Your Choice - at Login"
date: 2012-01-19
comments: false
categories:
 - bash
 - samba
 - mac
 - automator
---
One thing I've discovered in my move from Windows to MACs is that it isn't as
easy to consistently mount a windows share to a consistent location in your
file system. Initially I wasn't even sure if it was possible. The built in GUI
doesn't really give you an option. For instance if you are mounting the
following two shares : smb://server1/d$ and smb://server2/d$ it is possible
that one will end up at /Volumes/d$ and the other will end up at /Volumes/d-1$
or something like that.  
  
 The problem is it isn't easy to tell by looking which one is server1 and
which one is server 2's mount point. Thus, if you mount them in an
inconsistent order server1 could end up at /Volumes/d$ once and then
/Volumes/d-1$ the next time. It's not an ideal situation.  
  
 Now you may already be asking - who cares? If you setup an automator script
with you login things will always be mounted in the same order and be at the
same volume location and you'll just get used to knowing where things are.
True. However, I work on a team and one of the things I also want to be able
to do is have an ant script that can reliably run on each person's machine
that can access these various samba shares (imagine one click deployment to a
samba share?) Thus I need a way to consistently have all this stuff in a place
that does two things:  
  

  1. Be a nice human readable location on the file system so you instantly know what should be there
  2. Is the same on everyones machine and exists in an easy to recreate way for new members of the team.

Thus I am using an automator task that uses both an applescript and a bash
script to achieve my result.  The apple script part is used to request the
users login password for the windows domain which is then used in the bash
script when mounting the samba shares.  
  

So here is the apple script part:  
```js on run {input, parameters}  
tell application "System Events"  
set the_password to "password"  
display dialog "Please enter your Windows password: " default answer ""
buttons {"OK", "Cancel"} default button "OK" with icon 2 with title "Password"
with hidden answer  
set the_password to text returned of the result  
end tell  
return {the_password}  
end run  
  
```

I stole that bit from [Aric Friesen](http://aricsblog.blogspot.com/2006/09
/running-shell-commands-with-automator.html). I removed a bunch of his script
but the basic core part of it remains unchanged. In my automator task the
second step is to "Run Shell Script" were you Pass Input as arguments. Here is
my bash script (it calls PHP to url encode the password to make sure no
special characters like @ are in there which would break the samba call):  
  

```js #!/bin/bash  
  
pwd=$(php -r "echo rawurlencode('$1');")  
if [ ! -d ~/windows ]; then  
mkdir ~/windows  
fi  
if [ ! -d ~/windows/server1-d ]; then  
mkdir ~/windows/server1-d  
else  
umount ~/windows/server1-d  
fi  
if [ ! -d ~/windows/server2-d ]; then  
mkdir ~/windows/server2-d  
else  
umount ~/windows/server2-d  
fi  
  
  
mount_smbfs "//DOMAIN;USERNAME:$pwd@SERVER1/d$" ~/windows/server1-d  
mount_smbfs "//DOMAIN;USERNAME:$pwd@SERVER2/d$" ~/windows/server2-d  
  
```

There may seem like some extraneous fluff in there but I want to make sure it
works no matter if the drives have ever been mounted before. It turns out to
mount a drive to a predetermined location you have to have a directory created
at that location already. The mount_smbfs command will then change that
directory into a mount point. Thus I have some checks to make sure my
directories already exist and that the mounts haven't already happened before
I try to mount to them. I would prefer if I could tell that the directory were
actually already being used as a mount point (so I could skip mounting it) but
I couldn't find a reliable way to identify if a directory was a mount point
and what it was actually pointing to.  
  
Once I had this automator process setup I saved it as an application called
"MountNetworkDrives".  From there you can make it execute on login by
following these simple steps:  
  
  

  1. Open System Preferences
  2. Click on Users &amp; Groups
  3. Using the "Current User" select "Login Items"
  4. Click on the small "+" at the bottom of the right panel
  5. Find your new application "MountNetworkDrives" and add it

And Voila!  You have created a consistent way to setup mounts on your mac.
Now you can share that automator script with your teammates.  Just have them
change the username value in the bash script step and it is good to go.

