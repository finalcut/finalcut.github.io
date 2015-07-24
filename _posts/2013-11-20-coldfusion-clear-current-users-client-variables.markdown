---
layout: post
title: "Coldfusion: Clear Current Users Client Variables"
date: 2013-11-20 14:21
comments: true
categories: [coldfusion, client variables]
---
**`Be warned, you can probably seriously bork things by messing around in the CDATA nand CGLOBAL tables!`
`Proceed  with great care and at your own risk.  If you use this and it breaks it's your fault.`**



Today a colleage asked me the fastest way to get rid of all of the client variables that were currently set for his account in an app he is working on and testing.  I told him to restart ColdFusion.  But, curious, I figured that perhaps this would work:


```cfc
<cfloop list="#StructKeyList(Client)#" index="key">
	<cfset structDelete(client, key) />
</cfloop>

```


It didn't work.  On the app he is using it is storing client variables in the database so then I tried out  [`DeleteClientVariable`](https://learn.adobe.com/wiki/display/coldfusionen/DeleteClientVariable)


```cfc
	<cfloop list="#StructKeyList(Client)#" index="key">
		<cfset structDelete(client, key) />
		<cfset DeleteClientVariable(key) />
	</cfloop>

```


That didn't work either.  The documentation for `DeleteClientVariable` says you have to have an application.cfm with client management turned on.  This particular app has an Application.cfc with client management turned on.  I assumed it would still work.  It didn't.

Finally, I added in two queries to force the issue:


```cfc

	<cfset cfid = "#client.cfid#:#client.cftoken#%" >

	<cfloop list="#StructKeyList(Client)#" index="key">
		<cfset structDelete(client, key) />
		<cfset DeleteClientVariable(key) />
	</cfloop>

	<cfquery datasource="dsn">
		delete from cdata where cfid LIKE <cfqueryparam cfsqltype="cf_sql_varchar" value="#cfid#" />
	</cfquery>
	<cfquery datasource="dsn">
		delete from cglobal where cfid LIKE <cfqueryparam cfsqltype="cf_sql_varchar" value="#cfid#" />
	</cfquery>


```


You'll note I make a copy of `CFID` before I do anything else.  I also append a `%` to it so that I can do a `LIKE` search.  I'm not sure why but the exact string match didn't work.  I think there is some non-printable characters added to the end of `CFID` in the database.  I honestly don't have the time to dig more into it right now.  Anyway, use this at your own risk and, even better, [consider never using client variables](http://www.dopefly.com/pages/ColdFusionClientVariablesFinalNail.cfm.)




