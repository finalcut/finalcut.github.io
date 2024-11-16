---
layout: post
title: "Configure EditPlus with ANT"
date: 2008-10-14
featured: true
comments: true
categories:
 - eclipse
 - ant
 - editplus
---
Ok, so you like to use EditPlus for your lightweight coding but you still want
to do Test Driven Development (TDD) using ANT to fire off your tests. What do
you do?

Well, fortunately, EditPlus supports "User Tools" (just like most programming
editors) that will fire off an external tool. Ant is pretty easy to configure
to use with Edit Plus; and thanks to the [Edit Plus Wiki's entry on
Nant](http://editplus.info/wiki/User_Tools#Compile_NAnt_Projects) I was able
to setup Ant pretty quickly.

This tutorial assumes you can find the dialog for adding a new user tool and
that you have already clicked the "Add Tool" button.





```
Menu Text: ANT

Command: {path to your ANT install/ant.bat}

Argument: $(CurSel) -find

Initial Directory: $(FileDir)

SELECT "Capture Output"

-----------

OUTPUT PATTERNS

UNCHECK "use default output pattern"

Regular Expression: ^[\t ]*(\[.+\] )?([^(]+)\(([0-9]+),([0-9]+)\)

File Name: Tagged Expression 2

Line: Tagged Expression 3

Column: Tagged Expression 4


```




Make sure you put the path to your ant.bat file.  I use the ant that comes with eclipse so mine is at C:\dev\tools\eclipse\plugins\org.apache.ant_1.7.0.v200706080842\bin\ant.bat.


The argument $(CurSel) basically lets you pick a target name and then fire off the ant tool.  You just highlight a string of text before executing the ANT user tool.  The -find argument tells ANT to search backwards up the file structure to find a build file.  The start directory argument of $(FileDir) tells Ant to start looking for a build file in the directory that you are currently editing.  Thus, you want to make sure you build file is in the root of the project you're working on.


By having these two arguments setup as they are you get a pretty generic tool setup so that you don't have to edit any of the settings for each new project you work on.  You just have to create a build file.




### Custom Build Tasks?



If you have custom build task jar files the best way to get them to work with ANT - regardless of how you are starting ANT is to put them in your ${user.home}/.ant/lib directory.  In windows your ${user.home} directory is c:\documents and settings\{username}.  You may not be able to create a directory that starts with a . in windows explorer but you can from the command prompt.  Just plop your custom jar files in that directory once it is all created and they will instantly be available in Ant if you use Eclipse, EditPlus, or any other editor (or just the command line).




