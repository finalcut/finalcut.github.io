---
layout: post
title: "Cruise Control, Ant, and Subversion"
date: 2008-10-15
comments: false
categories:
 - continuous-integration
 - tortoisesvn
 - cruisecontrol
 - ant
 - svn
---
I run in a windows environment generally and thus I use TortoiseSVN as my
local svn client. So, when I was setting up my CruiseControl installation for
my current project I used Tortoise to initially check out the source code and
then wanted to use the SvnAnt task to keep that version up to date before
running any tests.

Nice dream.

It seems that one of the three clients involved in my efforts just didn't get
along with the others. First there is the TortoiseSVN client, then SvnAnt, and
finally whatever CruiseControl is using to check the repo. One of these three
is causing me all sorts of grief. Basically, what happens is, if I update the
repo with one client the other's wont work due to their being "too old of a
version".

I'm using TortoiseSVN 1.5. I'm using SvnAnt ver 1.2 RC 1 (for SVN 1.5). My SVN
server is 1.5.5 and I'm using the latest version of CruiseControl. Maybe I'm
just missing something really simple but whatever is going on I'm kind of
annoyed so I've taken SvnAnt out of the picture.

Basically, all of us on the team us Windows with TortoiseSvn so now my ant
file has a target like so:




```xml
 <target name="updateSource">

  <exec executable="C:\Program Files\TortoiseSVN\bin\TortoiseProc.exe">

   <arg value="/command:update" />

   <arg value="/closeonend:3" />

  </exec>

 </target>


```




The /closeonend:3 argument forces the dialog to close so long as no errors, conflicts, or merges.  This will be a little annoying considering, at the moment, the CruiseControl server is on my dev box so everyonce in a while the update dialog will flash by.  However, this is a small price to pay to get everything working.


If anyone can recommend a good tandem of CruiseControl, TortoiseSVN, and SvnAnt I would really appreciate it!


**UPDATE**

TortoiseSVN 1.5.0 and SvnAnt 1.2 RC 1 work very well together.  The problem lies in the CruiseControl svn client which is older.  However, I can't use the SvnAnt 1.1 RC 2 task because it won't work with SVN Server 1.5.5.


Thus, at the moment, I have to pass on using the SVN config options for CruiseControl.  Hopefully someone is working on a new plugin for CC and SVN!


**BETTER UPDATE**

HAHA! Success.  One of the older versions of SvnAnt came with a JavaSVN jar.  Once I removed it all of my svn needs work.  Tortoise, SvnAnt, CruiseControl... Boo YA!




