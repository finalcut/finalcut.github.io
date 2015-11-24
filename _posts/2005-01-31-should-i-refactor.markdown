---
layout: post
title: "Should I Refactor"
date: 2005-01-31
comments: false
category: programming
tags: [refactor,oop]
---
I have an older app (initially written in CF 4.7) that has been
upgraded/modified pretty much every new fiscal year for a customer. It is a
very handy application and one that is mission critical for the customer.
However, it (like everything, I suppose) could be improved. The maintenance
headaches alone beg for a rewrite at times.  

When I first started on the project I was just learning CF - coming from an
Ada, Java, and C background. I also didn't have much experience with databases
yet - nor did I fully understand the price paid by performance for hammering
the database in one CF request. Needless to say in the intervening years I
have learned enormous amounts and I try to apply these lessons to each
successive update that happens to the customers project. In fact, I would
imagine that if you looked at the code you would see "evolutionary"
improvements to the way things are done. Overall, the app is very stable and
works as expected. Furthermore it isn't particularly fragile as each years
changes have not caused any breakage of past systems (amazingly enough). I'm
proud of the end result (if not all the code that makes it up) and, in fact,
it is the first time I used the XMLHttpRequest object (way back in 2000)
though then it was called a "data island".  

However, the app is basically still the same big procedureal spagehtti factory
that it always was. CFCs didn't exist until CF MX and even then cftransactions
and multiple CFCs didn't get along until MX 6.1. Beyond the merely technical
reasons for not rebuliding this beast from the ground up are the cost and time
constraints. As the old adage goes, "If it aint broke, don't fix it!" However,
I would really like to improve the application - even if it meant using my own
time.  

A couple of problems arise no matter how I go about refactoring. 1. How do I
explain the new "improvements" to the client without leading them to the
conclusion that the prior code was crap? And 2. How do I justify the fixes of
any bugs that appear in the new version to either my boss or the client?  

Obviously, the only real answer is to get the customer to agree to the rewrite
in advance perhaps with the caveat that the rewrite of existing functionality
is "on the house." That still doesn't really solve the problem of addressing
bugs though. Our company tends to work on fixed price or time and materials.
Like any other company we don't really like working on "Overhead" related
projects because they aren't generating revenue. Projects like the one I have
been discussing typically have maintenance contracts which deal with new
enhancments (of which there are tens of each fiscal year, some minor others
very major) and bug fixes that arise due to these enhancements - unfortunately
none of those really deal with this situation.  

In the terminology of fusebox there are probably 15 major circuits within the
application and I actually manged to update one of them to a CFC based
implementation last year. However, there are still 14 that could use the same
treatment. It would be a pretty substantial chunk of work and I would hate to
proceed if it didn't seem like the payoff for doing so would be worth it in
the long run. By payoff I mean ease of maintenance and code stability.  

I have been able to redo bits of the application before in order to generate
orders of magnitude better performance in those areas - and the customer as
been willing to pay for fixes related to these free improvments becuase they
felt the improvement was substantial enough to warrant the minor cost of the
bug fixes (changes have typically been UI improvements and database
interactions). How would you approach a scenario like this? Or would you at
all?  

In the end it is all up to the customer. As with many things I wish I knew
then what I know now. Hopefully, I will get the go ahead to make the changes I
feel are needed to insure the application lives long into the future.  
