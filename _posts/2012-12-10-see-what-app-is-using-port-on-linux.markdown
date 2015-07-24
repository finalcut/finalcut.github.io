---
layout: post
title: "See What App is Using a Port on Linux"
date: 2012-12-10
comments: false
categories:
 - linux
 - netstat
---
Sometimes you need to know what application is using a specific port.  Here is
the syntax so I can remember how to do it:





```sh
sudo netstat -lpn |grep :{PORTNUMBER}


```


 Just replace {PORTNUMBER} with the port in question:



```sh
sudo netstat -lpn |grep :3306
```


 When you do that you'll get an output sort of like this:



```sh
tcp        0      0 198.183.217.196:3306    0.0.0.0:*               LISTEN      880/mysqld
```






