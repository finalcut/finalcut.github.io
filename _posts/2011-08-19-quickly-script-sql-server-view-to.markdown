---
layout: post
title: "Quickly Script a SQL Server View to Oracle Table"
date: 2011-08-19
comments: false
categories:
 - sql
 - sql-server
 - oracle
---
I recently had a need to mirror a SQL server view in an Oracle database.
Without getting to detailed the basic premise is that a job runs once daily
that copies data from the SQL Server via hetergenous data services into the
Oracle table. This allows some useful reporting queries to run that are joined
across multiple Oracle schemas without having the slowdown involved with
communicating directly over the heterogenous link on each query.

Anyway, some of these views are stupid huge and I did not want to type each
and every column name and column type. Thankfully there is a great resource
inside SQL server that made my life quite a bit easier - the
INFORMATION_SCHEMA.COLUMNS table. It basically describes all the bits and
pieces involved in all of the tables and views in your database.

It's important to note that not all SQL server columns fit exactly into Oracle
columns so I also needed to include a bit of logic to make [the translation
between datatypes](http://download.oracle.com/docs/cd/B19306_01/gateways.102/b
14270/apa.htm).

Here is the query:




```sql
SELECT '"' + column_name + '"     ' +
		CASE data_type
			WHEN 'bigint'		THEN 'number(19)'
			WHEN 'binary'		THEN 'raw'
			WHEN 'bit'		THEN 'number(3)'
			WHEN 'char'		THEN 'char'
			WHEN 'datetime'		THEN 'timestamp'
			WHEN 'decimal'		THEN 'number(' + CAST(numeric_precision as varchar) + ',' + CAST(numeric_scale as varchar) + ')'
			WHEN 'float'		THEN 'float(49)'
			WHEN 'image'		THEN 'long raw'
			WHEN 'int'		THEN 'number(10)'
			WHEN 'money'		THEN 'number(19,4)'
			WHEN 'nchar'		THEN 'nchar'
			WHEN 'ntext'		THEN 'long'
			WHEN 'nvarchar'		THEN 'nchar'
			WHEN 'numeric'		THEN 'number(' + CAST(numeric_precision as varchar) + ',' + CAST(numeric_scale as varchar) + ')'
			WHEN 'real'		THEN 'float(23)'
			WHEN 'smalldatetime'	THEN 'date'
			WHEN 'smallmoney'	THEN 'number(10,4)'
			WHEN 'smallint'		THEN 'number(5)'
			WHEN 'text'		THEN 'long'
			WHEN 'timestamp'	THEN 'raw'
			WHEN 'uniqueidentifier' THEN 'char(36)'
			WHEN 'varbinary'	THEN 'raw'
			WHEN 'varchar'		THEN 'varchar2( ' + CAST(CHARACTER_MAXIMUM_LENGTH AS varchar) + ')'
			ELSE 'CHECK THIS.. ' + data_type + ' DataType'
		END + ', '

FROM information_schema.columns

WHERE table_name = 'your_table_or_view_name'


```



This will basically give you backa bunch of records that have the column name surrounded by quotes and then the type of the column followed by a comma.


Once you have that you just need to prepend the "CREATE TABLE tablename (" bit at the beginning and remove the final comma and append a closing ");" and you've got a nice script to create a table.


If you have a small table this probably isn't too helpful.  However, some of the views I have to mirror have over 250 columns!


It is possible that at times you will see a -1 in the datatype field.  If that happens it is because the length was set to "MAX" however I didn't really need to update my query to handle that so I'll leave that as an exercise for you if you need to handle that special case.




