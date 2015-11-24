---
layout: post
title: "Build Dynamic Breadcrumbs"
date: 2005-02-25
comments: false
category: coldfusion
tags: [breadcrumbs]
---
I posted about this before but today I did a rewrite which I think is a bit
cleaner. It is safe to use on CF 5 and above. I suppose it would work on 4.5
but I don't have that installed anymore and haven't tested it. Nor do I
remember if wddx was supported in pre CF 5.

I have seen other "breadcrumb" solutions before but they deal with directory
structure and don't necessarilly maintain all of the arguments that need to be
passed around in order to make each page in your traversal history work. This
solution does.

A couple of notes before I dig into the code:
1\. It requires client variables are enabled. Now, you could switch this with
session variables if you want but I use client variables. Replace as you need
to.
2\. It uses WDDX to store the entire breadcrumb structure in a client
variable.

There are a couple of things that are done kind of poorly as well - feel free
to comment on those if you want. Maybe you will see some things that I didn't.

The setup uses three files - but really it can be reduced to two. The third
file just contains a simple UDF that I had written previously and since I
already need it elsewhere in the application I keep it in it's own "functions"
file.


I'll start with the functions.cfm file and it's sole applicable function for
this process: "ArrayLeft()". This takes in an array and a count 'x' and
returns a trimmed version of the array down to length 'x'.


```cfc
function ArrayLeft(array,numElements){
var tArray= ArrayNew(1);
if (numElements gte arrayLen(array)){
return array;
}
for (i=1; i LTE numElements; i=i+1){
tArray[i] = array[i];
}

return tArray;
}

```


The second file is where alot of the good stuff happens. I called it
build_url_string.cfm and I call it as a custom tag. I keep this file in the
same directory as the other two instead of putting it off in the "Custom Tag"
directory.

Sorry, no syntax highlighting available and indention is lost by this blog
editor - but here is the file
===================================================================
// build_url_string.cfm
===================================================================

```cfc
<!--- build_url_string.cfm - Copyright (c) 2005 SBCS, Inc. --->
<!--- build_url_string.cfm - Copyright (c) 2005 SBCS, Inc. --->

<!---
Description:
I build a structure that contains all the information needed to build a
hypertext link to the current page.
Parameters:
@param pageVariable if you use a "switch" type mechanism and everything runs
through index.cfm - then what
is the name of the variable you switch on: ie: index.cfm?page=thisPage or
index.cfm?fuseaction=go
the pagevariables would be page and fuseaction respectively.

@param pageCaption the name of the current page. Basically the title or what
ever it is you want displayed in
the breadcrumb trail for this page.

@param ignoreAttrs a comma delmited list of attribute keys to ignore. As
attribues is a structure, you just provide
a list of keys to not include in the breadcrumb URL.

@param returnVariable the variable you want populated. This tag returns a
structure of the form:
struct
struct.link - the base url with the first "pageVariable" if one exists
struct.text - the text you want displayed. Basically just a copy of
pageCaption
struct.args - a string of argumnents to append to the link.

so if you wanted to display this link you would:

<cfoutput><a
href="#struct.link#">#struct.link##struct.args#</a></cfoutput>

you don't have to figure out if a ? or a & goes between url and arguments as
it
is built into the struct.args value that is returned

the link and the argument are separated for a reason as it provides the most
flexibility
for any calling file.

Usage:

<cf_build_url_string
attributeCollection="#attributes#"
pageVariable ="page"
pageCaption ="Home Page"
ignoreAttrs ="comma,delmited,list,of,attributes,to,ignore"
returnVariable ="urlInfo">


Revision History:
2/25/2005 wmrawlin this header block finally added after a complete rewrite.

\--->
<cfparam name="attributes.pageCaption" type="string" default="">
<cfparam name="attributes.pageVariable" type="string" default="">
<cfparam name="attributes.ignoreAttrs" type="string" default="">


<!--- define our return structure --->
<cfset urlInfo = structNew()>
<cfset urlInfo.link =
ListGetAT(cgi.script_name,ListLen(cgi.script_name,"/"),"/")>
<cfset urlInfo.text = attributes.pageCaption>
<cfset urlInfo.args = "">

<!--- make sure the current pageVariable is ignored --->
<cfset attributes.ignoreAttrs =
ListAppend(attributes.ignoreAttrs,attributes.pageVariable)>

<!--- make sure some special attributes are ignored --->
<cfset attributes.ignoreAttrs = ListAppend(attributes.ignoreAttrs,"ignoreAt
trs,pageCaption,attributeCollection,pageVariable,returnVariable")>

<!---
try to figure out what arguments were passed in via
form and url or arguments
\--->
<cfloop List="#StructKeyList(attributes)#" Index="thisKey">
<cfif NOT ListFindNoCase(attributes.ignoreAttrs,thisKey) AND
Len(attributes[thisKey])>
<cfset urlInfo.args =
ListAppend(urlInfo.args,"#thisKey#=#attributes[thisKey]#","&amp;")>
</cfif>
</cfloop>

<!--- prepend with an & or an ? for the first element --->
<cfif len(urlInfo.args) and len(attributes.pageVariable)>
<cfset thisKey = attributes.pageVariable>
<cfset urlInfo.args = "?#thisKey#=" & attributes[thisKey] & "&" &
urlInfo.args>
<cfelseif len(urlInfo.args)>
<cfset urlInfo.args = "?#urlInfo.args#">
</cfif>

<cfset "caller.#attributes.returnVariable#" = urlInfo>

```

===================================================================
// end build_url_string.cfm
===================================================================

That file returns a nice struture of the current pages URL. I use both of
these prior files in the next, and final file, to generate and draw a nice
dynamic breadcrumb.

===================================================================
// dsp.breadcrumb.cfm
===================================================================

```cfc
<cfsilent>
<!--- dsp.breadcrumb.cfm - Copyright (c) 2005 SBCS, Inc. --->

<!---
Description:
I maintain and build a dynamic breadcrumb trail (showing each page a user has
visited).

NOTE: All URL and FORM variables should be moved into the Attribute scope
before calling this file.
there are plenty of existing examples of code available to accomplish this. By
convention we typically
call said method in our application.cfm file.


Parameters:
NONE; just must be included in the context of your site where the URL and FORM
scope are still
available. These variables will be in the attributes scope by now - but this
rule is important or
else you might lose many important attributes, unless you always passon
attributesCollection to each
level of your page/circuit.

Usage:
<cfinclude template="dsp.breadcrumb.cfm">

Revision History:
2/25/2005 wmrawlin this header block finally added after a complete rewrite.

\--->

<cfinclude template="functions.cfm">

<cfset breadCrumb = ArrayNew(1)>

<!--- this is the title of your sites root page. we need to know this
--->
<cfset homePageText = "ListBuilder Home">


<!--- we store the breadcrumb structure as a WDDX packet in the
client.breadcrumb variable --->
<cfif NOT isDefined("client.breadcrumb") OR NOT
isWddx(client.breadcrumb)>
<cfwddx action="cfml2wddx" input="#breadcrumb#"
output="client.breadcrumb">
</cfif>


<!--- at this point we need to grab the existing breadcrumb info into a
local variable --->
<cfwddx action="wddx2cfml" input="#client.breadcrumb#"
output="breadcrumb">


<!--- if we are at the root page of the site, reset the trail --->
<cfif attributes.page EQ homePageText>
<cfset breadCrumb = ArrayNew(1)>
</cfif>

<!--- i pass "password" in as an ignoreAttr to be on the safe side for
security concerns --->
<cf_build_url_string
attributeCollection ="#attributes#"
pageVariable ="page"
ignoreAttrs ="password"
returnVariable="urlInfo">




<!--- now determine if this linkText exists in the trail - if so we need
to trim the trail down to this point --->
<cfset thisPageEntryIndex = 0>

<cfloop from="1" to="#ArrayLen(breadCrumb)#" index="bi">
<cfif breadCrumb[bi].text EQ urlInfo.text>
<cfset thisPageEntryIndex = bi>
<cfbreak>
</cfif>
</cfloop>

<!---
this does exist in the list already, so start trimming - even though
I could have trimmed in the last loop, this seems cleaner and much
easier to read
\--->
<cfif thisPageEntryIndex>
<cfset breadCrumb = ArrayLeft(breadCrumb,thisPageEntryIndex)>
<cfelse>
<!--- new breadcrumb entry, add it to the array --->
<cfset ArrayAppend(breadCrumb,urlInfo)>
</cfif>

<!--- save our breadcrumb back to the client variable as a WDDX packet
--->
<cfwddx action="cfml2wddx" input="#breadcrumb#"
output="client.breadcrumb">
</cfsilent>


<!--- display the breadcrumb --->
<cfoutput>
<!---
display as an ordered list - because that is what it is in reality
I use some styles to hide the list "look" and make it run horizontally
across the page
\--->
<ol id="breadcrumb">
<cfset lastCrumb = ArrayLen(breadCrumb)>
<cfloop from="1" to="#lastCrumb#" index="bi">
<cfif bi EQ lastCrumb>
<li><span>#breadCrumb[bi].text#</span></li>
<cfelse>
<li><a href="#breadCrumb[bi].link##breadCrumb[bi].args#"
title="#breadCrumb[bi].text#">#breadCrumb[bi].text#</a>
></li>
</cfif>
</cfloop>
</ol>
<br class="clear" />
<h2 id="pagecaption">
#attributes.pagecaption#
</h2>
</cfoutput>

```

===================================================================
// end dsp.breadcrumb.cfm
===================================================================


As always, comments and critisism is welcome. If you want to use this code -
go for it. It is free to use under the GNU Public License. I have tested it
fairly well and it seems to work no matter how complicated of a page your
loading (ie 0 or 100 attributes required). I'd love to hear how others
approach the same issue.

## Comments

Noel Luneau

Hi Bill,

I'm interested in this this, but like Ken, I'm lost on the application of your
attributeCollection="#attributes#" and cfif attributes.page EQ homePageText.

Would you mind providing some examples from application.cfm and etc, on how
you set attributes.page and attributes.

I also use index.cfm?page=somePage&amp;someargument;=SomeValue.

Thank you,

Noel Luneau

Bill

attributeCollection is a way to pass in all of the attributes to a custom tag
in one structure (instead of passing each argument by name).

The attributes value I am passing in to attributeCollection contains all of
the form and url parameters that were needed for the current page to load.

Ken Gladden

OK, but i still don't understand what attributeCollection = "#attributes#" in
build_url_string needs to be.

Ken

Bill

page is my page variable (ie when I say
index.cfm?page=somePage&amp;someargument;=SomeValue)

I didn't think I had left any direct refrences to attributes.page in the code
I posted - but if I did you will want to update it to be whatever you call
your "page" argument.

I use a page argument because all of my pages actually are accessed via
index.cfm (as opposed to having a unique .cfm address for each part of the
site).

Hope that helps

Ken Gladden

Thanks for answering!
I'm still missing something. What do I put in my CF page? I thoguht I did a
cfinclude of dsp.breadcrumb.cfm but I get an error saying that "page" is not
defined in "attributes" which is this line in dsp.breadcrumb.cfm:

cfif attributes.page EQ homePageText

I thought after the include of dsp.breadcrumb.cfm I would then be able to set
urlInfo values.

TIA

ken@kibbage.com

Bill

i pretty much turn every form and url variable I need for the current page to
load properly into the attributes scope. Then I pass that structure in to the
build_url_string function. It builds the full url that will be used as the
hyperlink for the crumb in the trail.

Hope that helps.
Bill

Ken Gladden

This is exactly what I was loking for (can't believe it was posted over a year
ago). Thank you very much. However the 'build_url_string
attributeCollection="#attributes#"' doesn't appear to be documented. What
should this be.
I hope you are still on this blog!
