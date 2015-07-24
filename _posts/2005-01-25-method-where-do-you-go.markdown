---
layout: post
title: "Method - Where do you go?"
date: 2005-01-25
comments: false
---
I'm still working on ProTask and have a bit of a condundrum as I rearchitect.
I have a project object and a user object. Both of these have a gateway object
available to them. Now, the question that presents itself to me is where does
the following method go?  
  
"get all projects that a specific user is a member of"  
  
My initial inclination was to have the userGateway take care of this since I
am passing in the userID - however, I am basically just trying to get Project
information so it seems like it fits better in the projectGateway.  
  
Within ProTask there are also Issue and Area objects. An area is basically
just a way of categorizing an issue. A project can have n Areas defined -
however an Issue can only be categorized by one (or zero) Areas. You can also
delete an Area that Issues are associated with without deleting the Issues -
basically the Area reference is just removed before the Area is deleted. Now,
I have an issueGateway an areaDAO. Where does the query that deletes the
references go?  
  
My initial inclination is to put this extra query in the areaDAO in the delete
method. It violates the letter of the law on DAO objects it seems but does fit
into the spirit of the method. It isn't as if I am putting business rules into
the data layer. Instead I am enforcing a data layer rule where it most makes
sense.  
  
Where do you think these methods should go? Should the getUsersProjects method
go in the projectGateway? And should the deleteAreaAssociation query go in the
delete method of the areaDAO?  

