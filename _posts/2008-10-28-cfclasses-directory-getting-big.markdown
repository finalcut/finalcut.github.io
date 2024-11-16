---
layout: post
title: "cfclasses directory getting big?"
date: 2008-10-28
comments: false
categories:
 - coldfusion
---
This is probably obvious to most of you out there but, just in case you missed
it there is a setting in the CF Admin panel that will help keep your cfclasses
directory from getting huge.  
  
On the "Caching" page of CF Admin there is a checkbox titled " Save class
files " if you are in development you should seriously keep that UNCHECKED.  
  
Here's an example to illustrate why that is a good idea. We are working on a
semi-complicated CF app using Model-Glue and Coldspring. When the site is
first hit, after starting CF server, 3,002 .class files are generated and
placed in the cfclasses directory. Now, imagine you are editing and revisiting
some of those files (or flushing the entire MG cache). That number keeps on
growing and growing. Eventually, something will go wrong and you'll want to
delete some .class files to make sure you are seeing the latest code. However,
because your cfclasses directory is so huge you won't even be able to "cd"
into it. Your system will appear to hang. Trying to delete the directories
contents will take a long, long time.  
  
What do you do? Well you uncheck that damn box that's what! That will prevent
a huge backlog of files from building up in the cfclasses directory in the
first place. Trust me, uncheck it.

## Comments

Bill

well that depends on your CF install. With CF8 it is in your
jrun4/servers/cfusion/cfusion-ear/cfusion-war/WEB-INF/cfclasses  
  
in older coldfusion if they are installed normally it will be somewhere under
your cfusionmx (or cfusion) directory.. you just have to drill down to find
it.

Anonymous

Where is this cfclasses directory that you speak of?

