---
layout: post
title: "CF: QueryIntersect UDF"
date: 2009-11-05
comments: false
categories:
 - coldfusion
 - query
 - user-defined-function
 - unit-testing
 - udf
---
Today I needed a function that would return the intersection of two query
objects (think Matrices and Sets). If you aren't that familiar with
intersections basically what this function does is it returns a query object
that contains each cell where the two queries were equal. Thus if you send in
two queries with 10 different columns (excpet one of which in both is
"firstname") and in both queries, in the 3rd row, the firstname was "richard"
but nothing else about the two queries was equal then the return query would
have a bunch of empty rows with one column (firstname) - and the firstname
value of the third row would be richard.

One of these probably already exists out on the web somewhere but I wanted to
write it myself and so I did.

A couple of caveats - 1. I know the variable naming sucks; I am lazy; so deal
with it. I don't like having to "var" everything and I don't like typing
"local" all the time; so I used very short and not very clear names. That's ok
though becuase I also give you a unit test to show you that the function works
the way I expect it to. Anyway, it's a pretty short function that you can
easily update if you want it to be more readable.


```cfc
<cffunction name="QueryIntersect" access="public" output="false"
returntype="query">
<cfargument name="q1" type="query">
<cfargument name="q2" type="query">

<cfset var l = structNew() />
<!---
grab all the column names that are the same between the two incoming queries
\--->
<cfset l.colNames = "" />
<cfloop list="#q2.columnList#" index="l.c">
<cfif ListFindNoCase(q1.columnList,l.c)>
<cfset l.colNames = listAppend(l.colNames, l.c) />
</cfif>
</cfloop>

<cfset l.q = QueryNew("#l.colNames#") />

<cfset l.max = q1.recordCount />
<cfif q2.recordCount LT q1.recordCount>
<cfset l.max = q2.recordCount>
</cfif>

<cfloop from="1" to="#l.max#" step="1" index="l.s">
<cfset QueryAddRow(l.q) />
<cfloop list="#l.colNames#" index="l.i">
<cfif q1["#l.i#"]["#l.s#"] EQ q2["#l.i#"]["#l.s#"]>
<cfset querySetCell(l.q,l.i,q1["#l.i#"]["#l.s#"]) />
</cfif>
</cfloop>
</cfloop>

<cfreturn l.q />

</cffunction>

```


Here is the unit test

```cfc
<cffunction name="QueryIntersectTest" access="public" output="false">

<cfset var q1 = QueryNew("id,name,title") />
<cfset var q2 = QueryNew("name,email,id") />
<cfset var q3 = "" />

<cfscript>
QueryAddRow(q1);
QuerySetCell(q1,"id","1");
QuerySetCell(q1,"name","bill");
QuerySetCell(q1,"title","chief");

QueryAddRow(q1);
QuerySetCell(q1,"id","2");
QuerySetCell(q1,"name","carl");
QuerySetCell(q1,"title","bozo");


QueryAddRow(q2);
QuerySetCell(q2,"id","1");
QuerySetCell(q2,"name","tom");
QuerySetCell(q2,"email","tom@bob.com");

QueryAddRow(q2);
QuerySetCell(q2,"id","4");
QuerySetCell(q2,"name","carl");
QuerySetCell(q2,"email","carl@r.org");


QueryAddRow(q2);
QuerySetCell(q2,"id","3");
QuerySetCell(q2,"name","ted");
QuerySetCell(q2,"email","cop@pork.com");

q3 = QueryIntersect(q1,q2);

AssertTrue(q3.recordCount EQ q1.recordCount,"the wrong number of rows were in
the intersection");
AssertTrue(ListFindNoCase(q3.columnList,"id"), "id should be a column");
AssertTrue(ListFindNoCase(q3.columnList,"name"), "name should be a column");
AssertTrue(q3.id EQ 1, "first row id should have intersected");
AssertTrue(q3.name EQ "", "first row name should not have intersected");
AssertTrue(q3["id"][2] EQ "", "second id should NOT have intersected");
AssertTrue(q3["name"][2] EQ "carl", "second name should have intersected");

</cfscript>

</cffunction>

```


I'll probably post another one later that does an intersection of all the rows
in a single query as well. (I updated the unit test to better reflect what
this function does).

## Comments

Bill

Yeah the intersection is basically like matrice intersection. I just happen to
be using a Query structure to store my matrix.

Bill

Sorry to be such a noise maker.. But I figure I should explain my purpose for
this function.

Imagine you have a train that goes from station A to Station B then to Station
C and then again to Station D The train is responsible for logging its trips
in some format and then transferring their log to me, the parent company, on a
regular basis. Now lets say the train forgot to log the trip between B and C
and only logged the A-B and C-D. Someone in the parent company knows the train
(maybe via a verification phone call) that B-C happened, but the data isn't in
the system. So they want to quickly create a record for that trip.

A lot of the information might be the same - but maybe not some things (for
instance when the train got to D it might have had 1000 tons of coal and no
iron ore but when it left A it had both coal and iron ore).

I want to prepopulate the new trip creation form with everything that was
consistent between leaving and and leaving C.. Then the user has to manually
fill in the rest of the stuff that is "different" (and they might change some
of the intersecting data as well).

Hopefully this example (not an actual one) will clarify one place where such a
function would be useful.

Ben Nadel

Hmmm, sorry, I think I misunderstood where you were intersecting - I think I
am wrong.

Bill

well email is a bad example since that column isn't returned.. but if I change
Carls id in the second query the name carl should still come back even though
the id shouldn't.

Bill

hrm. the more I think about it the less I still think it will work - for
instance in my example from the unit test the two queries being passed in in
Row 1 nothing intersects - I think both solutions would handle that.

However, in row 2 only the name and id fields should come back populated - the
email field should be blank - I don't think the QoQ will handle that - at
least I'd be surprised if it did.

We shall see shortly!

Bill

Ok well I'll try it out and see what happens - my curiosity is piqued.

Ben Nadel

When you join two queries in a query of queries, it implies that it will be on
a Row-by-row basis (hence you don't have to provide the row number).

But, like I said, the two concepts are exactly similar - I'm not recommending
you switch - I was just trying to clarify what Rick was saying.

Bill

I dunno - maybe I'm just not getting what your saying but it seems to me that
a query of the two queries will result in me getting back rows where
q1.colX[row1] = q2.colX[row5] which I don't want. I only want it to come back
if q.colX[row1] = q2.colX[row1]

Maybe in the query of queries you can also join on the rownumber metadata and
I just don't know it but if not I am not sure what your saying will work.

Ben Nadel

I think what Rick was saying was that you could perform the same logic you are
performing (comparing each column) inside of query of query:

SELECT
*
FROM
q1, q1
WHERE
... loop to compare q1[col] = q2[col]

Same exactly concept, just moving the comparison into the WHERE statement.

However, within a query of queries, you *might* run into strange data type
casting issues that you won't experience in your CFLoop solution.

Bill

Sorry Rick, I don't follow your logic? There is no problem where data doesn't
match up perfectly as far as I know - this intersection does what I expect
(though, perhaps I don't explain that well).

Please let me know what, in your suggestion, I'm missing. Thanks.

Rick O

Instead of doing the manual loop, why not use a Query of Queries? This would
also solve the problem where the column data doesn't match up perfectly.

