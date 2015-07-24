---
layout: post
title: "Private Method Injection"
date: 2005-09-15
comments: false
categories:
 - coldfusion
 - ioc
 - dependency-injection
---
I have to honestly say I haven't had a reason to use Method Injection with CF
but yesterday I ran into a post at [Compound
Theory](http://www.compoundtheory.com/?action=displayPost&ID=61) that talked
about the subject and provided some tips. During the article he mentioned
injecting a method into a components variables scope and then said he would
leave that as an exercise for the reader.

Before you go on, if you aren't really familiar with what method injection is
I suggest you read the article at [Compound
Theory](http://www.compoundtheory.com/?action=displayPost&ID=61). He does a
fine job of explaining it.

So I quickly jotted down my thought on how to do it last night and was able to
test it this morning. Suprisingly, it worked. I have two methods of doing it -
but they really both boil down to the same thing.



  1. Start with a public method in the CFC that already does the ditry work of moving the method into the private variables scope


  2. Inject said public method into the CFC first



Here is the method that will help you inject into the private variables scope:


```cfc
<cffunction name="addmethod" access="public" hint="I inject methods into
the private variables scope">
<cfargument name="newmethod" type="any">
<cfargument name="methodname" type="string">

<cfset variables["#arguments.methodname#"] = arguments.newMethod />

</cffunction>

```


Pretty straight forward really. It is as easy to use as it appears:

```cfc
<cfset myComponent.addMethod(someFunction,"someFunctionName") />

```


Where someFunction is actually a defined UDF and someFunctionName is how you
want it referenced in the variables scope.

Can you think of any other ways to inject a method into the private scope? And
finally, why would you want to?

UPDATE:
For anyone that wants to know more about IoC or Dependency Injection, which is
what this whole excerise is about really, Dave Ross left the following link in
a comment:
[Dependency Injection Pattern](http://static.springframework.org/spring/docs/1
.2.x/reference/beans.html#d0)

## Comments

Anonymous

well.. I just came back to this tonight (not sure why - I'm a blog zombie).
Wish Blogger did notifications.

Anyways, Mark, the reason for wanting the lookup-method injection to be
private is that it's only meant to be called by the object it's injected into.
When you give a girl your number you don't want her ugly friend calling,
right? ;)

Bill,

Glad you took a look at the concepts behind IoC/DI. I truly believe that they
help with CFC development, especially for larger codebases. I find ColdSpring
very unobtrusive to work with... you don't really know it's there, but after
you wire together 2 fully configured objects with a mere inclusion of a setter
method, you definitely appreciate its abilities.

-dave ross

Mark Mandel

Why would you want to inject private methods?

Hmnn... depends what you are doing -

Maybe as a helper method for another public method you don't want to be
exposed is one that immediatley comes to mind.

Or if an extending object is expecting that the method will be there - and you
don't want it exposed as public... but that's getting into some pretty
convoluted circumstances.

So you could say it doesn't pop up too often, but it can do.

Glad to be interesting ;o)

In reposnse to DavidR:
This sort of approach can be used to as a 'lightweight' form of inheritence.
Look up Robin Hilliard's usage of mixins.
(http://www.rocketboots.com/blog/index.cfm?mode=entry&amp;entry;=6E1A91AC-E081
-51EF-A796B568EF7FABEA)

Bill

Dave (Ross), thanks for the Link. I had to reread a couple parts (note to
self, don't try to learn this stuff when sleepy).

It makes sense. I didn't really get the part about the Interface Injection.
But the constructor and getter injection both made sense.

And better yet - the point of them - made sense. I'm not sure I have a current
need for this knowledge but it is good to have nonetheless.

Thanks Guys.

Bill

Mark, glad to link to an interesting post.

Just curious though, why do you need to do private method injection? I'm sure
there is a value to it that is just eluding me.

Thanks

Mark Mandel

Thanks for linking me!

I just noticed my site was blocking yours with my referrer spam blocker.

I made sure that wasn't going to be an issue for you now.

As per techniques - I think you've hit the 2 on the head, but I actually have
a CFC that does it all for me. I find it easier that way.

Anonymous

I'd like to implement the lookup-method bean attribute in ColdSpring, which
should be injected as a private method, however there's not *too* much harm in
leaving it public. For background on what lookup-method does, see: http://stat
ic.springframework.org/spring/docs/1.2.x/reference/beans.html#d0e1161

-Dave Ross

David Ringley

I could see using something like this if I wanted to get at the CFC's instance
variables in the variables.instance structure but was too lazy to write a
getMemento() function for each. I could just inject a getMemento() function
into the CFC and call it to retrieve the memento to be used in some type of
TransferObject before passing it to a DataAccessObject to persist. Though, I
am not sure that I would actually do this since this seems rather invasive.

