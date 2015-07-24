---
layout: post
title: "Debugging a Query"
date: 2005-01-28
comments: false
categories:
 - coldfusion
 - debugging
---
I had to debug a query the other day and it was agonizing trying to figure out
what was going on. It wasn't that the query was complicated - but the problem
was subtle - and thus difficult to find. Here it is:  
```cfm  
<cfquery name="jurisdictionSelect" datasource="#variables.dsn#">  
SELECT sh.SectionHeaderID,  
sh.chapterid,  
sh.sectionnumber,  
sh.sectionheadingname,  
c.chaptercode,  
c.chapterid,  
c.chaptername,  
s.description,  
'Normal' as sectionType,  
0 as orderBy  
FROM sectionheader sh,  
chapter c,  
jurisdictiontypegroupmapping j,  
s.sectionheader  
WHERE j.jurisdictiontypegroupid = <cfqueryparam cfsqltype="cf_sql_integer"
value="#attributes.jurisdictiontypegroupid#">  
AND sh.jurisdictiontypeid = j.jurisdictiontypeid  
AND c.chaptercode = sh.chapterid  
AND s.chapterid = c.chaptercode  
AND c.chaptercode NOT LIKE 'O%'  
AND c.chaptercode NOT LIKE 'T%'  
<!--- get the "Other" chapter id values --->  
UNION (  
SELECT sh.SectionHeaderID,  
sh.chapterid,  
sh.sectionnumber,  
sh.sectionheadingname,  
'O' as chaptercode,  
c.chapterid,  
'Other' as chaptername,  
'Other' as sectionType,  
s.description,  
1 as orderBy  
FROM sectionheader sh,  
chapter c,  
jurisdictiontypegroupmapping j,  
s.sectionheader  
WHERE c.chaptercode LIKE 'O%'  
AND j.jurisdictiontypegroupid = <cfqueryparam cfsqltype="cf_sql_integer"
value="#attributes.jurisdictiontypegroupid#">  
AND sh.jurisdictiontypeid = j.jurisdictiontypeid  
AND c.chaptercode = sh.chapterid  
AND s.chapterid = c.chaptercode  
)  
<!--- get the "Toxic" chapter id values --->  
UNION (  
SELECT sh.SectionHeaderID,  
sh.chapterid,  
sh.sectionnumber,  
sh.sectionheadingname,  
'T' as chaptercode, c.chapterid,  
'Toxic' as chaptername,  
'Toxic' as sectionType,  
s.description,  
2 as orderBy  
FROM sectionheader sh,  
chapter c,  
jurisdictiontypegroupmapping j  
WHERE c.chaptercode LIKE 'T%'  
AND j.jurisdictiontypegroupid = <cfqueryparam cfsqltype="cf_sql_integer"
value="#attributes.jurisdictiontypegroupid#">  
AND sh.jurisdictiontypeid = j.jurisdictiontypeid  
AND c.chaptercode = sh.chapterid  
AND s.chapterid = c.chaptercode  
)  
  
ORDER BY orderby, chaptercode, chaptername, sectionnumber  
</cfquery>  
```  
  
The end result was I was getting a nasty cartesian product. But the problem
just didn't jump out at me. All three tables were joined nicely - so what
gives? If your lucky then the problem jumps right out at you. But for me, I
wasn't so lucky. I spent a good twenty minutes mucking with this query in
PL/SQL Developer before I finally saw the problem.  
  
At first glance you might think the problem is related to the fact that the
join between "sh" and "c" is c.chaptercode = sh.chapterid and that the join
between "s" and "c" is also s.chapterid = c.chaptercode. It's good place to
start looking - but the wrong one. The tables were designed along time ago by
someone who once worked for the customer and we are just tasked with extending
some functionality around the existing tables - so please, don't complain
about the database design.  
  
Do you see the problem yet? Well it turns out that in each of the three parts
of the query sectionheader is defined twice. So the alias 's' and 'sh' are
totally redundant and thus things went whacky with an end result of hundreds,
maybe thousands more records being returned than necessary. As soon as I
removed referencs to the 'sh' version of the table everything came back to
normal. Sometimes I hate debugging - but it always feels good to get the
problem fixed.  
  
Why did it take me so long to figure this one out? Well first I starting
checking the jurisdictiontypegroupmapping table out to see if the mappings
were poorly defined - and thus giving me back extra data. Then I started
focusing on the actual joins making sure each aliased table had a join that
logically chained all of the tables together. Then I dropped the two union
parts of the query out. Then I started taking the remaining query apart one
table at a time, from the bottom up, to see where things went haywire. I
honestly never thought to study the "from" part of the clause because it
didn't occur to me that someone would alias the same table twice for reason.
Next time, perhaps, I check that first!

