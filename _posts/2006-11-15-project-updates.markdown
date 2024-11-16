---
layout: post
title: "Project Updates"
date: 2006-11-15
comments: false
category: [general,.net,php,c#]
tags: [wordpress,vb.net]
---
Just an FYI for those interested.  



  * The wordpress-flash theme ended up being canceled. The customer decided he didn't want anything that flashy after all - sorry for the pun.


  * My VB project was put on hold; I hope I get to finish it - it was actually kind of interesting.


  * I'm building a C#.net project now. We are using a DAO library called ["Doodads" by "My Generation"](http://www.mygenerationsoftware.com/portal/dOOdads/dOOdadsOverview/tabid/63/Default.aspx). They are OK - but have some pretty big limitations (or at least our understanding suggests they do). All of the objects are built 1-1 with the database tables - even though our model OFTEN spans multiple tables. In order to have a "DAO" (the call them "DooDads") that spans multiple tables we actually have to create a View and then create a readonly "viewdad" Not only does it sound stupid talking about them I really don't enjoy using them much. I really like ActiveRecord - does anyone know of a good .NET ActiveRecord implementation I could use on future projects?  

I think this project, especially with it's scope, and the fact that I
constantly have to dynamically generate objects, would have been better served
in an interpreted language like Ruby; plus Ruby's ActiveRecord is a better fit
for what were trying to do. Oh well, live and learn.  

Coldfusion is out of the question for this project because this is a desktop
and a web app. CF would have been fine for the web back end I suppose but that
would have been clunky considering we can reuse all of our DAOs on both
desktop and web server using a unified language between the two.  

C# does have one great benefit that I'm not sure would have been present in
Ruby - a one click updater. It is incredibly easy to push new updates to the
desktop client using C#. If you are using any of the .net 2.0 stuff and you
aren't using this feature you should take a look - it's very slick and super
easy to use.



  * I actually really like Visual Studio 2005 - its a really nice IDE and it loads surprisingly fast. I still prefer [EditPlus](http://www.editplus.com) for my day to day work but when doing this .Net stuff VS 2005 is a good solution.


  * I have two monitors at work now and the second monitor is a huge boon! I never realized how much more efficient it would be to have the DB open in one screen and the IDE in another. It is so much better than toggling back and forth. However, I feel my short-term memory may no longer get exercised as much since I can just reference the other screen now.


  * I'm still actively working on 2 coldfusion projects. One uses MG:Unity and I have to say I really like it and using ColdSpring. I didn't really grep ColdSpring when I first heard about it but once you use it it's easy to fall in love. I haven't tried Reactor yet.



I was called by the worst ever recruiter the other day. Every other word out
of his mouth was "uhhm" and he didn't even bother looking at a map to figure
out where my city is located in relation to another state. If only I could
take the fact that a recruiter called me as a compliment it would have made it
bearable but we all know they are just trying to make a buck and I seemed like
a potential client.  

Right now my life consists of switching from one project to another on, about
a 4 hour interval. So I switch from PHP, to CF, to C#, and bounce between
Oracle and SQL Server pretty regularly. Because of this I really haven't had a
chance to post any nice "insight" articles recently. But I will try to do
better.

## Comments

Anonymous

Have you checked out http://www.castleproject.org/activerecord/index.html as a
C# ActiveRecord
