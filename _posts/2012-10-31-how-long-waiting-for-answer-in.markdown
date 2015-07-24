---
layout: post
title: "How Long Waiting for an Answer in StackOverflow - An Addendum"
date: 2012-10-31
comments: false
---
Today I came across a post titled "[How Long Waiting for an Answer in
StackOverflow](http://blog.guillermowinkler.com/blog/2012/10/30/how-long-
waiting-for-an-answer-in-stackoverflow/)" that uses a cool service [built into
StackOverflow to query the data](http://data.stackexchange.com/faq).
Guillermo Winkler, the author of that post, was  thoughtful enough to provide
the queries he used however, there were still some people who complained that
Perl and Python weren't included in the mix.  So, to appease (call me
Chamberlain), I modified his query that includes "difficulty level" and
included Perl, Python, and for my own curiosity, ColdFusion and ran it.  It
took about 93 seconds to run the full query so, in order to spare the
StackOverflow servers I'm sharing the results here.



```

TagName  DifficultyGroup Total Average StandardDev

c   Easy   22684 27  44.93158724

c   Hard   844  3681 2054.32233

c   Hell   624  65729 100305.4377

c   Medium   1479 660  332.5307891

c#   Easy   101671 29  47.99106764

c#   Hard   6395 3790 2036.896902

c#   Hell   5109 69559 101441.9676

c#   Medium   9252 734  351.5870257

c++   Easy   47099 27  44.72630576

c++   Hard   1926 3769 2004.750274

c++   Hell   1623 66865 96822.88407

c++   Medium   3447 691  339.3129365

clojure  Easy   1243 59  61.88653835

clojure  Hard   92  3457 2029.433055

clojure  Hell   57  99400 115464.8556

clojure  Medium   306  626  300.5990237

coldfusion Easy   1241 53  58.8145155

coldfusion Hard   123  3662 1840.082258

coldfusion Hell   75  70134 92203.96548

coldfusion Medium   252  732  332.8786129

haskell  Easy   3479 45  57.02075156

haskell  Hard   148  3487 1779.395102

haskell  Hell   118  65520 87998.77949

haskell  Medium   496  608  298.0567828

java  Easy   85766 31  48.89842231

java  Hard   5907 3765 2010.932162

java  Hell   5197 71558 101831.4202

java  Medium   8826 717  345.5430699

javascript Easy   86375 25  42.91600968

javascript Hard   4685 3784 2025.935042

javascript Hell   4320 73794 101298.4912

javascript Medium   6531 728  344.8005289

lua   Easy   713  58  63.46671507

lua   Hard   76  3243 1652.483831

lua   Hell   46  53789 78578.61928

lua   Medium   199  672  328.4408645

perl  Easy   5997 43  55.91177132

perl  Hard   257  3664 1967.493456

perl  Hell   174  65605 85205.42372

perl  Medium   697  641  318.448049

php   Easy   88927 23  42.9707536

php   Hard   4047 3782 2021.484997

php   Hell   3512 73866 103946.8728

php   Medium   5901 714  335.4683515

python  Easy   38519 35  52.08066926

python  Hard   2475 3733 1982.435262

python  Hell   2096 80801 112891.3908

python  Medium   4454 675  330.5440297

ruby  Easy   16659 41  54.92089149

ruby  Hard   1274 3826 2012.591462

ruby  Hell   1263 79333 106803.6384

ruby  Medium   2135 682  337.2806176

scala  Easy   3891 56  61.98182303

scala  Hard   276  3245 1808.706038

scala  Hell   211  73277 106251.322

scala  Medium   834  623  316.2735868


```




A friend has put [this data in a google spreadsheet](https://docs.google.com/spreadsheet/ccc?key=0At9xIZA2GNQYdEdwVklzNTFaSEllSGpkSnpwQlY5dGc#gid=0) so you can filter/sort it.


I encourage you to go read his post and then use this as an additional reference while reviewing his analysis.


For reference purposes here is the query I ran to obtain the above results:



```sql
SELECT DifficultyGroup, COUNT(1) Total,

       AVG(CAST(ResponseTime AS bigint)) AS Average,

       STDEV(CAST(ResponseTime AS bigint)) AS StandardDev,

       TagName

FROM

  (SELECT

         Questions.CreationDate,

         Questions.Title,

         Tags.TagName,

         Answers.CreationDate AS ResponseDate,

         DATEDIFF(minute, Questions.CreationDate, Answers.CreationDate) AS ResponseTime,

         CAST(DATEPART(hour, Questions.CreationDate) as int) as ResponseHour,

         CASE

              WHEN DateDiff(hour, Questions.CreationDate, Answers.CreationDate) < 5   THEN 'Easy'

              WHEN DateDiff(hour, Questions.CreationDate, Answers.CreationDate) < 24  THEN 'Medium'

              WHEN DateDiff(hour, Questions.CreationDate, Answers.CreationDate) < 144 THEN 'Hard'

              ELSE                                                                         'Hell'

         END as DifficultyGroup

    FROM Posts Questions

    JOIN Posts Answers ON Answers.id = Questions.AcceptedAnswerId

    JOIN PostTags ON PostTags.PostId = Questions.Id

    JOIN Tags ON Tags.Id = PostTags.TagId

    WHERE Questions.CreationDate > CONVERT(datetime, '01/01/2011', 101)

                 AND TagName  IN ('ruby', 'c++', 'c', 'clojure',

                          'scala', 'javascript', 'haskell',

                          'c#', 'java', 'lua', 'php', 'coldfusion', 'perl', 'python')

) AS Responses

GROUP BY DifficultyGroup, TagName

ORDER BY TagName, DifficultyGroup


```







## Comments











Ade






Interesting.

Would be good to see a break down of

tech, difficulty, was answered

or

tech, difficulty, number of responses










