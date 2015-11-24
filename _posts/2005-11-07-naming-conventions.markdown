---
layout: post
title: "Naming Conventions"
date: 2005-11-07
comments: false
category: coldfusion
tags: [oop]
---
On a recent post on the cfc-dev list Chris Scott stated:  


>  
variable names start lowercase with each word starting upper: userName  

class names (cfc names) start uppercase: SecurityService.cfc or User.cfc  

instances of classes are variables, so they follow the variable naming
convention: user is an instance of User.cfc  

methods in cfcs, start lowercase: user.getName()  

I'm not sure where the community stands on this, but cf cfunctions (reserved
keywords) should start uppercase: ArrayAppend()  



I post this to support the conventions he mentions as "standard CF
conventions" and I hope others practice them as well (I know alot do, but for
those that don't, please consider them).
