---
layout: post
title: "Model-Glue : Knee Deep"
date: 2005-11-04
comments: false
category: coldfusion
tags: [modelglue,framework,mvc]
---
Well I'm making pretty good progress with my Model-Glue experient. Thanks to
Dave Ross and his "turn the debugging" off double reminder the performance is
also pretty darn fast.  

Where am I? Well, so far I have the abilitiy to create todo's that are stored
in a single 'mgTodo' table in my SQL Server database. I have abstracted that
away into a DAO so I could quickly change the backend without a problem and
that should work pretty well.  

I am using a variant of [Jared Rypka-Haur's facade component](http://www.web-r
elevant.com/blogs/cfobjective/index.cfm?mode=entry&entry=7B760E34-BDB9-5320-E8
8A375CA379AB9F) (i modified it quite a bit) but it was an excellent basis for
my needs to store the current user object in the session scope. That's right,
I have also added some bare bones security to it.  

Currently the security is incredibly bare bones using a ConfigBean to identify
the only pages in the app that don't require security and a cached security
component to check if the user has access to the requested page. I don't
actually have any kind of real login/authentication setup but it is all
stubbed out so I can pretend to login (just nothing gets check in the DB) and
my user auto has access to everything once I'm pseudo-logged in.  

All of this worked out pretty well with MG and I was able to abstract pretty
much everything I needed to. However, I did run into a small problem when I
introduced multiple controllers. Basically, all of my controllers need access
to my factory object. However, I don't want to create the factory in each
controller and basically have redundant code in each. So, basically, I'm not
sure where that should happen.  

My solution, was to create a "controller" object that is pretty generic for my
needs that extends "ModelGlue.Core.Controller" then each of my controllers
extends this generic controller (I know, i'm starting to get a inheiritance
tree so I'm not thrilled, but we will see how this works out).  


### What I was Doing


In my basic Controller's init method I had it create an instance of the
factory object and store it in it's local variables.instance structure as
variables.instance.factory. The main problem I see with this solution is that
I get one factory per Controller created still (but the controller is cached
by MG in the application scope so at least it isn't recreated all the time).  

As my app grows and I think of other objects that need to be in the singleton
(or as my factory creates objects which I typically just store in it's private
scope) I will have repetitive "singletons" which pretty much destroys the
whole idea of a singleton. What's a guy to do?  


### My Solution


Well I think "What a guy should do" is use the built in Model-Glue "cache"
methods, ExistsInCache, AddToCache, and GetFromCache (plus RemoveFromCache).
I'm still going to keep my base "controller" object so I know my various
controllers have access to my factory and session, but since the main
controller checks against the existance of either singleton in cache ahead of
time I should maintain the singularity of each.  


### One Problem


There is still one problem though - the function
ModelGlue.Core.Controller.RemoveFromCache says it returns a boolean value. It
inturn calls ModelGlue.Util.TimeCache.RemoveValue which doesn't remove
anything (void). This contradiction raises an error saying that the first
method (RemoveFromCache) isn't returning a boolean. So, I updated my copy to
return void and changed the line (56) cfreturn
variables.ModelGlue.ModelGlueCache.removeValue(arguments.name) to cfset
variables.ModelGlue.ModelGlueCache.removeValue(arguments.name)

## Comments

Jamie Jackson

Doesn't appear a bug report was filed for this until today. This is fixed in
the bleeding edge version.  

http://trac.model-glue.com/model-glue/ticket/307

Bill

You may want to ask Joe Reinhart about how to change the behavior of MG. You
can find him at http://www.model-glue.com or sign up for the model-glue
mailing list and ask your question there because, frankly, I don't know the
answer to your question.

Anonymous

Hi  

In modelglue 1 if we call a function in controller which actually doesnt exist
from the ModelGlue.xml message listener part  
it will cause an error.  

But in modelglue 2 this doenst seem to happen. Is there any way  
to get it back like it was in modelglue 1
