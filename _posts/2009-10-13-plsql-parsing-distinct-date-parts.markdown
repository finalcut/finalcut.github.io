---
layout: post
title: "PLSQL : Parsing Distinct Date Parts (STRING.SPLIT)"
date: 2009-10-13
comments: false
categories:
 - plsql_split
 - string.spllit
---
This may not be very useful - I know that after I wrote it I actually ended up
not needing it but it was a fun exercise anyway. Basically what it does is it
parses the current date (or any date really) and results in three variables
being populated with the month number, day number, and year number from the
date given. You could use this for other types of string.split type activities
if you needed.






```sql
  vDay          NUMBER;

  vMonth        NUMBER;

  vYear         NUMBER;



  SELECT

     TO_NUMBER(regexp_substr(t.now, '[^,]+', 1)) INTO vDay,

     TO_NUMBER(regexp_substr(t.now, '[^,]+', 4)) INTO vMonth,

     TO_NUMBER(regexp_substr(t.now, '[^,]+', 7)) INTO vYear

    FROM

        (

                SELECT to_char(sysdate,'dd,mm,yyyy') as now

                  FROM sys.dual)


        t;


```




Overall this is a pretty simple little query but, if you aren't very familiar with PLSQL it might seem a little daunting.  Here's what's happening in a nutshell.






  1. The regexp_substr is getting the string deliniated by the comma; the numeric argument passed to it tells where to start getting the substring from.



  2. the t; on the last line of the code is an alias that represents the result set returned by the SELECT to_char subquery.  The semi-colon just means the code is complete.  You may have to remove it depending on where you're using the code; personally,  I had it in a stored procedure.



  3. NOTE:I inserted the comma's into the datestring by specially formatting the date with the to_char method.  Typically people use slashes but I like comma's better for this purpose.




I've put this up here mostly as a reminder for myself but I hope it helps someone else at some time.


If you want to just run it in a SQL query real fast (without variables) try this:




```sql
 SELECT

    TO_NUMBER(regexp_substr(t.now, '[^,]+', 1)) as vDay,

    TO_NUMBER(regexp_substr(t.now, '[^,]+', 4)) as vMonth,

    TO_NUMBER(regexp_substr(t.now, '[^,]+', 7)) as vYear

   FROM

       (

               SELECT to_char(sysdate,'dd,mm,yyyy') as now

                 FROM sys.dual)


       t


```






