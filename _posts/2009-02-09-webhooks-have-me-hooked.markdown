---
layout: post
title: "Webhooks Have Me Hooked"
date: 2009-02-09
comments: false
categories:
 - webhooks
 - webservices
---
Today, of all days, I have been inundated by discussions concerning webhooks.
First I saw [this post over at Jon Udell's
blog](http://blog.jonudell.net/2009/02/09/a-conversation-with-andy-singleton-
about-distributed-software-development/#) where Andy Singleton mentions how
great webhooks are. Then, a little later, I saw a [post by Timothy
Fitz](http://timothyfitz.wordpress.com/2009/02/09/what-webhooks-are-and-why-
you-should-care/) about webhooks linked on reddit.com  
  
It seemed clear that I should investigate and I'm glad I did. Webhooks are,
really, a no-brainer. As one person described them they are "triggers for the
web" - an analogy that only makes sense if you're familiar with databases but
apt nonetheless.  
  
So, you've made it this far but don't feel like reading the linked articles?
No problem, I'll tell you what webhooks are.  
  
Let's say you have an application, oh - i dunno, like this blog. On the blog
you do a few different things but the most common action is to post a new blog
entry. Blogs have actually long supported the idea of a webhook but you may
not have realized a "ping" was a webhook. Basically, what happens is that when
you publish a new post a separate http call is made to the aggregator site. A
ping is super simple - it just calls the url with a special parameter and the
receiving server then knows your blog, specifically, was updated.  
  
However, any RESTful service could be the target so that when you do an action
on your application an http call to the REST service, along with some properly
formatted XML, could be made and bam some entirely new process might be set
off.  
  
Let's say you run a small theater and you use something like MS Outlook to
keep track of your calendar of events. A webhook could be present that sends
that same event off to your online calendar at the same moment for instant
synchronization and publication to your theater's website.  
  
Tim has a more mundane but probably more useful example:  

>  
I imagine a future where twitter feed updates instantly call a webhook. I've
pointed that webhook at a service that does bayesian filtering. The filtering
has been set up to determine if the tweet looks time-sensitive "Anyone
interested in getting dinner tonight?" vs time-insensitive "Webhooks are
cool." Time sensitive posts call another webhook, this time set to sms my
phone. Note that nowhere in this future am I writing any code. I don't have
to.  

  
  
Webhooks have been around for a while but it seems likely that they will
become far more ubiquitous in the future.  
  
Here are some links for further reading:  

  

  * [Webhooks.pbwiki.com](http://webhooks.pbwiki.com/)
  

  * [Webhooks.org](http://blog.webhooks.org/)
  

  * [Webhooks Google Group](http://groups.google.com/group/webhooks)
  

  * [Uche Ogbuji on Web Triggers](http://notes.4suite.org/Bright_Content:Design:Web_Triggers) written in 2006 but basically the same idea.
  

