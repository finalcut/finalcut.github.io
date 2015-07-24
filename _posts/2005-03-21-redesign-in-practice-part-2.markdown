---
layout: post
title: "Redesign In Practice - Part 2"
date: 2005-03-21
comments: false
categories:
 - coldfusion
---
In my last post I talked about ProTask (an issue management system) and, sort
of, covered how it was designed during its first two iterations. In this and
any subsequent posts on the topic I will discuss the design as it stands
currently, why I have made some of the decisions I have made, and where I am
still stuck as far as design decisions go (and why I'm stuck).

In my last iteration there were seven CFCs in the entire application and they
each contained way more logic than they should of - there was no real
separation between the business layer and the data storage mechanism or from
the KD framework for that matter. If an action seemed like it was primarilly
associated with one or more instances of one of my seven objects that is where
method went. It wasn't the best process for vetting out my system methods -
but I didn't know what else to do.

Now, however, things are cleaning up quite a bit. There is still some
confusion on my part - but overall things are looking much better. Today I am
just going to discuss a couple broad topics then I will narrow my focus in
subsequent posts. As a convetion my objects will be in ALL CAPS.

My first decision was that I do not want any front end to have to know too
much about all of these different objects. In fact, if I can help it I want to
have one simple facade to the whole underlying system. I believe this will
work (almost) considering the current scope of the application. Basically,
when someone interacts with the system they are dealing with one PROJECT at a
time. A PROJECT consists of zero or more ISSUEs, zero or more AREAs, zero or
more BILLING codes, ten PRIORITY(ies), and zero or more MILESTONEs. Since you
can not create any of the sub items without having a PROJECT first I don't
expose any of their methods publicly - just on a package level. To facilitate
this I have a big [facade](http://java.sun.com/blueprints/corej2eepatterns/Pat
terns/SessionFacade.html) object titled project.cfc. I will probably end up
renaming this as it ended up conflicting with my
[bean](http://c2.com/cgi/wiki?BeanPattern) object naming.

Initially I had planned on calling my beans something like projectbean.cfc and
issuebean.cfc but that quickly grew tedious so I went back and renamed all of
them to just issue.cfc, area.cfc etc.. except projectbean.cfc which I haven't
renamed yet due to my project facade object. I suppose I could name the
project facade projectfacade.cfc but that seems pretty clunky to me. I will
come up with something better.

I mentioned that this project facade would almost work for hiding all of the
complexity of the system design from the user while still exposing all of the
functionality he/she might need. The problem arises when you are trying to get
a view into many PROJECTs to see some simple statistics on the ISSUEs in that
project. For instance with our KD portal we have a view that shows how many
ISSUEs are bugs, questions, features, or tasks in PROJECTs that the current
person is a USER in. My project facade deals with a single PROJECT (it takes
an optional projectID as part of it's initialization).

Therefore there is also a projects.cfc which is a facade as well. It gives you
some access to very limited information about mutliple projects and can also
return to you an instance of my project facade class. So, right now to use the
system you have to initialize one object:


```cfc
myProjects = createobject("component","com.sbcs.protask.projects").init(reques
t.site.datasource,request.site.databaseType);
```


_request.site is a structure currently defined by our KD framework that holds
a variety of configuration information including the database type and the dsn
name (datasource)._

If you want a specific project facade you just call


```cfc
thisProject = myProjects.get(attributes.projectID);
```


Those two initializtion paramters of datasource and databasetype are used
within the system to determine what [composite objects](http://java.sun.com/bl
ueprints/corej2eepatterns/Patterns/CompositeEntity.html) and what [DAO objects
](http://java.sun.com/blueprints/corej2eepatterns/Patterns/DataAccessObject.ht
ml) to use - I'll get into those areas in a later post.

the project facade object really does very little beyond managing the calls to
the appropriate decendant objects for processing. However, I do have one
method that is floating in there currently that I can't figure out where it
goes: determineIssueStatus. It takes in the following parameters and based on
this information determines what the status of the ISSUE should be:


```cfc
<cffunction name="determineIssueStatus" access="private" output="false"
returntype="com.sbcs.protask.issue.issue" hint="determines the status for an
issue">

<cfargument name="issue" type="com.sbcs.protask.issue.issue"
required="true" hint="the issue to evaluate" />

<cfargument name="user" type="com.sbcs.protask.user.user" required="false"
default="#arguments.issue.getAddedBy()#" hint="the user performing the current
action" />
<cfargument name="approved" type="numeric" required="false" hint=""
default="0">
<cfargument name="accepted" type="numeric" required="false" hint=""
default="0">
<cfargument name="open" type="numeric" required="false" hint=""
default="0">
<cfargument name="locked" type="numeric" required="false" hint=""
default="0">
<cfargument name="resolved" type="numeric" required="false" hint=""
default="0">
```


I don't think it belongs in a gateway (to be honest, I may have gateway and
composite object naming mixed up or at least the functionality mucked together
into one composite gateway object) as they deal with multiple records and I'm
only working on one issue. I don't think it goes in a DAO because it doesn't
touch the data layer at all. I know it doesn't really fit in the project
facade - but until I can come up with a better place for it that is where it
will sit. About the only place I can think of that might, and this is a big
might, be better for it currently is in the issue bean. However, I don't think
the bean should really be determining anything - it just holds data (and
perhaps validates it) but it shouldn't be computing anything that I know of.

Another area that I keep bouncing around on currently is the file structure of
my CFC collection. As you can see from the arguments I have shown I store them
under the com/sbcs/protask directory. However, I currently plop each in a
directory that applies to the object as well - so there is some redundancy in
the calling of the bean objects such as com.sbcs.protask.user.user. I may
change that so that they are all in the same root directory later. Currently
the only cfc's in my root com.sbcs.protask directory are projects.cfc,
project.cfc, daofactory.cfc, and gatewayfactory.cfc. You'll notice I did add
the pattern name to the factory objects and that is because that makes sense
to me. I also add DAO to plain dao objects. However, plain gateways dont have
the word gateway in their name. For instance one gateway is projectissues.cfc
which deals with many ISSUEs within a PROJECT.

One drawback to my current setup - and I really don't view it as much of a
drawback - is that I have a very large number of methods in my project.cfc
(the facade object). Alot of these methods map directly to a method in one of
the dependant classes so that my project.cfc method just consists of lines
like:


```cfc
<cffunction name="getUserIssues" access="public" output="false"
returntype="query">
<cfargument name="userID" type="string" required="true" />

<cfreturn variables.instance.issues.getAssignedTo(arguments.userID) />
</cffunction>
```


The reason I don't consider this a real drawback is because the API for anyone
else is very simple. They only have to know about the methods exposed via
projects.cfc and project.cfc. They never have to worry about instantiating any
other object as project.cfc will generate new, empty single instance objects
for everything they might need to directly interface. The only objects beyond
projects and project that expose their internal methods are the bean objects
which expose all of their getters and setters.

The exposed getters and setters will probably be modified in the future to
support the use of a [transfer object](http://java.sun.com/blueprints/corej2ee
patterns/Patterns/TransferObject.html) where applicable as it seems there will
be less overhead in using them, especially when dealing with the display of an
objects data (calling multiple getters on an object).

