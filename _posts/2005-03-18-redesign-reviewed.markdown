---
layout: post
title: "Redesign Reviewed"
date: 2005-03-18
comments: false
category: programming
tags: [uml,oop]
---
I was asked on my prior post what process I follow once I have decided to
redesign an existing application. This is not an easy question for me to
answer partly because the process is dependent on the application being
redesigned and also because my general approach to the problem evolves with
each new project - whether it is a redesign or an entirely new application.
However, some elements of the process are always present.  

First off, I need to understand the existing application. Sometimes I was the
person who wrote the initial application but typically that is not the case.
Nor do I usually have any real documentation on what the application does and
sometimes I don't even have the source code (such as when we are tasked with
writing a new generation of software for a government system and the initial
contractor doesn't even exist anymore). While learning to understand the
application I make sure to document all of the functionality that I can in
both use cases and the UML. This helps me get a better grasp on what I will
need to do, plus help me identify any existing holes in the current system.  

Once the current systems functionality is documented and understood I can
begin to identify the objects that make up the system. Via my prior
documentation I can typically see most, if not all, of the inter-object
relationships as well. Once again, I return to writing documents and crafting
UML diagrams.  

As you might imagine, this is pretty boring stuff. But it needs to be done
else nobody working on the final product will have a clue what really needs to
be done and we won't have any real requirements to verify against.  

Now that I have a set of objects defined I work on creating a data model that
will support my objects. The data model doesn't necessarily match up with my
objects on a object::property <--> table::column basis but most of my
object::property values do need to be represented somewhere in the data model.  

Up to this point I probably haven't even settled on a data source nor an
implementation language. At times the customer might have already specified
both - but sometimes we have the choice of actually picking what we think will
be the best tools for the job.  

At some point we do have to actually build the system though so once all the
analysis and modeling are "done" some code will get written. I say "done"
because the models will all change many times as I come to a better
understanding of where certain methods should be within the system and as I
gain a stronger understanding of the system as a whole.  

It is also important to remember that the customer (whomever that is, be it
your boss or an actual outside entity) needs to stay involved throughout the
process to make sure you are actually giving them what they want and not
necessarily what they said they want.  

Communication is a tricky thing and this is probably the most important lesson
I have learned. Until the customer actually sees what they asked for in a
system they don't necessarily always know what they really wanted. It is
important to make many small point builds on a regular basis that the customer
can see/touch. By doing this they can give more consistent and frequent
feedback. I for one would rather know as soon as we do something that didn't
match the customers vision than weeks or months down the line when a change
may be exceptionally difficult/expensive.  

I know this doesn't necessarily explain my process but it is about as well as
I can do in a short hopefully readable post. Later this weekend or early next
week I will try to explain what I am going through with ProTask - an
application I inherited and already redesigned once and am in the process of
redoing once again.  

My degree is in "Computer Science and Software Development" which is about as
close as [my university](http://www.marshall.edu/) could come to claiming it
offered a true Software Engineering degree. Needless to say, I came into my
profession without the best background as almost everything I learned at
school was self taught. Because of this my work has taken giant steps since I
entered the industry 5 years ago. However, this means that some of my earlier
work has plenty of room for improvement.  


Finally, here are a couple of books that I have read that have been both
useful, informative, and that I recommend.  


  * [The Object Oriented Thought Process](http://www.amazon.com/exec/obidos/redirect?Tag=strictlymovie-20&path=ASIN/0672326116)
  * [Applied Java Patterns](http://www.amazon.com/exec/obidos/redirect?Tag=strictlymovie-20&path=ASIN/0130935387)  
