---
layout: post
title: "EditPlus and MxUnit Tests Directory Testing Tool"
date: 2008-10-16
comments: true
featured: true
categories:
 - coldfusion
 - tdd
 - unit-testing
 - mxunit
 - editplus
---
Sometimes it is useful to be able to fairly quickly fire off a directory of
unit tests using MxUnit. EditPlus and the UserTool functionality come in handy
once again:




  1. Create a new user tool; I called mine MxUnitTest a Directory


  2. Command: c:\Program Files\Internet Explorer\iexplore.exe


  3. Argument: http://localhost/mxunit/runner/HtmlRunner.cfc?method=run&amp;test;=$(FileDir)&amp;output;=html&amp;componentPath;=$(Prompt)



The $(Prompt) argument is there to ask you what the component path is. For
example I just ran this one against lb2.unittests.model.bean - it wants the
component path to the directory so make sure you don't include the final
portion that would point to a specific component.

The ($FileDir) argument basically grabs the full path to whatever directory
your currently active file is in.

