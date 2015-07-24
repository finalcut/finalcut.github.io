---
layout: post
title: "Remove Ubunutu Dual Boot with Windows 7"
date: 2012-03-14
comments: false
---
My linux luck continued with a failure in getting Ubuntu 11.10 to work
properly right out of the box so I decided to uninstall it.  However, removing
it isn't nearly as simple as installing it was.  Here are the steps you need:  
  
  

  1. You need to remove the linux partition(s) - I used the free tool [EASUS Partition Master](http://www.partition-tool.com/personal.htm), removed all of the non windows and non-recovery partitions, and then stretched out my windows partition to reclaim that space.
  2. After you setup the new partition rules your computer has to reboot.  After the bios screen the unix boot loader Grub will still appear offering to start linux or windows.  Start windows but then hit f8 to get to the recovery menu for windows.
  3. Pick to start windows in recovery mode; a graphical user interface will open.  Eventually you'll have the chance to pick from a small menu of about eight options, pick the "Command Line" option (or console).
  4. At the command line enter "bootrec /fixmbr" without the quotes. This will get rid of grub.  It's almost instantaneous. 
  5. Restart your computer; EASUS Partition Master will then do it's partition resizing foo.  This isn't instantaneous so just have some patience.
  6. You're done. 

  

