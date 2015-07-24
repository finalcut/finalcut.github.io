---
layout: post
title: "Rollback from Mountain Lion to Lion"
date: 2012-02-27
comments: false
categories:
 - macports
 - xcode
 - mac
 - mountain-lion
 - lion
---
**Disclaimer: Before you do this; if it doesn't work you can't blame me.  It worked OK for me but maybe I was just lucky.**  
  
Ok, with that out of the way here's the lowdown.  I installed the developer
preview of Mac OS X Mountain Lion and immediately started to notice some
things that I really needed wouldn't work anymore.  No parallels, macports had
issues and couldn't compile things with XCode 4.4 (what is required for Mt
Lion), and quite a bit more dealing with things that depended on macports or
the compiler within xcode.  
  
So what did I do?  I tried to be creative and everything failed.  
  
Oh, and I didn't have a time machine snapshot of my system before the upgrade.
Anyway, I eventually went to google to find some solutions and found this
posting explaining how to [install uninstall Mountain
Lion](http://kurrytran.blogspot.com/2012/02/how-to-uninstall-mountain-lion-
os-x.html) except it doesn't show you how to uninstall Mountain Lion at all;
it just shows you how to install Lion on another partition.  It does, however,
have the key to the castle so to speak and I'll get into that in a little bit.  
  
Before you can install Lion you need a copy of Lion.  Makes sense right?  Well
I didn't have a copy but the aforementioned post told me I could get it using
my apple dev center account but then it said I couldn't because I was running
mountain lion and that I'd need to get it another way.  Well damn.  
  
Later in the article he said you have to fool the system to let you install
lion on the other partition by changing the version number of Mountain Lion.
I thought, well, what if I just do that now so I can get a copy of Lion and
BAM! it worked.  So here are the basic steps.  
  

  1.  I use sublime as my text editor and I have a command alias to launch sublime using the word sublime from the terminal..  
_$ sublime /System/Library/CoreServices/SystemVersion.plist_

  2. _It will ask you for your password; enter it then change the two version instances from 10.8 to 10.7_
  3. _Save the file; you'll be asked for your password again; enter it._
  4. _Now download Lion.  If you don't have an dev center account I guess you can pay the $30._
  5. _wait a while.  Lion is big and it takes a long time to download.  It kind of freaked me out because it showed it going into my "Applications" at first but then it felt like nothing was happening.  Have some patience; go read reddit for a while._
  6. _Eventually the download will finish and the Lion installer will open automatically.  Notice, nowhere in this list did I tell you to make a new partition.  Screw that step!_
  7. _Install right over mountain lion.  Just pick the partition you normally have things on and GO._
  8. _**WAIT WAIT.. finish reading this before you go...IT'S REALLY IMPORTANT**_
  9. When the install is done your machine will reboot and prompt you to login but you won't be able to. [ Lion hates your old passwords and gets rid of them all](http://www.gibni.com/cant-login-after-os-x-lion-install-solved) \- you can't login yet.  Just reboot again and wait for the screen to go completely black then hold down  cmd+r 
  10. HOLD THEM DOWN; don't just press and release.  HOLD THEM BOTH until a window opens called "Utilities"
  11. In the main menu bar there is a services option, click on it and find terminal.  If it isn't services just look in each menu until you find terminal; open terminal
  12. in the terminal window type "resetpassword" without the quotes and hit enter
  13. A new windows opens and it shows you all of your old accounts.  Find yours and reset your password.
  14. While you're at it reset the administrator password.
  15. Once your down with that close all the windows then in the system menu pick restart
  16. This time you don't have to hold down any keys.
  17. Eventually the login screen will pop up; login as yourself
  18. Now go to the system menu and install any updates so you're nice and secure.

That worked for me (I also reinstalled xcode 4.3 from the app store after
that).

  
Good luck

  
\-------  
Some additional notes:  
  

  1. After you re-install XCode 4.3; go to preferences, downloads, and install the command line tools
  2. I also reinstalled macports to be on the safe side
  3. parallels still doesn't work for me after the rollback.. I will reinstall parallels and hope for the best **UPDATE:** uninstall and reinstall fixed it.
  4. because of some changes to mail; rolling back left me with a broken mail app; not a deal breaker as I can just use outlook as we get our mail from an exchange server at the office.
  5. **UPDATE**: you can't use the systems preferences panel for setting desktop backgrounds after doing this.  You can still set your primary monitor background using the "right click, services menu" on the image you wan to make your wallpaper.

## Comments

Yar Oo

Sir, I am from Myanmar, your help me with great deal and you also a great mac
man! thanks

Anonymous

I walked through this solution with a senior apple advisor and it worked. I
did not restore with time machine however. Instead I deleted the
/System/Library/PrivateFrameworks/iLifeMediaBrowser.framework  
folder and then restarted the computer. And then did software update. Software
update found that I needed "iLife support". After updating the folder was
replaced and boom!: mail.app opens.

teethblast!

I walked through this solution with a senior apple advisor and it worked. I
did not restore with time machine however. Instead I deleted the
/System/Library/PrivateFrameworks/iLifeMediaBrowser.framework  
folder and then restarted the computer. And then did software update. Software
update found that I needed "iLife support". After updating the folder was
replaced and boom!: mail.app opens.

Bill Rawlinson

Yes, the rollback doesn't leave everything working as you might hope.  
  
Mail also will fail to work.  
  
Also, after re-upgrading to Mt. Lion final certain things just didn't work
quite right. Thus, when I decided to settle on using the final version of Mt
Lion I did a clean install.  
  
The rollback worked well enough - but if you absolutely must use some of those
apps Apple wasn't lying when they said you can't rollback.

Garrett

Worked for me, but I am unable to use iPhoto, Logic 9.1.7 ect. Crashes on
startup with a similar error message for both.

Bill Rawlinson

Had I shown sufficient foresight and created a time machine backup of lion in
the first place I wouldn't have had to deal with any of these problems most
likely - I probably could have just restored to that backup.

Bren Munroe

Out of curriousity:  
  
Could you follow each of these steps, then make a new Time Machine backup of
Lion to aide in making a proper clean-install that would fix all of the small
kinks in the system?  
  
A little extra work, but could still help in fixing the issue. Though I guess
it somewhat kills the point.

Anonymous

For the mail issue, does anyone have a way i can get a copy of the
privateframeworks folder that i can get ahold of?

Anonymous

Thanks a bunch man!  
This saved me a lot of trouble.  
I was too curious too think about all the implications of this preview. While
I've got everything to work, coding was not possible anymore.mu

Anonymous

Thanks a lot! I'm really surprised how easy your method is, after having spent
a lot of time looking for this. I was just desperate. I wonder why this is not
known by every Mac user :)  
You're great man. Things are easier thanks to guys like you. Thanks again.

Bill Rawlinson

Scott, glad it helped. I don't have a donate button as none is necessary but
if you insist I have a paypal account bill@doxie.org :O)

Scott

WOW. Where is the donate button? You just saved me hours and hours and hours
and so much lost productivity... I just successfully downgraded from Mountain
Lion Preview 2 to Lion 10.7.3. I don't have sublime and I didn't know my su
password, so I changed the permissions of SystemVersion.plist in Finder so
everyone could read/write it, then used emacs from Terminal (for some reason
TextEdit still wouldn't let me save the file).  
  
THANK YOU!!!

Anonymous

Thanks. Worked well.  
  
I managed to fix the Mail issue by copying  
  
/System/Library/PrivateFrameworks/iLifeMediaBrowser.framework  
  
from a different Lion machine. The installer probably doesn't update it and
leaves the ML version.  
  
Drew

Daniel

is there any way to fix the mail app?

Chaitan Roa

Worked like a charm, many thanks

Anonymous

Hi,  
parallels works fine if you move "Parallel Service" from "Non-compatible apps"
to "Parallels" folder.  
After that, restart your mac.  
  
thanks for the guide

