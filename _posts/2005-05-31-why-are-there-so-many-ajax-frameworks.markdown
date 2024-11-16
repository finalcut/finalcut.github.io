---
layout: post
title: "Why are there so many AJAX frameworks"
date: 2005-05-31
comments: false
category: coldfusion
tags: [ajax,xmlHttpRequest,sack]
---
At MXNA I keep seeing posts about different AJAX frameworks. One for
Coldfusion, one for ASP, one for PHP, another that has "backends" for a bunch
of languages. I honestly don't get it.

Until last week I had my own little homegrown javascript object that would
take care of creating the xmlHttpRequest object and then I could do what I
wanted with it.

Then last week I was shown SACK which was very similar to what I was doing -
but honestly, it was better written, so now I'm using it. But it doesn't have
any language specific backends. And for the life of me I can't understand why
it would need a language specific backend.

Maybe I'm missing something.

Here is how I understand things. The xmlHttpRequest object has four states; 1
which is loading, 2 loaded, 3 interactive, and 4 completed. 3 (interactive)
doesn't tell you much except that it is actually downloading data. 4, to me,
is where the magic happens because I have my remote data. I can access it via
the responseXML or responseText properties of my xmlHttpRequest instance.

Typically I am passing around XML so I'm more concerned with the responseXML
property. When I first instantiate the xmlHttpRequest object I assign a
javascript function to run during state 4 (completed). My function has access
to the responseXML which I can parse, loop over, or do whatever I need to with
it.

To generate the XML on the backend I don't need some AJAX backend library
bloating me down. For instance using Coldfusion my xmlHttpRequest object will
post back to a different CF file that contains the logic necessary to get some
data and create an XML structure.


```cfc
<cfprocessingdirective suppresswhitespace="yes"><cfsilent>

<CFPARAM Name="url.someID" Type="Numeric">


<cf_users_get
someID ="#url.someID#"
returnvariable = "users">

</cfsilent><cfcontent type="text/xml"><site.xml>
<CFIF users.RecordCount>
<CFOUTPUT Query="users">
<element_id>#users.userID#</element_id>
<element_value>#XMLFormat(users.userName)#</element_value>
</CFOUTPUT>
<CFELSE>
<element_id>0</element_id>
<element_value>No Users Available</element_value>
</CFIF>
</site.xml></cfprocessingdirective>

```


There is nothing super fancy going on here. I just call some query that gets
some data and then I output the query data into XML. Why do I need an AJAX
backend?

I know some people read this blog so if you know of a reason why I would need
a backend (for some other example perhaps) then please let me know. Because,
honestly, all of the libraries I see popping up seem unnecessarilly
complicated for a process this is generally pretty simple.

## Comments

Bill

Thanks for your comment Guy. I can see your point, particularly if you are
working with a development team where a consistent API could mean the
difference between project success and failure.

Guy Peled

You are looking on it from a very narrow usage. If you retrieving data from
the server and that is what you need that you do not need any AJAX framework.
When AJAX frameworks come handy is when you need a sophisticated and
responsive UI. Web technology in general is to generic and AJAX frameworks
give you bigger building blocks that are more specific for your development
scenario.

The server side of an AJAX framework in my view is almost as important as the
client side and in some cases even more important. JavaScript development is
quite complex to manage and to produce a stable out come. You can see google
going to GWT and Microsoft with Script# which are both generation of
JavaScript from compiled code. Here comes the great benefit of a good server
side support as it reduces the amount of client side script you have to write.
For example when you want to update a part of a screen in Atlas you simply
update a panel and the framework knows how to send the data to the client and
interact with a built in JavaScript framework that will update the screen.

I for one am an architect of an even more total framework
(http://www.visualwebgui.com) that hides from you all the web plumbing and
technologies and lets you develop web like you develop WinForms. It is an AJAX
solution for IT applications but here you can see all the goals I talked about
taken to the extreme.

To make things short there a definitely to much frameworks and here I would
add "doing the same thing" but as a farmer once said it is a good time to grow
tomatoes. Well it seems like a good time to grow an AJAX framework.

Bill

I think coining the term AJAX is good because it makes discussions about that
technique easier.

I also think by having it known as a more mainstream technique that more cool
applications of the technique will be found.

However, I don't know that ALL of the different frameworks are that necessary.
In fact, many seem incredibly redundant. I use SACK mostly because, as it's
name (Simple Ajax Code Kit) suggests - it's simple.

I can understand some of the bigger ones that also have a built in library of
effects.

However, having a ton of simple ones, and a ton of complex ones, just seems
like overkill to me.

Finally, I don't see why each server side development platform needs it's own
framework for AJAX. Your server has to return structured data (xml or json
most likely) so just return it. The AJAX interface to your API shouldn't need
to be any different than the older legacy interface.

Anonymous

Yeah Bill, I have the SAME EXACT QUESTION...I am a php coder and have been
building out AJAX-esque web applications for several years now. AJAX
functionality is nothing new and am wondering what all the fuss is about.
Additional libraries for AJAX seems completely unecessary - is the development
community just trying to come up with new acronyms?

Anonymous

Yeah Bill, I have the SAME EXACT QUESTION...I am a php coder and have been
building out AJAX-esque web applications for several years now. AJAX
functionality is nothing new and am wondering what all the fuss is about.
Additional libraries for AJAX seems completely unecessary - is the development
community just trying to come up with new acronyms?

Bill

Sack can be found at:
http://twilightuniverse.com/2005/05/sack-of-ajax/

Anonymous

Is there a URL for SACK?

Bill

Im really more focusing on things like SAJAX, CFAJAX (coldfusion), TOXIC
(php), XAJAX (php), AJAX.net (.net), DOJO

They just don't make sense to me. I'm hoping someone can tell me WHY we need
all these language specific implementations - what purpose do they actually
server? Why would someone want to use them over a generic solution that
doesn't require a language based backend (such as SACK)?

Anonymous

to use backbase client, you don't need
any backend software.
However, we have java and .net servers, which enables you to easy do
databindings, xml transformations(xml-xslt pipelines etc.),e.g.:
http://www.theserverside.com/articles/article.tss?l=BestBothWorlds
m.j.milicevic

Bill

Yep, Ive seen backbase before and it's pretty well done as far as I can tell.

However, I still dont see why these language specific packages are needed.

AJAX - asynchronous javascript and xml. So to me any language that can spit
back plain text or XML can can be used without special backends.

I know I must be missing something. But it seems to me these backend libraries
are just added weight that isn't really needed.

Anonymous

well,I agree there are many libraries around, many of them made as yours for a
certain need, other ones do some backand integration/processing before result
is returned.
I work at backbase, and we also made an ajax library, but, it's different than
anything out there.
check backbase.com site to see what I mean.

cu,
m.j.milicevic
