---
layout: post
title: "Redesign In Practice - Part 1"
date: 2005-03-19
comments: false
category: programming
tags: [oop]
---
ProTask is an issue management system that was initially developed as "the
issues system" It was a very clunky, very poorly designed system. It isn't
very clunky anymore but it is still fairly poorly designed. Initially it was
developed by a new hire who was still in
[University](http://www.marshall.edu/) \- he was faced with the limitations of
learning a new language while building the application, learning the
[KnowledgeDispatch](http://knowledgedispatch.com/) (KD) framework, and working
in relative isolation. All of this lead to a system that was both unusable and
one that was never really finished.

However, as an organization we still needed to use it. Every software
development project benefits from an issue tracking system. I can't imagine a
succesful project without one. Instead of griping and complaining about our
issue tracker I decided it would be best to just rewrite it. KD is implemented
in ColdFusion and one requirement was that our issue tracker needed to
integrate with KD - and that we needed single sign-on between the two.

[ColdFusion MX](http://www.macromedia.com/software/coldfusion/) was just
released so I decided to develop ProTask (as it became called) with MX and to
attempt to use CFC's. To be honest, I didn't fully understand the capabilities
of CFCs and there were many, many silly learning mistakes I went through in
the process. For instance I learned not to name a variable the same as an
other method and to var scope my variables (including query names). However,
during this initial redesign I never knew about the variables scope within a
CFC - so my CFCs methods were all far more complicated than they needed be and
basically each CFC was just a function library.

I also didn't know anything at all about [Design Patterns](http://www.amazon.c
om/exec/obidos/redirect?Tag=strictlymovie-20&path=ASIN/0130935387) nor how
they could be applied to a ColdFusion application. I had heard about Design
Patterns but only in the context of Java and since I wasn't working in
[Java](http://java.sun.com/) at all at the time I didn't focus much energy
towards learning them. That was a mistake.

Not all was a loss however, in the end my attention to the UI of the
application was sufficient to overcome the shortcomings in my architectural
design. Once the UI was cleaned up, simplified, and actually made usable we
had much better buy in by the rest of the development staff.

The architectural design wasn't horrid either - it just wasn't good. There was
still some good to take from it. First off I did identify the major objects
that are a part of the system. I also had a decent initial cut at where the
various methods should go in relation to said objects. The design of each
object as far as it's contained methods definatly still needed some work - but
thankfully this is an iterative process and I knew I wasn't done.

Here were my objects:



area



An area is a category within a project. An issue can be related to a single area. I used area instead of category because there are four constant categories per project; bug, feature, question, and task. Areas can be added and removed from a project as well as modified. They are basically just a label.

activity



an activity is a subcategory to billing. Our company's billing system breaks things down by charge code and activity. Some example activities are meeting, analysis, design, development, testing, etc.

billing



This represents a charge code within our billing system. A project lead within ProTask has the choice to turn billing management on or off on each project.

issue



This is the issue, the bug, whatever you want to call it. It has only one required property - a title. The system determines the issue's status automatically and all issues fall into at least one category by default.

priority



Each project has ten priorities ranging from 1 to 10. However the text associated with the priority such as "High" or "Low" is modifiable on a project level basis.

project



This is the collection of all the other objects - there are a bunch of settings associated with a project

user



this is a person who uses the system. they have a name, email address, and role - roles are not modifiable across projects but a person can and usually does have a different role in each project.



After working on a different project where I learned about how little I knew
about CFC's I new the time would come where I could begin the redesing of
ProTask. That time is now and I will attempt to address what changes I have
made and, more importantly, why I made those changes.
