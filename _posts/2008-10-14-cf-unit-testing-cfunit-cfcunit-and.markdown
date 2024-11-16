---
layout: post
title: "CF Unit Testing - CFUnit, CFCUnit, and MxUnit  Part 1"
date: 2008-10-14
comments: false
categories:
 - coldfusion
 - continuous-integration
 - unit testing
 - cfunit
 - cfcunit
 - unit-testing
 - mxunit
---
I love unit testing but, to be honest, I just haven't been able to come up
with an approach I really like for continuous integration and unit testing of
CF apps. This week I decided I was going to try out the three main frameworks
I know of; CFUnit, CFCUnit, and MXUnit and see if I can't find one that I like
using for comprehensive testing.  
  
Our shop doesn't use CFEclipse much and, in general, we don't really like
loading up Eclipse that much for developing CF apps; it seems like overkill.
We do, however, use Ant so I referenced a bunch of CF-Eclipse type tutorials
to get some basis for making all of this work.  
  
The first one I tried out was CFUnit. This is the one I have used the most in
the past and so it seemed like it would be my choice in the end. The first
problem I ran into with CFUnit was the inability to run a test suite with the
ANT task. This may be a feature I just don't see but nobody else seems to be
documenting how to do it either.  
  
My normal approach to setting up CFUnit is to create a test directory under
the root of my project and then create a similar directory structure as my
normal object model. For instance in my object directory I might have a bean,
dao, gateway, and service subdirectory. Within each of these directories I
will create a test CFC and a runner CFM for each test. Then I will create a
simple CFM in that directory that does a cfinclude for each CFM runner; these
comprehensive runners are my test suites. Then, in the parent object directory
I will create another runner CFM that includes each test suite so that I have
one full suite I can quickly access.  
  
CFCUnit does support Test Suites. However, the initial install itself seems to
have some problems. For instance when I follow the installation instructions
that say to run the CFCUnit's own unit tests a bunch of them fail. The failing
tests are primarily concerned with the CFUnit wrapper functionality but the
fact that all of those tests failed caused me some real concern.  
  
MxUnit doesn't support Test Suites either however it does support "directory"
testing and seems like the best option of the three for what I want to do.
Now, instead of having to create each of my test runner files I can just
create an ANT task that is responsible for each directory and then another ant
task that will run each of the directory level tests to serve as my overall
test suite. It's not perfect but it seems like a good option.  
  
While messing with all of these I tried using the BuildAgent in Eclipse to get
the build to happen on each save. That kind of sucked. While I liked the
constant testing it was just too much. For instance, I use ColdSpring with a
pretty large app and each time my tests run they have to load the ColdSpring
xml file to resolve dependency injection. Perhaps that isn't the greatest
structure but I want my tests to also help confirm that my coldspring
configuration is valid. Furthermore, I tend to change and save files pretty
quickly. Each time I would save the ant task was still firing off from the
prior save and I'd end up having to cancel it. For my workflow I prefer to
make my batch of changes and then hit the "test" button (or key combo).  
  
I'll be posting a followup with my final conclusions on how I approached
continuous testing along with precise instructions on how I configured
everything. After I do that I'll be looking at a collection of build tools
such as CruiseControl for testing automatically whenever someone checks in a
change.

## Comments

Jon Wolski

I'm using cfcUnit with ant in Eclipse, and I too had the problem of long-
running tasks on file-save.  
  
I resolved this by running my 'unittest' ant target (2-seconds) on "Auto
Build" (in the launch configuration properties for the project) and a more
comprehensive ant target on "Manual Build."

Slava Imeshev

Our [Parabuild](http://www.viewtier.com) might be worth adding to the list of
[Continuous Integration](http://www.viewtier.com/products/parabuild/continuous
_integration.htm) tools to consider.

