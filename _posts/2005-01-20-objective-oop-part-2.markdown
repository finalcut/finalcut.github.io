---
layout: post
title: "Objective OOP: Part 2"
date: 2005-01-20
comments: false
category: coldfusion
tags: [oop]
---
Yesterday I talked about my ProTask dilemna concerning what objects to create
and how to break my system down into logical parts. After writing about it - a
very helpful exercise - and then talking about it with some coworkers I am now
leaning toward a different setup, of sorts.

I think there will be two objects that can be created within the application
code: Projects and Project. When I want to create a new project I will can
Projects.newProject(); which will return a reference to a Project.
Projects.cfc will also have methods for getting collections of Project.
Overall it will be a fairly simple object.

Project on the other hand will be my main entrypoint to all other objects.
Basically, there is no User without a Project. There is no Issue or Priority,
Area, or Category without a Project. Because of that if I want to associate a
User with a Project I will first call Project.newUser() which will return a
UserBean - I will populate this and then call Project.AddUser(userBean).
Project.AddUser will then be responsible for invoking the correct other
objects/methods to accomplilsh its mission.

Project.AddUser() will probably look something like this:


```cfc
...
projectGateway = createobject("component","components.projectGatewayFactory");
projectGateway = projectGateway.init(variables.projectID);

projectGateway.addUser(arguments.userBean)
...

then projectGateway.addUser() would probably look like
...
<cfquery datasource="#request.dsn#">
INSERT INTO project_user (
project_id,
user_id,
role
) VALUES (
<cfqueryparam cfsqltype="CF_SQL_INTEGER"
value="#variables.project_id#">,
<cfqueryparam cfsqltype="CF_SQL_INTEGER"
value="#arguments.userBean.getID()#">,
<cfqueryparam cfsqltype="CF_SQL_VARCHAR" value="Project Lead">
)
...
</cfquery>

```


Basically this same type of setup would happen for all the different objects.
This would, I believe, make life easier for anyone building new functionality
into ProTask as well as if I want to provide webservices etc. I only have to
provide remote access to up to two objects and the entire system will be
available remotely. It seems like a good way to go to me at the moment. What
do you think?
