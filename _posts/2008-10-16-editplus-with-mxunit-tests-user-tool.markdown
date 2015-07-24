---
layout: post
title: "EditPlus with MxUnit Tests User Tool"
date: 2008-10-16
comments: true
featured: true
categories:
 - coldfusion
 - unittesting
 - mxunit
 - editplus
---
Today I decided I wanted a quick way to launch a specific MxUnit test file
from within EditPlus. It turns out the handy UserTools menu comes to the
rescue again.




  1. Create a new User Tool - I called mine UnitTest


  2. Command: c:\Program Files\Internet Explorer\iexplore.exe


  3. Argument: http://localhost/$(ProjectName)/unittests/$(Prompt)/$(FileName)?method=runTestRemote



You'll notice I have the argument ${ProjectName} in there. I did this so my
tool would be fairly generic and usable across each project I'm working on. In
order for it to work, however, you need to use EditPlus's built in "Project"
tool and create a project. Your project name should match up to whatever your
projects webroot directory is called. So if you are working on a project
accessible via http://localhost/myUnitTestDemo then your project name should
be myUnitTestDemo even if the directory your files in is named something else
(and you just have it aliased in your webserver).

I also have a $(Prompt) argument there. This lets me specify what directory,
relative to my base "unittests" directory the file I am testing is in.

Finally the $(FileName) argument does limit me in requiring that I have the
MxUnit test file I want open and active before using the tool. However, that
seems like a decent sacrifice to me over having to type in the URL for the
entire file each time I want to run a test.

