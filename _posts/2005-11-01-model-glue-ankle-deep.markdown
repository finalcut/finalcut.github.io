---
layout: post
title: "Model Glue - Ankle Deep"
date: 2005-11-01
comments: false
category: coldfusion
tags: [modelglue,framework,mvc]
---
Well I just finished off my first Model-Glue (MG) application. It was an
extremely trivial Todo list program that used no persistence mechanism beyond
the application scope via the MG controller.  

Overall, I have to say it was pretty easy to pick up. My production was a
little slower than it normally would have been - BUT - that is because I'm
trying to learn the nuances of the framework. The end result seems pretty
solid. However, I do have one minor quibble - not all directed exactly at MG;
but some are relevant.  


### Quibbles



#### Execution Speed


I turned off the "reload" and the "debug" stuff in the ModelGlue.xml file and
the speed of the loading of my VERY simple form was still kind of slow (over 1
second). I guess I figured things would be a bit more responsive than that.
With that said I am concerned about how it will do with a more complicated
view. Is the MG overhead fairly consistent around the 500-1000 ms range or
does it grow along with your view? If it is consistent then I can probably
live with it.  

I had thought perhaps I was doing something wrong that was causing the 1.5
second load time but even the sample contact manager takes that long to show
the empty contact list with all the refresh stuff turned off.  


#### Documentation


Well, I can't complain too much since this is a free offering but a bit more
documentation would be nice. For instance, I turned off the "reload" setting
in the stock price sample app but didn't realize I had to set a reloadtoken
and reloadvalue before hand. So now the only way I can reload that app, it
seems, is to restart the CF server. Not a big deal - but one that I could have
avoided had the basic settings been more clearly documented in the samples
and/or the MG Application Template files.  


#### Event Forwarding


I dont know which is better - to use the event.forward method of rediction OR
the ModelGlue.xml result tag with the redirect option set to true. I have a
gut feeling it is better to do the redirect in the XML so the program flow is
more transparent - and to only use the event.forward mechanism when necessary.
I'd like to see what the best practice is on that.  

I also don't really understand why the append parameter of event.forward is
required. Seems like it should default to a blank string to me.  


### Disclaimer


I have barely scratched the surface of MG. I didn't mess with config beans at
all or Event beans. In fact I haven't even gotten close to dealing with
ChiliBeans in anyway. My goal today was to build a clean MVC app using the MG
framework and that is exactly what I did. I can create, edit, delete, and
toggle the status of different todo items within one global list.  


### Things I instantly Like



#### Flow


I like the way the xml file and the controller work together. I like the
message broadcasting and I really like the way views are collected and then
spit out. Typically I don't like to couple anything but the ability to couple
various "view snippets" into one master view template is pretty nice. (I had
noticed this in my brief review of Mach-II).  


#### Easy


It is one easy framework to start using. I doubt you even need to have a grasp
on what MVC is to learn MG pretty quickly though some knowledge of MVC
certainly helps.  


#### Event Forwarding


Even though I put this under my quibble section too - I'm still glad event
chains are supported - and in a flexible manner.  


#### Sample Apps


I think there are 8 sample apps currently included. While not documentation in
the true sense of the word that is a pretty large selection of samples. It is
also cool that each of them can teach you something else. It would be nice to
see one "master" sample that included all the techniques used in the other's
(maybe one does and I just don't realize it).  


#### Organization


I like the natural organization that occurs to your application when using any
MVC framework and MG is no exception. I assume, but haven't tried yet, that
you can further organize your files within the model, view, and controller
directories using subdirectories without any issue. This overarching
organization would obviously improve team productivity.  


### Gotcha!


A few things "got me" as I was developing my todo list app beyond the things I
mentioned in my quibbles.  

#### ModelGlue.xml


Make sure you put everything where it belongs. I accidently put a event-
handler after the closing event-handlers tag and for obvious reasons my event-
handler wasn't found by MG.  

#### Caching


Even though I already said this, make sure you specify a reloadkey and reload
password in ModelGlue.xml, at least during development. This will save you the
headache of restarting CF down the road.  


### Final Thoughts


I think with the impending Arf! work that Joe is doing (ActiveRecord)
presuming it gets added into MG that MG will be a pretty darn compelling
solution. I have to commend Joe on his excellent work and his generosity of
the work with the CF community.  

My next step in digging into MG is going to involve adding a basic security
mechanism , some form of persistence, and letting each user keep their own
TODO list with my app. After that I will dig into the config and event beans
of MG. Once I have that done I will then look at using ColdSpring with MG as,
according to Sean, the integration is pretty slick. Once ColdSpring is
integrated then I will get to touch on the AOP stuff to see how well it works.  

Overall, I'm pretty excited about the opportunity to try these things out with
CF. And, I may even get to apply them all to a new project at work in the not-
too-distant future. If I do get to use MG with that project then I will let
you know where it is once I have completed it.

## Comments

Bill

Thanks for the tip Dave. I'll double check that tomorrow and post what I see
then.  

Sean, is their a key/value pair defined by default if they aren't specified in
the ModelGlue.xml file at all?

Anonymous

Great to see you documenting your learning experience! Thank you!  

Documentation / reloading:  

reload="false" simply means that the framework won't automatically reload on
every request. You can still force it to reload by specifying on the URL the
reload key/value pair which, by default, is init=true. i.e., you can omit
these because they have defaults. You do not need to restart the server!  

Forwarding:  

Best practice is to do the redirects in the result tag if possible (it isn't
always possible if your event is dynamically selected).  

Note that most event chaining will be done without a redirect (internal event
chaining).  

\-- Sean Corfield

Anonymous

See if you have debugging turned on (within CFADMIN) -> specifically "Report
Execution Times".  

That's probably the issue with your slowdown.  

-Dave Ross
