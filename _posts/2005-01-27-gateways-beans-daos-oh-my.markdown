---
layout: post
title: "Gateways, Beans, DAOs - Oh My!"
date: 2005-01-27
comments: false
categories:
 - factories
 - daos
 - coldfusion
 - patterns
 - beans
 - design patterns
 - gateways
---
Today I progressed (or regressed; it seems I may never know) in my OOP/Pattern
approach to developing ProTask. First off I consolidate a whole slew of
gateway objects into one gateway. I also made some decisions that kind of go
against my initial understanding of what a DAO is all about. And, finally, I
starting crafting a big facade object that will probably not exist in any form
resembling itself when I am all done.  
  
  
Let me give you a rundown of the "base objects" that I am dealing with before
I start into what methods I'm putting where and why I'm doing it.  

  * Project - this is really the core of the whole system
  * Issue - a project consists of one or more issues. These are basically bugs or defect reports and there can be any number of them.  

  * Area - Issues are categorized by areas. There can be any number of areas
  * Milestone - Issues are further categorzied by Milestones. There can be any number of milestones.
  * Priority - yet another categorization of Issues. There are always 10 priorities per project - they can be edited
  * User - people who can submt or be assigned Issues. Currently these are provided via an external system titled KD (that currently shares the same schema).
There are actually a few other categorization methods as well but these five
basic objects are enough to illustrate the rest of my thoughts so far.  
  
At first I started off creating a DAO for each of these objects as well as a
gateway for selecting multiple instances of each item I also have a bean for
each object. In fact there are actually three DAOs for some of the objects
(Area, Milestone, and Project) but only one DAO for the others (issue,
priority). The reason for this disparity is due to the different database
backends I support (Oracle and MS SQL). So basically I have an objectDAO as
well as two subclasses: an objectDAO_mssql and an objectDAO_orcl for those
objects that need it and just an objectDAO for those that don't.  
  
To give a touch more background information about the DAOs since they are the
most prolific object I am coding for at the moment I also have a DAOFactory
and two other DAOFactory subclasses; DAOFactory_mssql and DAOFactory_orcl.
Now, when my system needs a DAO I instantiate the DAOFactory and pass in the
database type (sqlserver or oracle) and it returns to me an instance of the
appropriate subclass. This I can then call getObjectDAO on the factory and get
the corresponding object. So there is a getProjectDAO method and so forth. For
example, if I want the projectDAO for a oracle database I might do the
following:  
```cfm  
<cfscript>  
dao =
createObject("component","protask.daofactory").init(request.dsn,"oracle");  
<!--- I now have an instance of protask.daofactory_orcl --->  
dao = dao.getProjectDAO();  
<!--- dao is now an instance of projtask.project.projectDAO_orcl --->  
</cfscript>  
```  
  
projectDAO_orcl is a subclass of projectDAO. In projectDAO I defined all of
the methods that are the same across both database backends (update and
delete) and then in each database specific dao I define the methods that
change based on the database (create and read). Overall, this works pretty
well and is exactly what I had hoped for. As far as I can tell this system
won't be changing as I further develop the system. In the past when I had
queries that changed based on the database type I had some  clauses embedded
in the query. It made for difficult to read queries (mixing syntaxes within a
single cfquery tag) and didn't seem very elegant; especially when dealing with
very complicated queries. This DAO inheiritance looks to work perfectly and
will make maintaining each databases queries much easier.  
  
Now, as I mentioned in my prior post not everything was perfect. For instance
when I delete an area using the areaDAO where do I remove the references to
the area? Well, for now I have decided on doing it within the areaDAO. I made
this choice because it is the most logical place for the extra query. The
query is exactly the same across platforms and is really only a rule due to
data integrity concerns. I absolutely can't delete an area while an issue
still references it and so I delete the references at the same location as I
delete the area. I am about 99% confident in this decision but, presented with
a better solution, I am willing to change it if I should.  
  
While reading the cfc-dev mailing list today a fellow poster suggested that
objects that only exist because of the existance of another object can, and
perhaps should, be dealt with in the required objects DAO. I'm not totally
sold on that idea yet - but I do think it is a good idea for pretty much every
gateway method I had defined. Earlier today I had a gateway for User,
Priority, Area, Issue, etc. Each of these gateway objects had methods like
getAreasInUse or GetAreas and each took as an argument the projectID. After
much deliberation I decided that these queries should all be in the
projectGateway. So far all of the queries in the projectGateway are the same
regardless of the database used. However, if I start having to add methods
with special query considerations I will end up using the Factory pattern
again just like I did with the DAOs. I think combining all of these gateways
into the projectGateay makes alot of sense. First off, all of the methods are
in one easy to find location. Second, whenever the business layer needs any of
the property groups for a project it can always go to the projectGateway
instead of having to go here, there, and everywhere just for read methods.  
  
Finally, I started to create a project facade object. This project facade
exposes alot of methods. To start with it has all my "bean builders" so that
when I want to create a new project or a new issue for a project (or area or
milestone) I can just call project.newProject() or project.newIssue(). Now,
while these seem like a decent idea I'm not totally sold on it yet. I
definately want a facade so that my system isn't having to worry about all
these different objects but still have the power of them all. Now, I may end
up needing to have more than one facade object - but at the moment I am
reluctant to do so. However, I am doing my best not to lock into any one plan
yet. We will see what happens.  
  
Overall this is a bit harder than I expected. I can read, read, read all I
want but, like most things it is in the doing that I learn the most. However,
I think having a mentor with this stuff would definately speed me along the
path to full comprehension. It isn't that I don't understand the concepts -
but rather when and how to apply them. The cfc-dev list is sort of helpful as
there are a few people who have already mucked with this stuff before and come
to some kind of greater understanding; yet, I don't really feel it is enough.
To be honest, I'm not experimenting with the best language. However, the
subset of OOP functionality that Coldfusion provides may be for the best since
I don't have as much to learn.  
  
Once I finish rewriting ProTask in the fashion that I am going now I will
write it again as jTask - a full blown java application using struts. Why
struts? Well, I like the whole implicit invocation idea (same with mach-ii in
the coldfusion land). and I think struts makes alot of sense. Who knows what
I'll think once I actually try to port this baby.  
  
As always feedback is both welcome and desired. Let me know what you think!

