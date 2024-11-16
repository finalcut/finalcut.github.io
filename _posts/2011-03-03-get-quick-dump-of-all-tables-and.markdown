---
layout: post
title: "Get Quick Dump of all Tables and Columns in Oracle Schema"
date: 2011-03-03
comments: false
categories:
 - pl/sql developer
 - plsql
 - oracle
---
Today I was asked if there were any columns in our schema that contained the
string "WIZ" in their name.  Here is the query I used to confidently answer
no.








```sql
SELECT table_name, column_name  from dba_tab_columns


WHERE LOWER(owner) = 'schema_name'


AND UPPER(column_name) LIKE '%WIZ%'


ORDER BY table_name, column_name


```




The only caveat was I had to be logged in as the db admin to access the "dba_tab_columns" table.




