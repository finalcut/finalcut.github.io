---
layout: post
title: "SQL Server: Update Records in One Table by Copying Related Data from a Second Table"
description: Using a select statement to update a record in mssql.  mssql update from select
date: 2013-07-17
comments: false
category: sql
tags: [update,mssql]
---
I always forget this syntax for updating from a select so it I'm posting this for my memory

```sql
UPDATE t1
SET   t1.col1 = t2.col1,
    t1.col2 = t2.col2
FROM  table_one t1
      JOIN table_two t2
        ON t2.table_one_id = t1.table_one_id
WHERE  t1.col3 = 'some_further_filter_value'
```

Here is an alternate syntax:

```sql
UPDATE table
SET Col1 = i.Col1,
   Col2 = i.Col2
FROM (
    SELECT ID, Col1, Col2
    FROM other_table) i
WHERE
    i.ID = table.ID
```    
