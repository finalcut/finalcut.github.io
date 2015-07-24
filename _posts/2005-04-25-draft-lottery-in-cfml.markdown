---
layout: post
title: "Draft Lottery in CFML"
date: 2005-04-25
comments: false
categories:
 - coldfusion
 - draft
 - lottery
---
In the spirit of the recent NFL draft and the upcoming NFL Fantasy Football
season my league is preparing for an expansion draft. Draft order is
determined based on a format similar to the NBA's lottery where each team gets
some "n" number of entries in the lottery based on their past performance and
new expansion teams get 3+ Max(n) to give them a slight advantage in the
drawing.

Instead of tearing up a bunch of paper, putting it in a hat, and then doing a
manual drawing I decided to throw together some very quick procedural code
that will enable this. I'm sure there are better ways to accomplish it, but
this is what jumped out of my head first and I didn't really give it much
thought beyond that.

Basically, it is up to the user to define a structure of teams and their
number of tokens. The code then does a bunch of randomization and gives you a
draft order based on the total number of teams in the lottery. Finally, it
displays that draft order as an ordered list. Pretty simple eh? I borrowed a
function from cflib and totally revamped another for my needs. Both are given
credit in the very sparse comments in the following code.


```js
<cfscript>

/* SETUP
add each team to the team structure and assign them a number of lottery
entries
obviously, each team name must be unique
*/


teams = structNew();

/* add old teams here */
teams.nate = 1;
teams.mike = 2;
teams.bill = 3;
teams.beth = 4;
teams.drew = 5;


newTeamTokens = structCount(teams) + 3;

/* add new teams here */
teams.ed = newTeamTokens;
teams.dan = newTeamTokens;





/* DO NOT EDIT BELOW THIS LINE */

function ListRandomElements(theList, numElements) {
/**
* Returns specified number of random list elements without repeats.
*
* @param theList Delimited list of values. (Required)
* @param numElements Number of list elements to retrieve. (Required)
* @param theDelim Delimiter used to separate list elements. The default is the comma. (Optional)
* @return Returns a string.
* @author Shawn Seley (shawnse@aol.com)
* @version 1, July 10, 2002
*/
var theDelim = ",";
var final_list = "";
var x = 0;
var random_i = 0;
var random_val = 0;

var theArray = "";

if(ArrayLen(Arguments) GTE 3) theDelim = Arguments[3];

theArray = listToArray(theList,theDelim);

if(numElements GT ArrayLen(theArray)) {
numElements = ArrayLen(theArray);
}

randomize(TimeFormat(Now(),"mmss"));

// Build the new list "scratching off" the randomly selected elements from the
original list in order to avoid repeats
for(x=1; x LTE numElements; x=x+1){
random_i = RandRange(1, ArrayLen(theArray)); // pick a random list element
index from the remaining elements
random_val = theArray[random_i]; // get the corresponding list element's value
theList = ArrayDeleteAt(theArray, random_i); // delete the used element from
the list

final_list = ListAppend(final_list, random_val , theDelim);
}

return(final_list);
}

function ListRemoveItem(list1,item) {
/**
* Removes all instances ofa specific item from a list
*
* @param list1 Delimited list of values. (Required)
* @param item item to remove from the list
* @param theDelim Delimiter used to separate list elements. The default is the comma. (Optional)
* @return Returns a string.
* @author Bill Rawlinson - based on ListRemoveList by Ann Terrell (ann@landuseoregon.com)
* @version 1, April 25, 2005
*/
var listReturn = list1;
var position = 1;
var theDelim = ",";
if(ArrayLen(Arguments) GT 2) theDelim = Arguments[3];

while (ListFindNoCase(listReturn, item, theDelim) NEQ 0) {
listReturn = ListDeleteAt(listReturn, ListFindNoCase(listReturn, item,
theDelim), theDelim);
}

return listReturn;
}
</cfscript>

<cffunction name="getDraftPool" returnType="string">
<cfargument name="teamList" type="string">
<cfset var theDraftPool = "">
<cfset var tokens = 0>
<cfset var thisTeam = "">


<cfloop list="#arguments.teamList#" index="thisTeam">
<cfset tokens = teams[thisTeam]>
<cfloop from="1" to="#tokens#" index="someteam">
<cfset theDraftPool = listAppend(theDraftPool,thisTeam)>
</cfloop>
</cfloop>

<cfreturn ListRandomElements(theDraftPool,listLen(theDraftPool)) />
</cffunction>

<cffunction name="getPick" returntype="string">
<cfargument name="pool" type="string">
<cfset var pickedteam = "">
<cfset var theIndex = 0>

<cfif listLen(arguments.pool)>

<cfset randomize(TimeFormat(Now(),"mmss"))>
<cfset theIndex = RandRange(1,listLen(arguments.pool))>
<cfset pickedTeam = listGetAt(arguments.pool,theIndex) >
</cfif>

<cfreturn pickedTeam />

</cffunction>



<cffunction name="runLottery" returntype="string">
<cfset var teamNames = structKeyList(teams)>
<cfset var overallDraftPool = getDraftPool(teamNames)>
<cfset var pickedTeam = "">
<cfset var thisTeam = "">
<cfset var lotteryResults = "">

<cfsavecontent variable="lotteryResults">
<cfoutput>
<ol>
<cfloop list="#teamNames#" index="thisTeam">
<li>
<cfset pickedTeam = getPick(overallDraftPool)>

#pickedTeam#

<cfset teamNames = ListRemoveItem(teamNames,pickedTeam)>
<cfset overallDraftPool = getDraftPool(teamNames)>
<cfif ListLen(teamNames) EQ 0>
<cfbreak />
</cfif>
</li>
</cfloop>
</ol>
</cfoutput>

</cfsavecontent>


<cfreturn lotteryResults />

</cffunction>



<cfset results = runLottery()>
<cfoutput>#results#</cfoutput>

```


