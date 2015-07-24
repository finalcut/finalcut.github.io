---
layout: post
title: "Create App Shortcut on Mac for MacPorts installed program"
date: 2012-01-20
comments: false
---
This is here just so I remember how to do this:



  1. create a new automator task
  2. type = application
  3. add a node: "Run Applescript"
  4. in the body of the method add



    do shell script "/opt/local/bin/{executable_name} &"
```



  5. change {executable_name} to the right value; for example if launching pidgin change it to pidgin

  6. save the task to your Applications directory

  7. profit?


Thanks go to this StackOverflow/[SuperUser post](http://superuser.com/questions/179842/create-alias-desktop-shortcut-of-an-application-installed-by-macports) that answered this for me.





I was a failure at using Platypus which was the other suggestion.




