---
layout: post
title: "basecomponent.cfc"
date: 2005-11-07
comments: false
---
In a recent newsletter from Hal Helms he discussed having a component that all
of his other components extend. I have been doing this for a while and I think
it is a pretty good idea in general because I almost always want these
individual methods in "all" of my CFCs. Granted, there are some that don't
really need the methods but the are pretty generic utility methods and so for
now they sit in my basecomponent.cfc

Admittedly some of them are pretty much only pertinent to "bean" type
components. That is those components that have a stateful representation of
data. I have debated having a baseComponent.cfc and a bean.cfc that extends
baseComponent.cfc and then have all my beans extend bean.cfc - but I haven't
been willing to add the intermediary step to my inheiritance chain yet.

Basically the way I do things is any object that doesn't have a "super" by
definition automatically extends my baseComponent.cfc

Here are the methods in my baseComponent:


properties..(not a method)


Pretty simple just creates a struct variables.instance and calls the "setUUID" method

setUUID


stores a readonly UUID for the object. Useful for object comparision

getUUID


fetches the objects UUID

equalTo


Compares the current objects UUID to a passed in objects UUID

getMemento


A fairly robust getMemento method that expands any children objects into their memento forms as well. Uses a private method copyMementoStruct recursively

copy


Makes a full copy of an object including its composite objects. Uses a private method copyProperty recursively

dump


Dumps the objects memento to show the object's current state and optionally aborts



Obviously the Memento stuff is what I was talking about when I said it doesn't
all fit EVERY object, but I don't think the overhead of these few methods is
that big a deal.

If anyone would like a copy of this CFC just let me know and I'd be happy to
share.

## Comments

Bill

Puc,
If you want to give me an email address (you can email me at bill.rawlinson
using gmail) then I'll send you a copy of my "BaseComponent.cfc"

Sorry it took so long for this reponse.. I just now saw your comment awaiting
moderation.

Puc

Hi Bill,

I am trying to create a base component like this but I'm having difficulties.

Could I get a look at your basecomponent to see where may be going wrong.

Thanks

Mike

Hi Bill,
I'd really like to see what you are doing in your base cfc. I've got a problem
with one of my projects where I've got a deep nesting issue that throws an
error intermittantly. I'd like to see if your memento and uuid comparison
functions might help me diagnose the problem.
Thanks.

