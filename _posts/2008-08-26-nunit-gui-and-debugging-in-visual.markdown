---
layout: post
title: "nUnit GUI and Debugging in Visual Studio"
date: 2008-08-26
comments: false
categories:
 - visual-studio
 - nUnit
 - .net
---
This is just a short note to help people debug their unit tests a little
easier. To most people this will probably seem pretty obvious but since I
don't spend a ton of time in the VS environment I thought it was pretty nifty
(and it saved me from having to buy something like TestDriven.Net - which
rocks btw).  
  
Basically what I needed was a way to debug my unit tests with the visual
studio debugger. This is actually pretty easy to accomplish. Just follow these
easy steps:  
  

  1. Set your test project as the default project. To do that just right click on the project name in the Solution Explorer pane and choose "Set as Default"
  2. Set the projects "Start Action" to launch the nUnit Gui. To do that right click on the project in the Solution Explorer, Select the "DEBUG" tab, then click the radio button labeled "Start External Program" - then pick the nUnit Gui Runner as the external program.
Now, you can run your test suite. By clicking the run icon in the Visual
Studio toolbar the nUnit Gui Runner will popup but no tests will run
automatically - however the Gui Runner will be populated with all the tests in
your project. Now you just need to pick the test(s) you want to run and run
them. If those tests (or the code they call) have any break points the Visual
Studio window will reactivate when the breakpoint is reached and you can step
through your code.  
  
I hope this helps others embrace unit tests with .Net and Visual Studio.

## Comments

Anonymous

Additionally in the Argument Section of the DEBUG tab. You can specify the
assembly name like this  
  
myTestAssembly.dll /run  
  
Helps if you work on several different projects.

Anonymous

You can also add the /run argument so that the tests are run automatically.

urfolomeus

Thanks. You've helpded to conclude a 3 hour search! I had all the points taken
care other than the (incredibly obvious) first one :$

