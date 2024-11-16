---
layout: post
title: "Git Me some Help!"
date: 2009-12-31
comments: false
categories:
 - git coldbreadcrumbs
---
I recently (in October) moved an old very shabby project I wrote into GitHub.
I did this for two reasons. The first is I've been keen to try out Git for a
while and this seemed like a good opportunity. The second is that a few people
have asked for this source code in the distant past so I figured I might as
well just stick it out there.  
  
Now, I'm not going to lie - [the code I put up
there](http://github.com/finalcut/ColdBreadCrumbs) is pretty crappy. However,
this post isn't about that - it's about a strange problem I've had with Git
the two times I have tried to use it.  
  
Back in October when I setup everything I had to create an ssh key. I'm not
even sure where the first one ended up going so I decided to just use the
"default" settings and trying again. I had associated both public keys I
created that day with my github account and I was able to add the files and
push them up. I figured all was good and the next time I made a change things
would be smooth.  
  
As Lee Corso says, "Not so fast my friend!"  
  
Today I updated the readme file and wanted to push the file up. At first I
forgot I had to start a command prompt with the git_cmd.bat file but once I
realized that I kept being told "Permission Denied (publickey)"  
  
I looked in the docs and they all suggested the key should be in my /documents
and settings//.ssh directory - none were but some of those I had previously
created were in my root git directory so I copied them out to my ~/.ssh
directory. Then I tried again and got the same error message.  
  
At this point I though, well, I'll try the git_bash.bat file. Same problem. So
I ended up creating a new keypair using all the defaults again and then
associating this new public key with my github account. At this point I was
able to push my changes up.  
  
Am I doing something wrong that leaves me needing to create a new key? Did I
not have to create a new key this time and I just had something setup wrong? I
don't know. I seriously hope I don't have to create yet another key the next
time I try this out.

