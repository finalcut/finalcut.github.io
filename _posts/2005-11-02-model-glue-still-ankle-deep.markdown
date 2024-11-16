---
layout: post
title: "Model-Glue : Still Ankle Deep"
date: 2005-11-02
comments: false
category: coldfusion
tags: [modelglue,framework,mvc]
---
Yesterday Dave Ross and Sean Corfield both stopped by this blog and clarified
a couple points in my last post. So I wanted to put those comments here so
that anyone following along wouldn't miss them.  

Dave said that by turning off CF debugging (particularly measuring of
execution time) that MG would be faster. He was right. However, without the
debugging trace on I can't give you a clear measurement of the difference.
Using just MG debugging each execution that was taking 1.5 seconds with CF
debugging was taking 700ms without it. I imagine it is even faster without the
MG debugging.  

Sean answered my question on the best practice for forwarding in MG by saying
that whenever possible I should use the XML result notation instead of the
event.forward method. That is what I suspected but it is nice to have
confirmation.  

He also mentioned the fact that you can do event chaining without forwarding
at all. While I figured you could (using the Broadcast xml directive in
ModelGlue.xml) I hadn't/haven't tested that yet. I just want to make sure
anyone else reading this is aware of the capability as well.  

Next up, adding a db backend to my lame Todo application.
