---
layout: post
title: "Kill an Unresponsive Process"
date: 2012-11-29
comments: false
categories:
 - awk
 - linux
 - command-line-magic
 - ps
 - grep
 - unix
---
This is a kind of obscenely specific post. I'm doing this so that I have it
for my own future usage. However, the concept behind it is translatable into
other scenarios.
While running a bunch of WSO2 API Manager servers I've run into problems where
one of the 2 gateway servers becomes a bad member of the cluster overnight.
But, when I try to ctrl+c to kill it at the terminal it doesn't respond and
die as expected.
Instead I have to figure out the process and tell it to die. I personally have
extracted all of my WSO2 server zips into a directory called "api_with_greg"
for my API Manager servers that are communicating with a Remote Governance
registry. The different servers might be on different physical or virtual
machines but I always put them inside a parent directory of api_with_greg.
Thus I might have some directories like this:



```sh

~/api_with_greg/store/

~/api_with_greg/publisher/

~/api_with_greg/gateway1/

~/api_with_greg/gateway2/

...


```



You get the idea. Thus, when I execute the ./{api_server_home/bin/wso2server.sh script the string "api_with_greg" is part of every JVM call when I run "ps -ef"

Thanks to this I can use a simple bit of command line magic to get the parent process id of each JVM instance (the parent process points to the wso2server.sh script [shell script] that launched the JVM).  Then I can kill the specific shell script

Here is that magic:



```sh
$ ps -ef | grep api_with_greg | grep -v grep | awk '{print $3 $14}'


```



Kind of crazy looking but I'll explain:




  1. ps -ef  gets a listing of processes along with a bunch of other data broken out into space deilmited columns

  2. the results of 1 are fed into a grep (search) for any lines containing "api_with_greg"

  3. the results of 2 are fed into another grep which removes the command in 2

  4. finally awk is called to display the results found in the third column (parent process id "ppid") and the 14th column which is the path to the HeapDump for that JVM which, in these cases is in a subdirectory of each individual API Manager server.


Here is an example ps -ef





```

1001      2795  2696  0 10:47 pts/3    00:00:00 /bin/sh ./wso2server.sh

1001      2812  2795  0 10:47 pts/3    00:02:21 /usr/lib/jvm/jdk1.7.0/bin/java -Xbootclasspath/a: -Xms256m -Xmx1024m -XX:MaxPermSize=256m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/home/standardstacks/api_with_greg/store/repositor

1001      3055  2956  0 10:48 pts/4    00:00:00 /bin/sh ./wso2server.sh

1001      3072  3055 87 10:48 pts/4    03:33:27 /usr/lib/jvm/jdk1.7.0/bin/java -Xbootclasspath/a: -Xms256m -Xmx1024m -XX:MaxPermSize=256m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/home/standardstacks/api_with_greg/greg/repository

1001      3330  3221  0 10:48 pts/5    00:00:00 /bin/sh ./wso2server.sh

1001      3347  3330  1 10:48 pts/5    00:02:27 /usr/lib/jvm/jdk1.7.0/bin/java -Xbootclasspath/a: -Xms256m -Xmx1024m -XX:MaxPermSize=256m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/home/standardstacks/api_with_greg/publisher/repos

1001      3615  3494  0 10:49 pts/6    00:00:00 /bin/sh ./wso2server.sh

1001      3632  3615  1 10:49 pts/6    00:03:48 /usr/lib/jvm/jdk1.7.0/bin/java -Xbootclasspath/a: -Xms256m -Xmx1024m -XX:MaxPermSize=256m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/home/standardstacks/api_with_greg/g2/repository/l


```




And here is an example of output of the whole command:



```
1549-XX:HeapDumpPath=/home/standardstacks/api_with_greg/keymanager/repository/logs/heap-dump.hprof

1809-XX:HeapDumpPath=/home/standardstacks/api_with_greg/gateway/repository/logs/heap-dump.hprof

2795-XX:HeapDumpPath=/home/standardstacks/api_with_greg/store/repository/logs/heap-dump.hprof

3055-XX:HeapDumpPath=/home/standardstacks/api_with_greg/greg/repository/logs/heap-dump.hprof


```




At that point I see the parent processes I might need to kill.  For instance, let's say the gateway server is hanging.  Then the parent process for that is in 1809 so I can kill it.


There are two ways of killing the process:


```sh

kill -9 1809

kill 1809


```




The first effort should be to use 'kill 1809' without the -9.  This will give the application a chance to execute any "exit" logic before it aborts.  Thus it might shut down gracefully.  If that doesn't do the trick then I can use 'kill -9 1809' which is a FORCE KILL and will just cause the process (and it's children) to stop immediately and no exit code will be executed.




