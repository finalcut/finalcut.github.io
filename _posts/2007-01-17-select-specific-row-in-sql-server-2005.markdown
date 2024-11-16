---
layout: post
title: "Select a Specific Row in SQL Server 2005 using Row_Number"
date: 2007-01-17
comments: false
category: sql
tags: [rownum,row-header,mssql]
---
Lets pretend we have a table, say a user table, with the following columns:

user_id
last_name
first_name

Now, lets pretend you need to grab the 28th user in the table when the table
is ordered by last_name, first_name. In the past you could do a [inner query
using TOP](http://cf-bill.blogspot.com/2006/12/t-sql-query-paging.html) but
SQL Server 2005 offers us another solution, Row_Number (kind of like Oracles
ROWNUM).

Here is the sample query to grab the 28th user from our user table:





```sql
 SELECT * FROM

  (

  SELECT Row_Number() OVER (ORDER BY last_name, first_name) as rowid,

    user_id,

    last_name,

    first_name

  FROM user

  ) as a

 where rowid = 28


```







## Comments











Aravamudan






Try this

----------

```sql
select * from (

select  row_number() over(order by t)[order],* from

(

  select top 10 1 [t], *  from #temp


)as T

)as  t1 where [order] =6

```









Anonymous





```sql
SELECT * FROM

  (

  SELECT Row_Number() OVER (ORDER BY last_name, first_name) as rowid,

    user_id,

    last_name,

    first_name

  FROM user

  ) as a

 where rowid = 28
```

i dont get it...

what's this ") as a"?


anyone explain each line... t.y in advance











Anonymous






Excellent suggestion


Thank You very much











Anonymous






Excellent suggestion.

Thank You very much











onRails






Two suggestions:


You can use ROWCOUNT











Anonymous






Is there a way to set rowid as a calculated value?  For instance: order values asc, get the rowcount, and then retrieve the median value (half the row count)
