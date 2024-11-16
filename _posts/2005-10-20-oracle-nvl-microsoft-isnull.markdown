---
layout: post
title: "Oracle NVL = Microsoft ISNULL"
date: 2005-10-20
comments: false
featured: true
category: sql
tags: [mssql,oracle,nvl,isnull]
---
Sometimes when writing a query, particularly during concatenation, you don't
want a NULL value in part to force a NULL return to the expression. With
Oracle I have always avoided that result using the NVL function and today
(suprisingly for the first time) I needed the same feature in Transact SQL
(SQL Server). The equivilent is ISNULL.


### Oracle NVL Usage

```sql
nvl(check_expression, replacement_value)
```


### T-SQL ISNULL Usage


```sql
ISNULL ( check_expression , replacement_value )


```




In both cases the function will return the replacement_value if check_expression is NULL otherwise they will return check_expression.  Note that replacement_value needs to be of the same type as check_expression.  You can't give the user back an orange when they ask for an apple so to speak!





## Comments











Evandro






Thanks a lot!











Anonymous






Bill -


Thank you.  Exactly what I was looking for!  I took a new job recently and the new company uses MS SQL Server as opposed to the Oracle I'm used to.











Don






Actually, they do work the same. What is not the same is that Oracle treats '' as equivalent to null. So, a statement like:

NVL(somefield,'')

is useless, because you are replacing null with null.











Esger






Hey, thanks for this.


One caveat I found is that whereas


where isnull(somefield,'') != 'gimme_all_other_values_including_NULL'


works in tsql


NVL(somefield,'') != 'gimme_all_other_values_including_NULL'


doesn't seem to return any result. at least when 'somefield' is a nullable VARCHAR2(30 CHAR) type field.


adding a character in the NVL construct


NVL(somefield,'x') != 'gimme_all_other_values_including_NULL'


does the trick, but it shows that the behaviour is not entirely the same and would blow some code when doing a tsql-plsql recoding.











Luke






Thanks for the post - I was looking for the Oracle equivalent of ISNULL().











Anonymous






As of Oracle 9, COALESCE now works in Oracle.











Anonymous






Both Oracle and SQL Server 2005 allow the use of the CASE statement (syntax shown below):


```sql
  SELECT CASE WHEN col5 = 0 THEN 'Value of column 5 is zero'

            WHEN col5 = 1 THEN 'Value of column 5 is one'

            WHEN col5 = 2 THEN 'Value of column 5 is two'

            WHEN col5 IS NULL THEN 'Value of column 5 is NULL'

            ELSE 'Value of column 5 is invalid'

            END AS Column5Value

FROM _sometable_
```










Dov






I don't know if Oracle has a variable-length method such as:


**

NVL(orig, repl1, repl2, repl3, ...)

**


But you can simulate it with:


**

NVL(orig, NVL(repl1, NVL(repl2, NVL(repl3, ...))))

**


It's certainly not as pretty, but probably nicer than some multi-line CASE statement.











Adriano






Wow!


This information help me a lot!


Thanks!











Bill






While not a particularly pretty way of doing it you could use the T-SQL function: DECODE to accomplish the same thing as Coalesce.


DECODE is a function that lets you perform one big case statement with conditionals at each case point.


I don't know if there is a cleaner way to do what you're asking.











Anonymous






Thanks for the info.


Is there an Oracle equivalent to T-SQL's COALESCE statement?


COALESCE takes an arbitrary list of parameters and returns the first non-null parameter in the list. ISNULL is equivalent to calling COALESCE with two parameters.


-Jamie


http://blogs.conchango.com/jamiethomson
