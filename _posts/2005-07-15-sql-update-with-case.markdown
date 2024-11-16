---
layout: post
title: "SQL Update with a CASE"
date: 2005-07-15
comments: false
category: sql
---
Because I just read the post titled "[Leveraging Your SQL - Update Using a
Join](http://mkruger.cfwebtools.com/index.cfm?mode=alias&alias=Join%20Update)"
over at Coldfusion Muse I figured I would add this post in an effort to help
expand our SQL Updating skills. Sometimes, particularly with update scripts, I
might need to update a bunch of rows in the same table to have different
values based on some other value in their row. One way to do this is to write
a bunch of different updates (one per row) OR you can write one update with a
CASE statement in it.






```sql
UPDATE user SET confirmed_ind =

    CASE data_release

        WHEN 0 THEN 1    /* if no consent, we don't care about the 2006 confirmation */

        WHEN 1 THEN 0    /* if prior consent given, user must confirm that a 2006 consent is registered. */

    END;


```




You can even do much more complicated things as well:






```sql
UPDATE user SET type_id =

    CASE payrate

        WHEN 0 THEN 125

        WHEN 1 THEN 150

        WHEN 2 THEN 175

        WHEN 3 THEN 150

        WHEN 4 THEN 125

         WHEN 5 THEN 200

        WHEN 6 THEN 125

         WHEN 7 THEN 250

    END;


```







## Comments











Kostas






In that case you can a different SET clause for every column with their own conditions











paul






Is there a way to use a CASE statement in an Update to change the column that is being updated?
