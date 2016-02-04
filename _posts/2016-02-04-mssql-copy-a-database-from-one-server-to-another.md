---
layout: post
title: "MSSQL Copy a Database From One Server to Another"
description:
headline:
date: 2016-02-04 13:32:13 -0500
category: personal
tags: [mssql]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
This post contains the body of a [stack overflow answer](http://stackoverflow.com/a/24175818/7329) just so I can be sure
to not lose track of it.

I occasionally need to create a copy of a production database and then restore that database on my development machine.


### To backup the source database:

```sql
USE MASTER;

BACKUP DATABASE [MyDatabase]
TO DISK = 'C:\temp\MyDatabase1.bak' -- some writeable folder.
WITH COPY_ONLY
```

The `WITH COPY_ONLY` makes sure your production database isn't interrupted while you make a backup of it.




### To restore the destination database

```sql
USE MASTER;

RESTORE DATABASE [MyDatabase]
FROM DISK = 'C:\temp\MyDatabase1.bak'
WITH
MOVE 'MyDatabase'   TO 'C:\Sql\MyDatabase.mdf', -- or wherever these live on target
MOVE 'MyDatabase_log'   TO 'C:\Sql\MyDatabase_log.ldf',
REPLACE, RECOVERY
```


Note, the source database path `c:\temp\MyDatabase1.bak` is a path on the database server. That might seem obvious but if your MSSQL server is on one machine and you're developing on another and try to use SQL Server Management studio from your development machine you might forget.. Not that I would; I'm just saying.

Also, if you don't know what the values (logical names) of 'MyDatabase' and 'MyDatabse_log' should be run this super handy command and it will tell you:

```sql
RESTORE FILELISTONLY
FROM disk = 'C:\temp\MyDatabaseName1.bak'
```

Finally, If you use SQL Server logins (not windows authentication) you can run this after restoring each time (on the dev/test machine):

```sql
use MyDatabaseName;
sp_change_users_login 'Auto_Fix', 'userloginname', null, 'userpassword';
```

Again all credit for this goes to user [MGOwen](http://stackoverflow.com/users/87861/mgowen) and his [answer on Stackoverflow](http://stackoverflow.com/a/24175818/7329).
