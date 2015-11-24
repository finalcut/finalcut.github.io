---
layout: post
title: "Generate All Months Between Two Dates with Oracle"
description: using connect by and multiset to solve the tricky problem of finding all months between two dates in oracle.
headline: 
date: 2015-11-24 09:34:19 -0500
category: oracle
tags: [oracle,multiset,cast,table,odcinumberlist,add_months,connectby]
imagefeature: 
mathjax: 
chart: 
comments: true
featured: false
---

I have been working on an app that has a really slow report.  The report has to look across two entities; one table and another view.  The view is constructed by a union across six other materialized views.  It's a mess and the report took way too long to run.  In fact, the performance for no discernible reason was 1000x worse in production that it was in our UAT environment.  It was unacceptable and I needed to fix it.

The report answered the question: Of all the entities that have been reported, by their lessor (owner) as being rented out, which entities were not being reported as being rented by the lessee (borrower).  To make things tricky a lessee can sublet (become the lessor of) the entity and so forth ad-naseum.

Data provided by the lessor comes roughly in the format `{entityId: ####, startDate: mm/dd/yyyy, endDate: mm/dd/yyyy||null, lesseeId: ####}`  There are other fields but those are the most important ones for this discussion.  Note that the end date can be null meaning the entity is still actively on rent to the lessee.

This data basically makes up the first table in question the `entity_lessee` table


|entityId|startDate|endDate	  |lesseeId|lessorId|
|--------|---------|----------|--------|--------|
| 1		 |10/1/2001|null   	  |34      |8       |
| 2		 |8/5/2005 |11/19/2008|34      |8		|


The view titled `entity_detail` table is a table that is populted with new data everymonth.  Anyone that is currently responsible for the entity has to report on it each month and show how it is being used.  If they are leasing the entity they have to show that the entity is in use or that they have leased it out to another lessee.

The problem is not everyone remembers to report all their entities each month so we end up with records missing in various months.


The other table sort of looks like this:

|operatorId|entityId|startDate |endDate   |usage   |
|----------|--------|--------- |----------|--------|
| 34	   | 1      | 10/1/2001|10/31/2001|idle    |
| 34	   | 1		| 11/1/2001|11/15/2001|cleaning|
| 34	   | 1		|11/16/2001|11/30/2001|loading |


So what we need to do is show if there are records in the second table (`entity_detail`) for every month in the span between `startDate` and `endDate` in the first table (`entity_lessee`)  If the endDate is null then we can substitute the current date `SYSDATE` in it's place.  Also note that `entity_detail.operatorId` is synonymous with `entity_lessee.lesseeId`.  All lessors and lessees are defined in an operator table and have an `operatorId`.

  
When the report is run the user of the system would ask what entities that are being leased to lessee 34 between Jan 2006 and Jan 2007 where not reported by the lessee?  In the older, slow solution, we looped over the months in question and did a union of the x number of queries sort of like so:

```sql
SELECT el.entityId
  FROM entity_lessee el
WHERE el.startDate <= @LastDayOfMonth
  AND (el.endDate >= @FirstDayOfMonth || el.endDate IS NULL)
  AND NOT EXISTS
		(SELECT ed.entityId
  		   FROM entity_detail ed
		  WHERE ed.endDate BETWEEN  @FirstDayOfMonth AND @LastDayOfMonth
        )

UNION
... /* repeat for each subsequent month between @FilterStartDate and @FilterEndDate */
```

The first part of the query is the tricky part because there may not be a record in the `entity_lessee` table at all for Jan 2007 but we can see that both entity 1 and 2 were on lease during that month as the start date is before Jan 2007 and the end date is after Jan 2007.

What I needed to really have was another table or something that showed me all the discreet months an entity was on lease, who the lessor was and who the lessee is.  That's where the real point of this post comes into play - this query:

```sql
SELECT	el.entityId
	 	, el.lesseeId
		, el.lessorId
		, add_months(trunc(startDate, 'MM'),column_value-1) leaseMonth
  FROM  entity_lessee el,
		table(
			cast(
				multiset(
					SELECT level
					  FROM dual
					CONNECT BY add_months(trunc(startDate,'MM'),level-1) <= NVL(endDate, SYSDATE)
				)
				as sys.OdciNumberList
			)
		)
 WHERE add_months(trunc(startDate, 'MM'), column_value-1) IS NOT NULL
```

Now if you aren't familiar with most of those Oracle concepts you're probably thinking "WTF does that do and how does it do it?"

`table` basically just creates an in-memory table that we can join to.
`cast` converts the in-memory list that mutiset creates into a dataset that `table` can use.
`multiset` creates a list from the data generated within it and sets it to a known type by using `sys.OdciNumberList`
`add_months` just does numeric arithmatic on date values.
`trunc` in this case is converting the `startDate` value into the first day of the month of the `startDate`
`CONNECT BY` is the magic creates the heirarchy of months.  Basically creating a list of months from the `startDate` to the `endDate`.  The join between the two tables basically creates a Cartesian Product resulting in a record for the entity for each month in the span from `startDate` to `endDate`

 
You can test the idea out without having a table other than `dual` like so:

```sql
SELECT ADD_MONTHS('1 JAN 2011', column_value - 1) as m
		FROM TABLE(
				CAST(
				MULTISET (SELECT level
								 FROM dual
								 CONNECT BY ADD_MONTHS('1 JAN 2011', level - 1) <= '1 OCT 2011'
						) as sys.Odcinumberlist
					)
				)
```

m         |
-----------
|1/1/2011 |
|2/1/2011 |
|3/1/2011 |
|4/1/2011 |
|5/1/2011 |
|6/1/2011 |
|7/1/2011 |
|8/1/2011 |
|9/1/2011 |
|10/1/2011|


You can further break it down to see what happens by doing this:

```sql
SELECT ADD_MONTHS('1 JAN 2011', column_value - 1) as m, t.*
		FROM TABLE(
				CAST(
				MULTISET (SELECT level
								 FROM dual
								 CONNECT BY ADD_MONTHS('1 JAN 2011', level - 1) <= '1 OCT 2011'
						) as sys.Odcinumberlist
					)
				) t
```


| m        |t*|
|---------|---|
|1/1/2011 | 1|
|2/1/2011 | 2|
|3/1/2011 | 3|
|4/1/2011 | 4|
|5/1/2011 | 5|
|6/1/2011 | 6|
|7/1/2011 | 7|
|8/1/2011 | 8|
|9/1/2011 | 9|
|10/1/2011| 10|


`t.*` will give you the list of numbers that the table creates.  Basically you can see then that what is going on is that for each entry in the in memory `table` [1,2,3,4,5,6,7,8,9,10] the line `ADD_MONTHS('1 JAN 2011', column_value-1)` will do some date math.  For the first value 1 it adds zero (column_value-1) and thus you still get back 1 JAN 2011 and for the last value, ten, it adds 9 months and thus you get back `1 OCT 2011`.

 
The final reward for figuring this out was that the report generation time went down substantially.  For instance in UAT where the report, when run for a single year, took roughly 20 seconds to execute; now it takes about 0.4 seconds and the report runs equally well in production.

To further optimize performance I created a materialized view `entity_on_lease_by_month` of this query which I was then able to index.  My final report query looks somewhat like this:

```sql
SELECT
		lm.entityId,
		lm.lesseeId,
		lm.lessorId,
		lm.leaseMonth
  FROM entity_on_lease_by_month lm
WHERE lm.leaseMonth BETWEEN @filterStartDate AND @filerEndDate
AND NOT EXISTS (
	SELECT ld.entityId
      FROM entity_detail ed
	 WHERE ed.entityId = lm.entityId
	   AND ed.operatorId = lm.lesseeId
	   AND TRUN(ed.endDate, 'MON') = lm.leaseMonth )
```

Please let me know if what I wrote about the improved query isn't clear enough or doesn't make sense and I'll try to clarify.  A lot of this post was to help me gather my thoughts and to get a better understanding of what the solution does and how/why it works.