---
layout: post
title: "Prevent SQL Server Transaction Log Getting Full in Dev"
date: 2013-05-14
comments: false
category: sql
tags: [mssql,transaction-log]
---
I routinely forget this and then have to look it up again so I'm putting it
here so I can remember it:

If you have a DEVELOPMENT database using SQL Server you can prevent your
transaction log from getting "full" and thus requiring you to back it up with
a simple command:





alter database {DBNAME} set recovery simple;
```




Just make sure you only use that in development - if you use it in production make sure you're aware of the limitations and the issues surrounding using SIMPLE logging.  You can [learn more about the transaction log on the MSDN Site](http://msdn.microsoft.com/en-us/library/ms190925.aspx).
