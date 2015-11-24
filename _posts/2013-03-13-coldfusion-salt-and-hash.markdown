---
layout: post
title: "Coldfusion Salt and Hash"
date: 2013-03-13
comments: false
category: coldfusion
tags: [security,encryption,salted-hash,password,hash,salt]
---
This isn't particularly ground breaking or even noteworthy - I mean people
have been salting and hashing passwords for quite a while - but I figured I
would put this coldfusion component out there to help people who haven't done
salting and hashing in coldfusion before.  

If you aren't really comfortable with the terms salting and hashing or[ salted
hash - then please read this great article on the
topic](http://crackstation.net/hashing-security.htm).  

I'm not really going to go into any detail on the component here - instead
I'll just point you to [the github repository where you can read the readme
and checkout the source code](https://github.com/finalcut/SaltAndHash#readme).  

Please provide feedback if you see something incredibly stupid in the code -
or better yet submit a pull request.  



## Comments

Henry Ho

Regarding use of Cryptographically Secure Pseudo-Random Number Generator with
CF, GenerateSecretKey() is as good as java.security.SecureRandom right? http:/
/help.adobe.com/en_US/ColdFusion/9.0/CFMLRef/WSc3ff6d0ea77859461172e0811cbec22
c24-6e72.html
