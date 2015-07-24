---
layout: post
title: "Issues and Comments"
date: 2005-01-27
comments: false
---
Well today I was digging into one of the more important objects that I'm
trying to model in my system; the Issue object. An issue is basically just a
bug or defect report. It has a bunch of small properties and then a long free
text description field. The freetext description also provides the capability
to add attachments such as screen shots, spreadsheets, or whatever you want.
The system currenly only supports one attachment per comment unless you email
the comment in then it will support as many as you provide. This is really
just a limitationof the UI.  
  
Anyway, the problem I am currently facing has to do with the issueDAO and what
to do with the comment and attachment(s). Currently, I am taking care of the
saving of the issue comment within the issueDAO. I have provided a new method,
createComment which takes in an issueBean. The issueBean stores all sorts of
information about the issue. However, it doesn't really make much sense to
keep all of the comment information in the issueBean. At first I thought it
did, and while I was mucking around with some code mockups it still did -
though the clunkiness was definately becoming apparant. Now, though, mostly
because of this post I have come to a new conclusion.  
  
  
I think I need an entirely new object to represent the comment. Since comments
are potentially editable (only if the project lead turns that feature on
within the project; and then only by the author of the comment) and because
they themselves have many properties such as date added, posted by user id,
description, attachments, and of course the comment text itself. So now I will
be adding a new object to my model - Comment. This will of course necessitate
the addition of commentDAO and potentially commentDAO_mssql and
commentDAO_orcl.  
  
Now, one thing I'm currently doing when I model an object; since almost
everything I am doing involves CRUD methods, is to just create a bean
representation. So for this new object I need a commentBean. I am typically
only making objects like Issue and Project which are kind of Facade objects;
except they might have some association logic going on in them. At a certain
point I need to work my way up to the business layer and that is what these
Facade objects are for to me - they are the middle ground between my data
layer and my business layer. Kind of a landing that I can rest on as I travel
between the two.  

