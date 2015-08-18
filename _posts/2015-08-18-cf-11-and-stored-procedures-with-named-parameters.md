---
layout: post
title: "CF 11 and Stored Procedures with Named Parameters"
description:
headline:
modified: 2015-08-18 08:42:53 -0400
category: coldfusion,oracle,mssql
tags: []
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
Up to this point none of my customers have upgraded to CF 11.  Some have been hanging out
at CF9 and others have long since moved to CF 10.  However, this week one moved to CF 11
and we ran into what I thought was a strange error.

The following code was failing with the error `[Macromedia][Oracle JDBC Driver][Oracle]ORA-06502: PL/SQL: numeric or value error: character to number conversion error ORA-06512: at line 1`

```cfm
<cfstoredproc datasource="#getDSN()#" procedure="pkgImportMediaItems.ImportMediaItems">
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.month#" dbVarName="pJurisdictionMonth" type="IN" />
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.year#" dbVarName="pJurisdictionYear" type="IN" />
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.clientID#" dbVarName="pClientID" type="IN" />
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.jurisdictionTypeID#" dbVarName="pJurisdictionTypeID" type="IN" />
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.userID#" dbVarName="pUserID" type="IN" />
  <cfprocparam cfsqltype="cf_sql_varchar" value="0" dbVarName="pItemNo" type="IN" NULL="true" />
</cfstoredproc>
```

All of the values being passed in to the first five parameters were numbers and the last one is forced to null in this instance.  There was no real reason that I could see for the problem I was seeing.  Interestingly enough this is the only procedure in the entire application where I specified the names for the parameters in the Coldfusion code - but they are all exactly correct and in the correct order.

For a long time now Coldfusion hasn't really cared what you used in the `dbVarName` attribute.  It was ignored and the order of the arguments was all that was considered and my arguments were all in the correct order too.  So what gives?

Well, it turns out that in CF11 Hotfix 3 adobe fixed the long standing problem of the `dbVarName` being ignored AND added a seemingly arbitratry requirement that you prefix your argument names with a colon (:) if you are using an Oracle db or an at sign (@) if you were using MS SQL Server.  I am glad they fixed the naming problem - it always annoyed me that my usage of named arguments as ignored.  But the inclusion of the prefix is kind of antiethical to the nature of Coldfusion which, typically, tries to simplify you're interactions with the database.  Plus it makes my code less portable between the two different database types (unless I use some stupid global setting for the prefix!).

Anyway, the entire block of code just had to be changed to this and it worked fine.  Go figure:

```cfm
<cfstoredproc datasource="#getDSN()#" procedure="pkgImportMediaItems.ImportMediaItems">
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.month#" dbVarName=":pJurisdictionMonth" type="IN" />
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.year#" dbVarName=":pJurisdictionYear" type="IN" />
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.clientID#" dbVarName=":pClientID" type="IN" />
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.jurisdictionTypeID#" dbVarName=":pJurisdictionTypeID" type="IN" />
  <cfprocparam cfsqltype="cf_sql_integer" value="#arguments.userID#" dbVarName=":pUserID" type="IN" />
  <cfprocparam cfsqltype="cf_sql_varchar" value="0" dbVarName=":pItemNo" type="IN" NULL="true" />
</cfstoredproc>
```

Yep, I just had to add the colons.
