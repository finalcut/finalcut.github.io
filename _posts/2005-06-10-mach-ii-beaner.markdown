---
layout: post
title: "mach-ii beaner"
date: 2005-06-10
comments: false
category: coldfusion
tags: [mach-ii,oop]
---
A few months ago I was turned onto a tool called the mach-ii beaner. It is a
very handy tool for quickly creating CF based beans. However, it had a couple
small failings. Nothing that has kept me from using it; but enough that they
tickled the back of my mind until I addressed them.  

The mach-ii beaner is the result of the hard work of Jon Block initially and
then added onto by Peter Farrell. I'm not sure how much extra Peter added
because I have never seen Jon's initial copy. Needless to say I owe them both
a big thanks for saving me TONS of time. However, as I said there were some
small issues I needed to address with the copy I got from Peter in March of
this year.  

Today I addressed those issues. I did nothing major, however they save me just
a bit more redundant typing, and they remove a potential bug that could creep
into your resultant bean.  


  1. updated numeric types to have a default of 0 instead of ""
  2. added support for a "date" type. This is CF MX 6.1 support. I will explain more in a second
  3. added support to add a dump method
The CF MX6.1 date support is kind of tricky. Bascially I fudge it. There is no
type="date" in CFMX 6.1 (that I know of). However, there are a lot of times
when I need a field to hold a date. When that field receives a date I always
want it to be formatted one way or another.  

So, what I did was let you type in date for your type while defining your bean
template. Then, when outputting the bean I replaced "date" with "string" when
appropriate (such as type="string") but during the setter, if you defined a
date format for me to use I added a little conditional.  





Then the setter just does what it always does.  

Finally I added the dump method. It takes in an optional abort parameter. If
you call yourobject.dump(1) it will dump that objects variables.instance
struct AND then cfabort. Drop the 1 (or change it to a 0) and it won't abort.  

I'm not sure if I am allowed to distribute this file. I haven't talked to
Peter or Jon yet. However, if I can I will let you know and I will put it on
the web for your downloading pleasure.  

For the time being you can always check out:  

  * [Jonathan Blocks Site](http://www.jonathanblock.com) (origional author)
  * [Peter Farrell](http://blog.maestropublishing.com) (first modifiers site)

## Comments

Anonymous

Hi Guys,  

This is great I'm very happy the Bean Creator is saving you all the painful
process of rewriting. In my opinion, each developer has their "own little way"
that they would want the bean creator to work for them. Personally, the way
mine works exactly matches the way in which i interact with beans and CFC's.
Modify and redistribute as you wish.... just don't forget about me when you
become famous. ;=)  

Cheers,  
Jon

Peter J. Farrell

I released version 2.1 of Rooibos Generator today (9/14/2005) with a couple
new features as well as an improved JS code base.  

You can check it out here:  
[Rooibos Generator](http://rooibos.maestropublishing.com)  

Best,  
.Peter

Bill

On July 14th Peter Farrell released an updated version of it including my
changes (for date and default numeric values, and maybe the dump method as
well). He probably added a bunch of other stuff too - I know it looks better!  

You can check it out here:  
http://rooibos.maestropublishing.com/

Anonymous

Hi Bill,  

Any updates on the release of the new [Rooibus] beaner?

Peter J. Farrell

I forgot to add that Jon came up with the idea and implemented it with basic
getter/setter name and it's type. I added all the extra checkbox options as
well as the LTO support, allowing defaults, bean/LTO paths and the method that
shows an example bean with a button.  

Best,  
.Peter

Peter J. Farrell

Hi Bill,  

Thanks for the blog entry. If you send over the file, I'll happy merge them
into the beaner. The beaner needs a little work - especially the javascript.
Hopefully when I get a chance, everything will be fixed in the next update.
The new beaner will be called Rooibus ("roy-bus"). Thanks for the input - so
far I like the ideas.
