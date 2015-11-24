---
layout: post
title: "CF Pleasantly Suprised Me"
date: 2005-08-30
comments: false
category: [coldfusion,sql]
tags: [oracle]
---
Today I was working on a project dealing with large sets of data in an Oracle
9i database (over 200k records in our subset for development purposes). The
data is pretty basic but I needed to generate a "rollup" report that
summurized at different levels the financials information stored in the db.

I had to show the information rolled up to three levels (Organization,
Department, Team) where a department is comprised of teams and an organization
is comprised of departments. The data was all stored in reference to a team
and the amount of time the spent on any given day using any specific
application within a collection of applications that are constantly audited
for usage amount.

Each application has a different cost associated with it's use based on the
month of usage.

My report needed to show the total costs for the organization, department, and
team for each month as well as a grand total for each over the year. (you may
have to scroll down to see the sample and further analysis for no obvious
reason a TON of whitespace is being inserted...)


Sample Report

```
Organization
| Department
| Team
| Jan
| ...
| Dec
| Total

---|---|---|---|---|---|---



US
| $xx.xx
| $xx.xx
| $xx.xx
| $yy.yy



| Accounting| $xx.xx| $xx.xx| $xx.xx| $yy.yy


| Receivable| $xx.xx| $xx.xx| $xx.xx| $yy.yy


| Payable| $xx.xx| $xx.xx| $xx.xx| $yy.yy


EUR
| $xx.xx
| $xx.xx
| $xx.xx
| $yy.yy



| Accounting| $xx.xx| $xx.xx| $xx.xx| $yy.yy


| Receivable| $xx.xx| $xx.xx| $xx.xx| $yy.yy


| Payable| $xx.xx| $xx.xx| $xx.xx| $yy.yy
```


Initially my plan was to have some functions on the oracle db that could get
each months totals and the annual totals and return them with the query. But
that meant I would need to call 39 functions per row of the query if I wanted
to return all the data in one query (12 months + 1 total for each
org/dept/team)

This approach proved to be painfully slow. Excruciatingly slow. Unacceptably
slow.

So, I decided to just pull back the basic data; organization, department,
team, month of usage, year of usage, duration of usage, and rate (cost per
hour of usage). Then I looped over this information building a big array of
structures that stored all of my information in a logical way - with all the
summary data included in each level of the structures:


```cfc
<cfscript>
orgs = arrayNew(1);

orgData = structNew();
orgData.organization = '';
orgData.jan = 0;
orgData.feb = 0;
...
orgData.dec = 0;
orgData.total = 0;
orgData.departments = arrayNew(1);

...
depData = structNew();
depData.department = '';
depData.jan = 0;
...
depData.dec = 0;
depData.total = 0;
depData.teams = arrayNew();
...
</cfscript>

```


This solution was remarkably fast. Lightening fast. The Oracle solution for
the same dataset took well over 100x longer to fetch the data as did the CF
solution of aggregating the data once I had the minimum.

The primary reasons for this, as far as I can tell

All of the data I have to read is in a view so the view is executed each time
the function is called whereas with the CF only solution the view is only
executed once (as opposed to thousands of times depending on how the requested
report is being filtered).
