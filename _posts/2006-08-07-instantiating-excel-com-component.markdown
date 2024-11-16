---
layout: post
title: "Instantiating Excel Com component raises error 0x80080005"
date: 2006-08-07
comments: false
category: programming
tags: [msexcel,com]
---
I ran into an odd error today running MS Excel 2003 sp2. Whenever I tried to
instantiate the COM object an error was raised:  

The cause of this exception was that: AutomationException: 0x80080005 - Server
execution failed. Note that Windows 95 does not support automatic launch of a
server, it must be running already. was raised  

I searched this Blog (bloggger.com search sucks) and searching Google did me
no good. Searching the MSDN Knowledge Base didn't help either. I thought I had
encountered this error once before; but I hadn't personally. It turns out
though that one of my clients had and because of that I had done some prior
research. Fortunately, I had saved the email which pointed to [a thread on a
microsoft support forum](http://support.microsoft.com/newsgroups/default.aspx?
dg=microsoft.public.excel&tid=201b83c0-df3c-4dfd-af39-dbf72e376f4e&p=1) that
gave me a hint.  

It turned out I needed to do something I had never done before on a windows
machine. I had to manage a DCOM security setting. I wasn't sure how to do it
but it turned out to be pretty easy and, I guess fairly intuitive since I
didn't have to search Google for help on it.  

Using the "start menu" I went to START | PROGRAMS | ADMINISTRATIVE TOOLS |
COMPONENT SERVICES. Once the window popped up I expanded Component Services |
Computers | My Computer | DCOM Config. Within that node of the tree I found
"Microsoft Excel Application". Right clicking on that I found a "properties"
option. On that dialog was a "security" tab. Under the "Launch and Activation
Permissions" I selected "Customize" and then clicked the "Edit" button. I
choose to "Add" a new user and another dialog appeared. Here I typed in my
IUSER account information and clicked "OK" and then choose the "Local Launch"
and "Local Activation" permissions. I wasn't sure which one I needed but at
this point CF and Excel were working together so I was happy.  

When adding the new account permission the process kind of broke down though
because I didn't know the name of my IUSR account of the the top of my head
and there was no way to have the dialog prompt me with a list of valid users.
I ended up having to open up the administrative interface for Users and Groups
to get that string.

## Comments

MLR

thanx for the info :D
