---
layout: post
title: "Western Digital Passport: Access Denied on Second Computer"
date: 2009-04-29
comments: false
categories:
 - passport
 - windows-xp
 - access-denied
 - windows-vista
---
My friend Mike recently bought a nice black Western Digital Passport. It's a
slick little portable harddrive the problem was it wasn't very portable. Sure
he could carry it around, but if he plugged it into a computer other than his
it was inaccessible; if you tried to open or explore it gave an "Access
Denied" error.  
  
WTF?  
  
Well, it ended up being a fairly simple fix. He updated the permissions on the
drive to include the "Everyone" group. For some reason when he first formatted
it (NTFS) the only groups that had permission to the drive were his account,
"SYSTEM", and "CREATOR OWNER" - but by adding "Everyone" it now works on other
windows machines.  
  
So if you're having a problem getting your Passport to work on multiple
computers, put it back on the original machine and make sure "Everyone" has
"Full Control" access to the drive.  
  
Open "My Computer", right click and pick "Properties" in the context menu.
Then select the "Security" tab. Once that is up, click the "Add" button, enter
"Everyone" in the field provided, hit "Apply" then "OK".. and voila' you'll be
good to go.

## Comments

Bill Rawlinson

I'm really not sure what your options are if you don't have the original
computer anymore. Sorry

Anonymous

I no longer have access to my old laptop which I used with the WD passport
initially, it packed in, but I have taken the hard drive out and have an
upgrade kit, in order to plug it into another laptop so I can at least access
files, but the WD passport is not working on the new laptop, I get the error
message when I try to access folder on it. Any suggestions for this situation.
I am not very tech savvy, so need walked through the processes!

Robert

cheese and rice I have no idea how to thank you. I somehow got primary access
rights to my drive assigned to one of my friend's computers, who i won't see
for like a year and was freaking out that nothing I did allowed me to open my
own hard drive but this worked. thanks!

Steven K

Thanks A Million I have been searching for hour how to fix and never occured
to me to check the security groups on the ntfs permissions list. Thanks

