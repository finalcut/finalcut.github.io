---
layout: post
title: "Are Getters and Setters Evil?"
date: 2005-08-05
comments: false
category: coldfusion
tags: [patterns,dao,oop]
---
I don't know if you have seen [the articles by Allen
Holub](http://www.javaworld.com/javaworld/jw-09-2003/jw-0905-toolbox_p.html)
or not but he thinks getters and setters are bad. Not always mind you, but
most of the time. I am not going to repeat his arguments here but rather
discuss my own thoughts about how those arguments apply to CF and the [oft-
discussed bean CFC](http://www.mail-archive.com/cfcdev@cfczone.org/).

Personally, I hate writing all the getters and setters. That's why tools like
[Peter Ferrel's bean generator](http://rooibos.maestropublishing.com/) (and my
lite-version bean-builder) exist. However, they don't really obviate the need
for getters and setters, they just make writing them easier. Holub suggests
that I shouldn't even need them.

Supposedly, the get/set idiom was designed in Java to identify private
properties of the class and were never meant to be called. Supposedly, the
getters and setters reveal too much implementation detail because they are
typed. What happens if the type changes in the future then everything that
calls those getters and setters might have to be updated. This logic, to me,
seems pretty dead on. Granted, CF isn't that strongly typed (for instance an
int and a long are basically just CF strings that only contain numeric values
so minor changes like that won't cause any problems in CF).

Almost all of the instances where I see accessors methods are in the Beans
that folks pass between their data access layer and their presentation or
business layers. They are basically just glorified structures that have some
validation built in. So, what is a developer to do when the data in that bean
needs to be accessed by the data access object (DAO) for initialization or
when it needs to be accessed by the view for display?

Typically, with the DAO I don't need the setters to populate my newly
instantiated Bean. I build a struct and then pass that struct into the init()
method. The init method then takes care of populating all of the necessary
private properties. It is the getting of the data that could be troublesome
without "getter" methods.

There are really only two types of getting that I can think of. 1. The
requester needs the specific data value for some operation (writing to the db,
or using it in a method) and 2. displaying the value (in the UI).

Holub says that in a well designed system...

> You may not ask for the information you need to do something. Rather, you
must ask the collaborator who has the information to do the work. It's okay to
pass to that collaborator information he needs to do the work, but keep this
interaction to a minimum.



So, to accommodate this "rule" when you need the data value, say for saving to
a DB, you should ask the bean to save (or to update, populate, or delete
itself). At this point the bean will call the DAO and PASS the data to the
create or update method. The whole bean shouldn't be passed to the DAO. The
DAO should specify the data types it requires to be compatible with the data
layer and the Bean should live up to that interface when passing the data to
the DAO. This is a pattern that should be easy for any CF developer to work
with and seems totally reasonable to me.

Solving the issue of having the bean do something with it's data we now need
to display it. Holub has a novel idea of giving the bean a "drawYourself()"
method. Now, I don't know if that means he thinks it is OK to have a "drawX()"
and "drawY()" method within an object; but I think that i what he means. So,
if I am dealing with a user profile that has the properties "userID, userName,
firstName, lastName, emailAddress, password" that there would be a draw()
method for each property that needed to be presented in the UI. This method
would be responsible for creating the corresponding HTML object and passing it
back to the caller.

At first glance this seems like both a crazy bad idea, and a good idea. If
some property within my object changes drasticly to become more complex - then
telling it to draw itself would only require me to update my code in one
place, even if I were showing that property in many places throughout my UI (a
very good thing). However, it also seems to plug some of my presentation layer
into the business layer (or does it? The presentation layer takes this
returned HTML object and puts it where it should be in the page hierarchy).

While I like the idea of only updating my presentation in one place (well
probably two thanks to CSS which I would probably be updating as well) the
fact that I use CSS that makes me realize it isn't a simple "drawX()" method
that is needed. In order for it to be flexible the draw method should take in
a "class" or "style" argument that can be applied to that particular drawing
instance. It also seems to me that the method should take in an option if it
should draw an HTML control or not (say in a read only situation it is really
just drawing the text representation?)

Maintenance at this point would probably be easier. My final view page would
look just like it always has - a dump of all the sub-views I have built - but
the sub-views would be a bit different. In the following examples imagine each
method takes to arguments "drawControl:BOOLEAN:DEFAULT=0 and
class:STRING:DEFAULT=''"


```cfc
...
<cfscript>
myobject.drawFirstName(1,"");
myobject.drawLastName(1,"");
myobject.drawUsername(1,"");
myObject.drawEmailAddress(1,"");
</cfscript>

...

```



as opposed to

```cfc
...
<input type="text" name="firstName" value="#myObject.getFirstName()#"
id="txtFirstName" />
<input type="text" name="lastName" value="#myObject.getLastName()#"
id="txtLastName" />
<input type="text" name="userName" value="#myObject.getUsername()#"
id="txtUsername" />
<input type="text" name="emailAddress" value="#myObject.getEmailAddress()#"
id="txtEmailAddress" />
...

```


I admit this is a pretty strange way of looking at CF development in general
particularly in regards to Beans. What do you think?
