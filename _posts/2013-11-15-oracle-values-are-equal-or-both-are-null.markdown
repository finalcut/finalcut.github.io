---
layout: post
title: "Oracle values are Equal or Both Are Null"
date: 2013-11-15 09:30
comments: true
category: [development]
tags: [oracle,null,decode,sql]
---
I've been using Oracle on and off for about twelve years so it seems like I should have known this trick already but today I learned so I'm sharing.

Consider this scenario:  You have a table that stores records about a course.  It is valid to allow a user to store a duplicate course record for everything
but the ID.  However, you want to tell the user that the record is a duplicate and point them to the carbon copy. Furthermore, many of the columns you
check against for equivalence are NULLABLE and are of different data types (DATE, VARCHAR, NUMBER).

The first thing you have to remember is NULL != NULL.  Thus you can't just check a column thusly `source_col = test_value`  It will work when both source_col
and test_value are NOT NULL but if they are both NULL you won't identify the two records as being copies of each other.

I've typically handled this by having this clunky bit of logic:


```sql
	WHERE (source_col = test_value OR (source_col IS NULL and test_value IS NULL))
		AND ...

```


If you are testing against five or six records your query quickly becomes kind of ugly and difficult to visually parse so I've not been really happy with this technique
even though it does work.  NOTE: `NVL(source_col, 'fakevalue') = NVL(test_value, 'fakevalue')` is both [slower](http://stackoverflow.com/a/192072/7329) and fraught with the possibility that fakevalue might, possibly
find a way to validly exist in the source_col which could lead to a false positive.

So with all that said what is a better solution?  Here is one that was suggested in [a stack overflow comment](http://stackoverflow.com/a/5303981/7329) referencing a book titled [Expert Oracle Database Architecture](http://www.amazon.com/gp/product/1590595300/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1590595300&linkCode=as2&tag=strictlymovie-20).


```sql
	WHERE DECODE(source_col, test_value, 1) = 1
		AND ...

```


This is super simple and brilliat but does depend on future maintainers of your code to understand how `DECODE` works.  Here is my explanation.  `DECODE` is defined like so `DECODE(expression, search_value, result)`.
`DECODE` is actually a little more complicated than what I'm describing so if please [read the documentation](http://www.techonthenet.com/oracle/functions/decode.php).  Anyway, for my usage `DECODE` is just dealing
with the first three possible arguments.  `expression` represents the source column that I am search against.  `search_value` is the test value I'm searching for.  `result` is what `DECODE` will return if the `search_value` and
`expression` match.  The key here is that `DECODE` considers it a  match if both `expression` and `search_value` are both NULL!

Thus if your source_col value IS NULL and test_value is NULL or your souce_col value is a non-empty string and your test_value is the same non-empty string the records will match.

WARNING!  I can't really stress this enough.  Oracle considers an empty string to be null.  Thus `DECODE(null, '', 1)` will return the `1` result.  Consider this dummy example


```sql
	SELECT 'foo' as bar from dual WHERE '' IS NULL;

```


You will get a row back with bar == 'foo' which may not be what you expected.  Thus, you will get a row back as well if you do this:


```sql
	SELECT 'foo' as bar FROM dual WHERE DECODE('',NULL,1) = 1

```

Even if you switch the NULL and empty string around the `DECODE = 1` will evaluate to `TRUE` so you will get this match every time.  This is just a part of how oracle works and I'm not sure you can do anything to work around it.
