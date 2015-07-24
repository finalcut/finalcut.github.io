---
layout: post
title: "Model Glue : Waist Deep"
date: 2005-11-09
comments: false
categories:
 - coldfusion
 - model-glue
 - oracle
---
I'm sure there is a lot to Model Glue I haven't touched yet. For instance I
haven't even looked at the Coldspring tie in with MG. I also haven't done any
IOC (dependency injection stuff) using ChiliBeans within MG. However, I have
been mucking with ConfigBeans.  
  
To be honest, at first, I thought they seemed like overkill. But like all
short-sighted people thinks quickly got blurry for me until I put on my
ConfigBean glasses and could see clearly. Quite frankly they are handy.  
  
Here's a for instance. I built an app not too long ago that let other
developers add page specific menu items to their view. So if you were on the
login page you could define a structure that contained all the info needed for
that link (text, caption, javascript to run on the click event, whether it was
a "admin" or "user" link, if you had to be logged in to see it, etc.. etc.)
you then passed this structure into a custom tag that stored the struct in an
array in the request scope. Then, when the page_menu view was loaded the array
was iterated over and the links added to the menu. It worked pretty well and I
was able to use a similar technique to let each page developer add context
sensitive "tips" to the application, and various filtering mechanisms to
different query views in a consistent manner.  
  
So, buy now you must be wondering why I'm droning on about this request scope
stuff when I started talking about ConfigBeans. Well in my dig into Model Glue
I decided to port this application as a good "indepth" exploration of the
framework. In doing this port I want to get away from using the Request Scope
unless absolutely necessary (I might post later on when it is necessary).
These page specific menu's are an ideal candidate for moving from the request
scope into a ConfigBean.  
  
Now, there are two options to making this move; I could make one ConfigBean
that stores all the page menu options for all the pages. Or I could create one
ConfigBean for each page that has custom menu items.  
  
In this initial dig into the idea I am using the first option. One big
ConfigBean that consists of a structure (each key is a page) and each
structure consists of an array of menu item structures. You'll notice the
array of menu item structures is the same. I basically didn't have to do any
work at all in converting my view in ModelGlue because of this.  
  
Now, on the onRequestStart event I load into the event data the pages menu
items. Then at the top of the page menu view instead of assigning my local
menuItems variable the contents of Request.Page.Menus I just assign it to
viewState.getValue("pageMenu")  
  
OK, admittedly, this example is pretty specific to my application so here is
another instantly useful example that you might find applicable.  
  
In the documentation about ConfigBeans Joe mentions they are a great candidate
for storing datasource information - then you pass in the datasource bean to
your DAO instead of the datasource name etc. This way it's all encapsulated.  
  
Well, with this same app I actually have to have two datasources defined. The
primary datasource (an Oracle 9i database) and an import datasource (an access
database). The import database just points to a totally empty place holder
access mdb file. But with CFMX 6+ the only way to dynamically connect to an
access database is to have this placeholder one in existence.  
```cfm  
<cfquery name="manuals" datasource="placeholderAccessDatabase">  
SELECT * FROM sometable IN 'full path to the actual access database to read
from'  
</cfquery>  
```  
  
Again I have two choices; one datasource ConfigBean with info about both
datasources (getDSN and getImportDSN) or two ConfigBeans - one for each. Again
I chose the former and just have one Datasource ConfigBean. In this example it
just makes sense to me to have one bean for all DS information especially
since my importation actions all need to get the data from the access
database, muck with it, then stick the transformed data into the oracle
database.  
  
Ok, so that one still isn't applicable? Well how about if you're using MG and
you have one primary layout view that takes the content you build in your
subviews and then sticks said content into its appropriate place in the main
template. How do you give each page a unique title within the html 'title'
tag? Well, I have a PageInformation ConfigBean that holds some general info
about the page.  
  
This particular application has a variety of entry points for the many
different organizations that use it. You can go down different branches within
it based merely on your entry point and based on the place you are at in the
application it needs to show the primary organizations "look/feel". So in my
PageInformation ConfigBean I not only store the page's title but also what
organization(s) is the owner of the page. (plus those page menus I mentioned
earlier also show some organization specific menu items depending on the
organization (or section) the page belongs too).  
  
So now I can quickly grab the organizations code and use it to load the
appropriate CSS for that page. I can also use it to load the correct page menu
items. And I can use that pages information to show a unique title for each
page that has a title defined in the ConfigBean.  
  
Admittedly, some of this stuff could have been stored in the database. But
there are a couple caveats to my ability to do things to the database. First a
specific customer owns the database and they have six or seven apps that use
it. Adding new tables to the schema isn't a very easy task (must go through a
committee to get each table approved and they only do review sessions twice a
year). Plus, I have tried to keep my apps specific data out of their way and
have left the database purely for storage of business related data. Because of
this the ConfigBeans work out really well.  
  
Whew, sorry I droned on :O) hopefully I haven't scared you away from my
craziness and instead have illustrated some of the potential of ConfigBeans
with ModelGlue.

