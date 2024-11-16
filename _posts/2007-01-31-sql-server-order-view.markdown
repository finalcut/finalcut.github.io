---
layout: post
title: "SQL Server - Order a View"
date: 2007-01-31
comments: false
category: sql
tags: [mssql,views,percent]
---
**Please Read the Update to this post as the post can not be considered accurate - the technique works but the result is not what I expected.**

On occasion I have had to write a view in MS SQL server (currently 2005) and
in the view I have wanted to order the results - but if you try SQL server
throws an error:


The ORDER BY clause is invalid in views, inline functions, derived tables,
subqueries, and common table expressions, unless TOP or FOR XML is also
specified.



I honestly haven't known how to work around this, until today that is. There
is a SQL reserved word "PERCENT" that I was unaware of but it is the perfect
solution for when I need a view to return all rows but in a specific order..





```sql
SELECT TOP(100) PERCENT a.x,b.y FROM a, b WHERE a.b_id=b.b_id AND y=@b

ORDER BY b.y, a.x


```




For many of you this may be old hat but for me it was a minor revelation.





**UPDATE:**



Well, Sadly, a helpful visitor to the blog (David) has shown me my impression of this technique is completely wrong.  It turns out you aren't guaranteed to get things back from the view in the right order even though the view is built with an order by clause.  I really should have known that and I apologize to anyone I have misled with this post.


Darn.


**UPDATE 2:**

Another reader just came by and let me know about a [hotfix](http://support.microsoft.com/kb/926292) that corrects this behavior.  The hotfix specifically addresses the issue where the order by clause in the views definition is ignored.  It turns on in SQL Server 2000 the behavior was what I expected and this hotfix brings that behavior back for both SQL Server 2005 and 2008.  This fix may already be applied to your db.





  1. SQL SERVER 2008 -- hotfix addressed in [Cumulative update package 1](http://support.microsoft.com/kb/956717/)



  2. SQL SERVER 2005 -- hotfix adddressed in [Cumulative update package 2](http://support.microsoft.com/kb/936305/)




Obviously you still need to be careful in using this technique.  Before trusting in it you need to make sure your production environment has this hotfix or patch applied otherwise you will end up with inconsistent results.





## Comments











Anonymous






Try this:


SELECT TOP(100) PERCENT * FROM View_Table;




This works for me in Delphi TQuery and TADOQuery too.

You can add more orders after it.


Best Regards,

DarkLight











Hugonne






Oracle views can be ordered, I don't see why SQL Server ones can't.











Anonymous






Read this HotFix:


http://support.microsoft.com/kb/926292











Anonymous






Using TOP (99.999999) PERCENT in a view is NOT a reliable substitute for putting ORDER BY in the query that references the view. By definition queries without ORDER BY are unordered as BOL makes clear. There are no workarounds.











Anonymous






The "SELECT TOP (99.999999) PERCENT" worked for my view.











R B






SELECT TOP (99.999999) PERCENT

is a decent workaround.











Will






There is a hotfix available for this now--see KB 926292.  In addition to the request-only hotfix, you also have to set compatibility to 80 and set a traceflag, but it does restore the behavior for SQL Server 2000











Bill






Thanks David - that does help.  I appreciate you taking the time to come back and explain and provide an example.











Anonymous






Books Online has everything you need to know:


"When ORDER BY is used in the definition of a view, inline function, derived table, or subquery, the clause is used only to determine the rows returned by the TOP clause. The ORDER BY clause does not guarantee ordered results when these constructs are queried, unless ORDER BY is also specified in the query itself."


http://msdn2.microsoft.com/en-us/library/ms188385.aspx


"Although the view definition contains an ORDER BY clause, that ORDER BY clause is used only to determine the rows returned by the TOP clause. When querying the view itself, SQL Server does not guarantee the results will be ordered, unless you specify so explicitly, as shown in the following query:


SELECT * FROM TopView

ORDER BY LastName "


http://msdn2.microsoft.com/en-us/library/ms188723.aspx


Relational tables and views are unordered sets by definition. The notion of "ordering" them is obviously in contradiction to the way SQL and SQL Server works. As for an example, here's one I tested in 2005 (build 2153). However, I can't guarantee you'll reproduce my results every time. Please trust the logic and the documented behaviour rather than just putting the query optimizer to the test.


CREATE TABLE t1 (x INT PRIMARY KEY, y INT UNIQUE);

GO

CREATE VIEW v1 (x,y) AS

SELECT TOP 100 PERCENT x,y

FROM t1

ORDER BY x

GO

INSERT INTO t1 (x,y) VALUES (1,3);

INSERT INTO t1 (x,y) VALUES (2,2);

INSERT INTO t1 (x,y) VALUES (3,1);

GO

SELECT x,y FROM v1;


Result:


x           y

----------- -----------

3           1

2           2

1           3


(3 row(s) affected)


HTH.

David Portas











Bill






Up until I came across this technique I agreed there was no such thing as an ordered view.  But, if the example I am providing is not an ordered view, please tell me what it is.  It is a view definition with an ordering that is enforced when you select * from said view.  That, to me, is an ordered view.


I am not sure how my result is "luck" what I did is perfectly valid SQL (in SQL Server 2005) and, based on the syntax shown, the view should be built in an ordered fashion.


If there are "demonstrably many" cases where this will not work I would appreciate just one example.      The point of this blog is to share things I learn - please join in the experience and make the lesson more complete.











Anonymous






There is no such thing as an ordered view. What you are really attempting to do is to order the result of a SELECT statement that references a view even though that SELECT statement doesn't have an ORDER BY clause. This is not supported. The order of SELECT statements without ORDER BY is always undefined so the result you get is just "luck" not by design. There are demonstrably many cases where it will not work.
