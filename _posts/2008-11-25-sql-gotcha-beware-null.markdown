---
layout: post
title: "SQL Gotcha:  Beware the NULL"
date: 2008-11-25
comments: false
categories:
 - sql
 - null
 - gotcha
---
Today I ran into a little bit of SQL that, on first glance, didn't make a
bunch of sense. Before I show you the SQL I'll give you a basic idea of the
two tables being queried:



### AREA





```
areaid | int NOT NULL

areaname | varchar2(100) NOT NULL


```











### FACILITY





```

facilityid | int NOT NULL

facilityname | varchar2(100)  NOT NULL

areaid | int NULL


```








There is actually a bit more to it but these columns are the important ones.  The query that had been written was trying to find all areas that had no facilities within them:




```sql

SELECT ar.* FROM area ar WHERE ar.areaid NOT IN (SELECT f.areaid FROM facility f)


```




That query returned no rows at all.  Meanwhile the following query returned one row:





```sql
SELECT ar.* FROM area ar WHERE NOT EXISTS (SELECT f.areaid FROM facility f.areaid = ar.areaid)


```




Honestly, I've given you a big hint to figuring this one out already since I titled this thing Beware the Null and I showed you which columns could be NULL and which couldn't.  But here is the problem.


**Any SQL comparision that involves a NULL will evaluate to FALSE**


That means all of the following examples would return no rows:




```sql
  SELECT * FROM area WHERE areaid NOT IN (1,2,NULL);


  SELECT * FROM area WHERE areaid IN (1,2,NULL);


  SELECT 1 as myRow FROM dual WHERE 1=null;


  SELECT 1 as myRow FROM dual WHERE 1 != null;


  SELECT 1 as myRow FROM dual WHERE null = null;


```




All of those return no rows because any comparison operator used with a null evaluates to false (IN, NOT IN, =, !=, etc).


So, how do I fix the NOT IN query to work the way I expected it to?





```sql
SELECT ar.* FROM area ar WHERE ar.areaid NOT IN (SELECT f.areaid FROM facility f WHERE f.areaid IS NOT NULL)


```







## Comments











Bryan Price






As an aside, I notice that having a NULL in an IN query is ok, but in a NOT IN query it's bad.


Thus the statement


SELECT ar.* FROM area WHERE areaid IN ( 1 , 2 , NULL )


will come up with results if areaid = 1 or areaid = 2, but


SELECT ar.* FROM area WHERE areaid NOT IN ( 1 , 2 , NULL )


will get no results in any case, even if there was an areaid=3 in there.











Bill






Thanks for the additional clarification Chris!











Chris






The key to this behaviour is the meaning of NULL. NULL does not mean "not existing", it means "unknown, if it even exists".


If the value is unknown, you can not know whether it should be in the subselect result set. But, NOT IN selects a specified resultset.


And if a value is unknown, it can not be part of that result set. ;-)


BTW Doug's solution is way faster than NOT IN, at least when it comes to bigger subselects... NOT IN can be a real performance killer.











Bill






Thanks Doug, you are correct and your query will return areas with no facilities.











Doug Giles






A left join will give you the results that you're looking for:


SELECT ar . *

FROM area ar

LEFT JOIN facility fa ON ( ar.areaid = fa.areaid )

WHERE (fa.facilityid IS NULL)


That query should return the areas that do not have a facility.











Bill






Because that won't work either:


I edited your code a little to work with Oracle:

SELECT ar.*

FROM area ar

INNER JOIN facility fa

ON (ar.areaid = fa.areaid)

WHERE (fa.facilityid IS NULL)



And it too returns no rows.. Where I am trying to find the rows in the area table that don't exist in the facility table.


Beyond the fact that your query returns no records (because the facility ID can't be NULL) I don't even see how I could convert your query to get what I wanted; I really don't want a join of the two tables, I want to find the differences between the two so to speak.











Rick






Why not a straight-up join?


SELECT ar.*

FROM area AS ar

  INNER JOIN facility AS fa

  ON (ar.areaid = fa.areaid)

WHERE (fa.facilityid IS NULL)










