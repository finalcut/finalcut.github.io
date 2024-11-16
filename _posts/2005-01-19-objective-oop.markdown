---
layout: post
title: "Objective - OOP"
date: 2005-01-19
category: Programming
tags: [oop,aop]
comments: false
---
While, nowadays, Aspect Oriented Programming (AOP) seems to be all the rage I
am still trying to master OOP, or Object Oriented Programming. I fully
understand the concepts and can typically break down simple systems into their
corresponding objects without much hassle. However, once I try to model more
complex systems with greater interaction between the objects - I oftentimes
become stumped. Well, maybe stumped isn't the right word - but I do get
stopped. You see, the problem is I'm not always sure if, or when, to create a
new object when I am actually managing relationships between two or more other
objects. Before I begin to babble I'll present you with an example from a real
project I have worked on (and infact I may never stop working on).

I created a defect tracking system titled ProTask that we use internally at place of
employment. Overall it's a pretty slick application whose simplicity was
inspired by FogBugz (ala Joel on Software). While the two products differ in
many ways my approach when building ProTask was guided by the design goal of
FogBugz - simplicity. So, from a Human Computer interface perspective ProTask
is done - it is feature rich and easy to use. Unfortunately, it is once you
dig deeper into how the system works that much remains to be done.

ProTask is
composed of a few different entities: Projects, Issues, and Users. A Project
is a collection of Issues and Users. An Issue is a collection of smaller
objects such as Priority, Category, Area, and User. Most of the objects are
pretty simple; specifically the Priority, Category, and Area. They are
basically just id, value pairs.

However, the three main objects, Project,
Issue, and User are each much more complex and it is the relationship between
them that I have encountered problems. If I didn't have to worry about
managing Issues and Users then my Project object and all of its supporting
functionality would be a snap. However, a project with no real properties
wouldn't be worth much would it?

So instead I have to associate users (with
different roles) to the project, and then these users can create issues that
need to be tracked/handled by at least one user of the project. Now, to
illustrate what I am doing currently I'm going to simplify a Project to being
just an id, value pair that is associated with one or more User (which is also
an id,value pair) and an Issue (which is an id, value, and user). When a user
creates a new Project they are automatically associated with the Project as a
user with the role "Project Lead".

Sounds pretty simple doesn't it? Ok, well
the first thing I want to do is create a project object. Since I'm doing this
in ColdFusion I create project.cfc which might contain a few different methods
associated with a project. What those methods are I'm not sure of yet but
there will probably be some.

Now, I really need, and want, to modularize this
application because right off the bat I have the requirement that it MUST work
on both MS SQL server and Oracle so all the database stuff needs to be
abstracted into some other object. For this I figure I will use a data access
object (DAO) called projectDAO.cfc.

Since this is a DAO it will just handle
Create, Read, Update, and Delete (CRUD) a single row from the project table,
p_prj. Also, since I am dealing with multiple database types I will probably
need a project DAO factory that creates an instance to the correct database
DAO when I need it so I will call it projectDAOFactory.cfc Fun, isn't it?

So already I have project.cfc (which has no methods to speak of yet),
projectDAO.cfc which contains four methods, and projectDAOFactory.cfc which
contains the method of giving me the right projectDAO.cfc. Now, I need an
object that can represent just the properties of an object - maybe have some
business validation rules in it - like confirming that the project name isn't
too long to fit in the database etc.

Borrowing from the land of Java I figure
this could be the projectBean.cfc which has a bunch of getters and setters to
initialize the project Bean. Ok this is starting to make sense right? So now,
if I want to create a project that I will save in the database I instantiate a
projectBean, set its title value then instantiate the projectDAOFactory.cfc
which I can then call to get a reference to the correct projectDAO.cfc.

Using the projectDAO.cfc I can pass in the projectBean I created before and have its
data saved to the database. The projectDAO.cfc can then call the
projectBean.setID method and return the bean to the caller.


```cfc
... thisProject =
createobject("component","components.projectBean");
thisProject.setTitle("Some Project Title");
projectDAO = createbject("compoent","components.projectDAOFactory");
projectDAO =projectDAO.getDAO();
thisProject = projectDAO.create(thisProject); ...

```


Great, I am feeling pretty good with this so far. OK - so now I need to
associate the current user with the project as the projectLead. Hrm, do I need
to create a new object ProjectUser.cfc that deals with these things - or
should this functionality be dumped into project.cfc? OPTION 1: My initial
inclination is to create a new object; but then don't I also need to create a
bunch of other objects to go with it? And then what about later when I want to
add priorities, or areas, or categories to the project. Do I need to create
new ProjectPriority, ProjectArea, and ProjectCategory objects and all the
supplemental objects I might need?

Sometimes, I'm just not sure what the
"right" answer to this problem is. So I stop working. I think, and think, and
think, and think somemore about what to do - what is the right path? OPTION 2:
Should I create my super object, project that works in conjunction with
projectGateway.cfc (for all the other database stuff) and
projectGatewayFactory (so I have the right gateway for the db I am working
with)? Even as I write this I debate back and forth. There are pros and cons
to both of these tacts.

For example with Option 1 each of the smaller objects
is completely independant from each other. Priority methods aren't even in the
same file, ever, as user methods. However, I now have a bunch of small very
specific files to maintain. I guess that could be viewed as either a plus or a
minus depending on how you look at it. In Option 2 I have only one real
interface that the rest of my application has to worry about when creating
relationships with a project, the project.cfc - the code through the app will
be very concise and there will be fewer objects (but one bigger one) in memory
at any given time. So what would you do? Would you go with either of these
options or would you do something completely different? I'll let you know what
I do. To be continued....
