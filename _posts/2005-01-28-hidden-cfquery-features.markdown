---
layout: post
title: "Hidden CFQUERY features"
date: 2005-01-28
comments: false
categories:
 - coldfusion
 - query
---
On the cfc-def list someone just posted a link to a cool resource that shows
some undocumented, and thus unsupported, features for the cfquery object. My
personal favorite is the sort method. Here is an example copied from the page
that I linked:


```cfc
  columnId = query.findColumn("name");
  query.sort(columnId, false);

```


Notice that the method - findColumn was called first. Thats because the sort
method takes in the following two parameters:
sort(int columnID, boolean ascending)

So you pass the name of the column you want the id for into findColumn and use
the resulting id value in the sort method. Its too bad this isn't an official
feature. I wonder if it is faster than a query of queries that just re-sorts.
I would bet it is.

## Comments

MarkT

This made my day. Much cleaner than a QofQ!

