---
layout: post
title: "CruiseControl and 500 Server Errors"
date: 2009-05-06
comments: false
categories:
 - continuous-integration
 - cruisecontrol
---
Today, for the first time in a few months, I had to interact with my cruise
control server again. To be honest, I'm not sure what happened but it stopped
working and I had to jump through some hoops to get it all working again.  
  
First I had to uninstall it and install it in a directory that didn't have any
spaces in the name. Before it was installed at c:\program files\cruisecontrol
- that space was causing a weird JSP error that prevented compilation.  
  
Thus I installed it at c:\cruisecontrol. Of course, I hadn't touched it in so
long I had forgotten about my special ant tasks and I had to go find those
again (uninstall actually deleted my entire old directory.  
  
However, during the reinstall there was a problem because the old service
wasn't removed (maybe because I had it running as me?) So I had to remove the
service  
  

  
sc delete <SERVICE name>  

  
  
Then I reinstalled again and it worked out OK. Once that was resolved I had to
get my projects all checked back out of SVN. I had forgotten that CC comes
with a connectfour project by default and so, after I replaced the config.xml
with my customized one, I couldn't load the CC dashboard anymore - I had to
delete the connectfour project directory and restart the CC service.  
  
Eventually I got it all up and running again and my projects built OK. Now I
just have to train 2 other teams on setting up their ColdFusion projects to
run tests from an ANT script so that they can take full advantage of CC and
MxUnit. I'll be doing that tomorrow.  
  
Then I have to figure out how to get CC to build a .net app; if I can't
hopefully I can install CC.net on the same server as CC without any issues. I
had hoped to use cc.rb but there are some issues with it on a windows server
so that is out of the picture at the moment (due to our needs for building
.net apps).

