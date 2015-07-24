---
layout: post
title: "10% Programming Challenge : Binary Search in ColdFusion"
date: 2010-04-20
comments: false
categories:
 - coldfusion
 - recursion
 - binary-search
 - iteration
 - binarysearch
 - computer-science
---
Yesterday I came across [a programming article that basically stated that only
10% of programmers could successfully write a binary search
function](reprog.wordpress.com/2010/04/19/are-you-one-of-the-10-percent/). I
don't know how true the statement is but I can rarely turn down a challenge so
I decided to give it a go.

Before I show you my solution(s) here is the defintion of binary search
provided in [the linked article](reprog.wordpress.com/2010/04/19/are-you-one-
of-the-10-percent/):


> Binary search solves the problem [of searching within a pre-sorted array] by
keeping track of a range within the array in which T [i.e. the sought value]
must be if it is anywhere in the array. Initially, the range is the entire
array. The range is shrunk by comparing its middle element to T and discarding
half the range. The process continues until T is discovered in the array, or
until the range in which it must lie is known to be empty. In an N-element
table, the search uses roughly log(2) N comparisons.



If you are interested in attempting the challenge yourself don't keep reading
until you've finished the challenge; then come back here and share your
thoughts.

Initially I decided to write my solution recursively because I tend to think
that way more naturally and here was my solution:


```cfc
<cffunction name="binarySearchRecursive" returntype="boolean"
output="false">
<cfargument name="ary" type="array" required="true" />
<cfargument name="val" type="string" required="true" />

<cfset var l = structNew() />

<cfif ArrayLen(arguments.ary)>
<cfif ArrayLen(arguments.ary) GT 1>
<cfif ArrayLen(arguments.ary) EQ 2>
<cfreturn VAL((arguments.ary[1] EQ arguments.val OR arguments.ary[2] EQ
arguments.val))>
<cfelse>
<cfset l.pos = Round(ArrayLen(arguments.ary)/2) />

<cfif arguments.ary[l.pos] EQ arguments.val >
<cfreturn 1 />
<cfelseif arguments.ary[l.pos] GT arguments.val>
<cfset arguments.ary = ArraySplit(arguments.ary, 1, l.pos) />
<cfelse>
<cfset arguments.ary = ArraySplit(arguments.ary, l.pos,
ArrayLen(arguments.ary)) />
</cfif>

<cfreturn binarySearchRecursive(arguments.ary, arguments.val) />
</cfif>

<cfelse>
<cfif (arguments.ary[1] EQ arguments.val)>
<cfreturn 1 />
<cfelse>
<cfreturn 0/>
</cfif>
</cfif>
<cfelse>
<cfreturn 0 />
</cfif>
</cffunction>

<cffunction name="ArraySplit" returntype="array">
<cfargument name="ary" type="array">
<cfargument name="sp" type="numeric">
<cfargument name="ep" type="numeric">

<cfset var l = structNew() />
<cfif arguments.ep LT arguments.sp>
<cfthrow message="End Point must be greater than or equal to the starting
point" />
</cfif>
<cfif arguments.ep GT ArrayLen(arguments.ary)>\
<cfthrow message="End point can not be greater than the size of the array
to split" />
</cfif>
<cfif arguments.sp GT arguments.sp>
<cfthrow message="Start Point must be less than or equal to the size of the
array to split" />
</cfif>

<cfset l.a = ArrayNew(1) />
<cfloop from="#arguments.sp#" to="#arguments.ep#" index="l.i">
<cfset ArrayAppend(l.a, arguments.ary[l.i]) />
</cfloop>


<cfreturn l.a />
</cffunction>

```


As you can see I also had to write a function to split an array. In my initial
effort I did not take into consideration an empty array being passed in but
this final example I'm showing fixes that bug. Because of that bug I guess I
fell outside the 10% of people who do this successfully on their very first
try though I saw the problem in my code before looking at any other examples
or reading any of the comments in the aforementioned post.

I also thought that I should challenge myself and try to write the function in
an iterative fashion that wouldn't have the dependency on the ArraySplit
function. The recursive solution took me about 5 minutes to write; the
iterative one took me closer to 20; it's just not how I think so I had to give
some deep thought to my looping conditional. Anyway, here it is for comparison
sake:


```cfc
<cffunction name="binarySearchIterative" returntype="boolean"
output="false">
<cfargument name="ary" type="array" required="true" />
<cfargument name="val" type="string" required="true" />
<cfset var l = structNew() />

<cfif ArrayLen(arguments.ary) EQ 0>
<cfreturn 0 />
<cfelseif ArrayLen(arguments.ary) EQ 1>
<cfreturn arguments.ary[1] EQ arguments.val />
<cfelse>
<cfset l.min = 1>
<cfset l.max = ArrayLen(arguments.ary) />
<cfloop condition="l.max GTE l.min">
<cfset l.mid = l.min + Round((l.max-l.min)/2) />
<cfset l.value = arguments.ary[l.mid] />
<cfif l.value EQ arguments.val>
<cfreturn 1 />
<cfelseif l.value GT arguments.val>
<cfset l.max = l.mid - 1 />
<cfelse>
<cfset l.min = l.mid + 1 />
</cfif>
</cfloop>
<cfreturn 0 />
</cfif>
</cffunction>

```


To be honest it is a heck of a lot cleaner and I like it a lot more. It also
turns out to be a heck of a lot faster which we shall see in a second. Here is
my basic performance test harness:


```cfc
<cfset myAry = ArrayNew(1) />
<cfloop from="1" to="9000" index="i">
<cfset ArrayAppend(myAry,i) />
</cfloop>


<cffunction name="testBS" output="true">
<cfargument name="ary" />
<cfargument name="func" />
<cfargument name="ftype" />


<cfoutput><h2>#fType# Binary Search</h2></cfoutput>
<cftimer
label="#ftype# total time: "
type="outline">
<cfoutput><pre>
#arguments.func(ary, 8)#
#arguments.func(ary, 13)#
#arguments.func(ary,0)#
#arguments.func(ary,100)#
#arguments.func(ary,190)#
#arguments.func(ary,504)#
#arguments.func(ary,700)#
#arguments.func(ary,893)#
#arguments.func(ary,9876)#
#arguments.func(ary,5001)#
#arguments.func(ary,2091)#
#arguments.func(ary,9010)#
#arguments.func(ary,9999)#
#arguments.func(ary,109876)#
#arguments.func(ary,-2321)#
</pre></cfoutput>
</cftimer>
</cffunction>

<cfset testBS(myAry,binarySearchIterative,"Iterative") />
<cfset testBS(myAry,binarySearchRecursive,"Recursive") />

```


On average the iterative tests run in about 15-20ms while the recursive option
runs in about 650-700ms. There are some obvious reasons for this the first
being my ArraySplit function which could probably be written a lot better.
However, I also remember that, inherently, [recursion is
slow](http://www.informit.com/articles/article.aspx?p=1390173&seqNum=3).

Finally, you may note that I get my "mid" point a little strangely using the
(min + ((max-min)/2)) process. I do this because I actually remembered reading
[this article](http://googleresearch.blogspot.com/2006/06/extra-extra-read-
all-about-it-nearly.html). That article is also linked to via the challenge
page. What's funny is that I remembered the nugget about min + (max-min)/2 to
get the mid point but I didn't remember the context which just happens to be a
Binary Search function post. I had completely forgotten WHY I did it that way
but I'm glad the basic rule at least stuck into my brain from whenever I had
read that post previously. To be truthful I doubt any code I ever write in CF
will need that type of protection against overflows - I've never worked with
an Array anywhere near 230 elements long so I would undoubtedly be safe using
just l.mid = (l.min+l.max)/2

## Comments

Bill

Rick,

Sorry I just saw your comment about teaching the web design degree. I agree
that nobody can learn everything in 4 years! Heck, even if you tried so much
new stuff could come out during that 4 years it would be just as if you are
starting over again.

I was asked to teach a course in advanced web development at a community
college once. It was not an easy task in part because I expected the students
to know more than they did by that point and in part because I had so much
material to cover in one semester.

The students did not appreciate my approach but I didn't really feel like I
had many options - they were woefully unprepared for their capstone course.

I was supposed to be teaching databsae driven webdevelopment but they didn't
even have a good grasp of HTML and yet I was supposed to teach them SQL and
asp.net? I was not asked to come back and teach again.

I spent most of the semester teaching them HTML and and ColdFusion because I
figured they would be able to learn CF faster due to its tag based syntax.

Bill

I think I would only use this as a type of interviewee if it was applicable to
their job.

If a candidate admitted they weren't familiar with the term "binary search"
I'd be a little surprised but if they could take the definition and create
something that basically worked I'd be satisfied. In fact if someone didn't
know what a binary search was and just try to BS me I'd be pretty
disappointed. Asking a question for additional information is a plus (so long
as you can actually do the work once you have the info).

Personally, in my little corner of the geek circle I don't care if anyone ever
asked me what "Binary Search" was. In fact, in general, I don't like talking
about what I do for a living with people who don't do similar things. Most of
the crap I do isn't very easily explainable beyond big general concepts. I
doubt that is particularly unique to my career field either (considering, in
order to build custom software I'm constantly having to learn how other people
do their job and how difficult it can be for them to really explain what they
do).

Jake Munson

I'd guess that a big portion of the other 90% don't even know what "binary
search" means. I'll admit that I didn't until I read your pasted definition.
After reading it, I said to myself, "Oh yeah, I know how to do that!"

I think this kind of thing is common in geek circles. We like to use acronyms
and big words, and we are partly hoping people will ask us, "Wait, what does
binary search mean?" because then we feel smarter. And to make matters worse,
there are often multiple terms that mean the same thing (when you travel
between different programming languages, for example.)

I can see this being an interview question, "Demonstrate with pseudo code that
you can write a binary search." And the poor interviewee is sitting there
wracking their brain for that long lost definition that they forgot 10 years
ago. And of course, if you ask what the term means, you don't get the job
(because they think you obviously aren't good enough if you don't know what
binary search means). If you don't demonstrate it correctly, you don't get the
job. Double edged sword. Meanwhile, this interviewee may well be the best
candidate among the lot, if given a chance.

Rick O

The degree that I teach for is a BS in "Web Design and Development". It's
_not_ a CS degree. We don't explicitly teach how to code algorithms like sorts
and searches. Instead, our students get HTML, CSS, JavaScript, jQuery, Flash,
Flex, PHP, SQL, and ColdFusion -- and a bunch of other non-programming web
technology courses, such as rich media streaming technologies.

Of course, we're always asked why the degree isn't a CS degree, and why we
don't teach the hard stuff. But flip the question around: why don't CS degrees
go into even half of what we do? There's just not enough time to cover both in
a 4-year degree.

You could argue that the CS student would have a solid enough base to be able
to pick up on any of those technologies ... but you could also argue that our
students are familiar with a breadth of technologies, and those technologies
don't change all that fast, so they'll probably transition just as easily into
new technologies.

The reality is that there's room in the world for both types of degrees and
both types of web devs. Some of our students are simply amazing designers and
developers, some of them even have a CS background (or future), and many of
them will be content somewhere in the middle of the two.

(I, too, come from a hard CS background. I'll admit that I occasionally have
to stop and remind myself that I'm _not_ teaching a CS degree. When all you
have is a hammer... )

Bill

Good comment Rick. I'm in the CS camp personally; but I enjoy both the
creative and the algorithmic side of things. I just wish had some graphic
design skills so that, on occasion, I could put a pretty face on something I
was building.

I work in a pretty small shop (about 10-15 developers) and we do almost no
public facing web work but the majority of the web stuff we do is in CF.

Our path into CF development was pretty funny. A marketing guy who used to
work here misunderstood someone and thought they were talking about net
objects fusion back when CF was still at 3.5 or 4. He told the prospective
customer we had plenty of experience with CF and so that day we started
learning CF so that if the customer called back we could actually build what
they wanted; they did, we did, and the rest (as they say) is history.

Rick O

If you look back at the history of web development, it's followed a twisty
path.

In the beginning, early to late 90s, pretty much anyone doing web work had a
CompSci degree. Everything was new and difficult and had to be coded by hand,
so if you didn't have a CS degree you were behind a very large 8-ball.

Then, at the end of the decade, something weird happened: the non-CS-folks
(read: creatives) got really fed up with being out of the loop. They pushed
back hard, and we got things like Flash and ColdFusion and WYSIWYG editors --
a whole slew of technologies that didn't require a CS degree to use. It took
those technologies a number of years to really take hold in the market, but as
they grew they shifted from making things easier for CS-minded people, to
making things easier for the entry-level web dev.

By the mid 2000s we were beginning to see a new class of web dev: people that
had **only** ever used those "soft" web dev technologies. These were people
without a CS degree. They weren't raised on algorithms and data structures and
memory/performance optimization. These folks began to dominate the market for
one simple reason: they didn't try to overengineer their deliverables, as they
hadn't been pumped full of waterfall methodology and all that rot.

ColdFusion developers are a great example of this entire lifecycle.

But now it's beginning to come full circle: as we begin to have to face
questions of scale, it's becoming apparent to the new guys that they aren't
quite up to the task of making the really big stuff even bigger. There's
beginning to be a real distinction between web development, web design, and
web programming. I think this is great -- it makes it easier for employers and
employees to figure out what they want and what they want to be.

