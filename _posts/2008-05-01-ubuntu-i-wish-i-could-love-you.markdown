---
layout: post
title: "Ubuntu I wish I could Love You"
date: 2008-05-01
comments: false
categories:
 - lotus notes
 - citrix
 - ubuntu
---
I am trying hard to get things just right on my Ubuntu install and it is
getting close. I could not recommend it to my non computer savy family members
as their default OS - but it is getting close to where I can use it all the
time.  
  
Today I had to get past a few different issues:  

  

  1. [Lotus Notes 8.01 install](http://www-10.lotus.com/ldd/nd8forum.nsf/7756aedc25e6d81285256324005ac76c/f683185b98129dd7852572ea001db523?OpenDocument). Please save your notes flames for another blog. I am not a fan of notes but it is what we use so I get in line lock-step. The install process is fairly smooth however getting Notes to actually work after you install it is not. The following steps assume you already have the tar file downloaded and extracted to some directory.  

    * Open a Terminal Window and move to the directory you extracted the tar too.
  

    * sudo ./setup.sh : You need the sudo or it won't let you install
  

    * Just go through the setup instructions.. this part is pretty straight forward
  

    * Once the install is done...  
  
sudo chmod 755 -R /etc/lotus  
  
sudo chmod 755 -R /opt/ibm/lotus/notes/

  

    * The install also created a lotus directory in your home directory - GET RID OF IT; it's whacked. When you first start Notes it will recreate the directory and this time do it properly.
  

    * Start Notes and follow the setup wizard.
  
  

  

  2. Citrix Client Full Screen - I needed the Remote Desktop Client (RDC) to work across both of my screens while in full screen mode. I use an NVidia card so to get this to work I had to   

    * install the NVidia settings manager (launch it as root)
  

    * change to "separate X screens"
  

    * enable Xinerama
  
  
This has the effect of disabling compiz fusion but I don't care much about
that; it's just fluff after all. I also couldn't have a panel bar on the top
of either of my monitors (or else my mouse in the Remote Desktop Client) is
offset and is fairly useless. After I restarted the RDC worked fine.

  

  3. [Volume Control Didn't Work](http://ubuntuforums.org/showthread.php?t=731763) \- this was really annoying. I could use the volume slider all I wanted but the volume wouldn't really change. This was fairly easy to fix.  

    1. Open Sound Control
    2. Select ALSA for "Sound Playback" under Audio COnferencing.
    3. Select "PCM" for the Default Mixer Tracks
    4. Restart
  
I don't know if you have to actually have to restart but I did.

  
  
  
Linux has come a long way in the past 14 years but it still has a ways to go
before I could recommend it as a home replacement for my "normal" relatives.

## Comments

tekiegreg

I hear you there, after trying on Mandriva 2006 a year back on a new computer,
I found myself with 2 key issues 1) Dual monitor support was non-existent and
fixing that would be icky and 2) No DVD movie playback. Never could fix either
one so I switched back to Vista, despite the criticism Vista does well on my
computer. Sorry Linux guys...

