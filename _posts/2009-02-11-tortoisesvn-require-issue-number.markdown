---
layout: post
title: "TortoiseSVN : Require an Issue Number"
date: 2009-02-11
comments: false
categories:
 - tortoisesvn
 - bug
 - windows
 - svn
 - issues
 - bug-tracking
---
We are a windows shop and we use SVN as our version control system, so, most
of us use TortoiseSVN as our primary interface to the SVN Server. Being agile
and all we try to create issues for everything and to help enforce attributing
code to an issue we, sometimes, use a nice built in feature in SVN that
provides a limited Bug Tracking System integration.  
  
We actually rolled our own bug tracking solution years ago that serves our
needs fairly well so the references you might see to it in my examples that
will follow should be replaced with whatever your systems conventions are.  
  
Enabling Issue System Integration:  
  

  

  1. Go to the root directory of your checked out project.
  

  2. Right click on the directory and select "properties" from the context menu
  

  3. Select the Subversion tab in the dialog window that appears
  

  4. Click on the "properties" button
  

  5. Add the following properties to your project:  

    * bugtraq:append - true
  

    * bugtraq:label - "Bug" or "Issue" or "Jira" or whatever..
  

    * bugtraq:message - "Bug: %BUGID%" replace bug with whatever you used for the label
  

    * bugtraq:number - true : obviously only select true if you insist your issue numbers are numeric.. for instance a JIRA is alphanumeric so this should be false if you use Jira
  

    * bugtraq:url - http://my.issue.server/showIssue/%BUGID% - this is whatever url you need to load a specific bug, where %BUGID% will be replaced with the value entered by the submitter
  

    * bugtraq:warnifnoissue - true : this will alert the user if they try to commit changes without providing an issue number.
  
  

  6. Click "OK" svn properties dialog
  

  7. Click "OK" on the folder properties dialog
  
  
  
There, you're set up. Now you just need to commit the change to your directory
to subversion. Then, everyone who updates from SVN will have these same
settings and everyone on the project will have the same level of integration.

## Comments

Jim Priest

This is very handy - I find myself much more apt to enter a # when this is
present.  
  
Here's a post I did with a screenshot...  
  
http://www.thecrumb.com/2008/11/25/integrating-jira-and-svn-using-bugtraq-
properties/

Bill

thanks for pointing that out. The field will be labeled with whatever you put
in the bugtraq:label setting  
  
I didn't really think to detail this much more as I was putting the post
together as a quick tutorial for a friend who had already seen my screen  
  
I'll put up a screenshot tomorrow of the modified commit dialog

Marc Esher

Another nice feature is that when you do this, Subclipse recognizes it and
adds a new "Bug ID" type field to the commit screen.

