---
layout: post
title: "Dynamic Breadcrumb CFC"
date: 2005-02-28
comments: false
---
Last week I posted about a procedural way of maintaining a dynamic breadcrumb
trail on your site. It had to be done that way so it could support CF 5.
However, for the future I think it would be better to have a component that
takes care of this - and thus makes it far more reusable. In that vein I have
built the first version of breadcrumb.cfc  
  
When I posted about the procedural method I put a whole bunch of code up. I'm
not going to do that this time. Instead, I have actually assembled a sample
application that you can download and try out yourself. There is a README.txt
file - please read it. All you should have to do is update the applicaiton.cfm
file to point to a valid client storage dsn and the sample app will work.  
  
Anway [here is the sample
app](http://blog.rawlinson.us/sourcecode/breadcrumb.zip). All of the code is
available under the [GNU public
license](http://www.gnu.org/copyleft/gpl.html).

## Comments

Bill

You can find it hosted on GitHub at:
https://github.com/finalcut/ColdBreadCrumbs.. I think I refactored it a little
when I put it on there but I don't really remember.  
  
I know the code works, it's still in use in a project.

Anonymous

Bill,  
Is this still available anywhere?  
I'd love to take a look at it.

Bill

I'd suggest not using this. You should probably roll your own since you have a
clearly defined structure to your site that is stored in the db.  
  
This is for sites whose structure is not in a database.  
  
Since yours is you can do a few things.  
  
1\. When the applicaiton is first loaded, load the site map in memory (a CF
structure would work well) then use it to get the page's heirarcy when a page
is loaded and show the trail. This has the advantage that the DB won't be hit
each time a page is loaded just to get the heirarchy - especially considering
the site won't change alot. When it does you save the page and update the in
memory structure so that new pages are automatically accounted for.  
  
2\. Or you can load the pages breadcrumb on each page load by querying the DB.  
  
3\. Or you can choose a hybrid approach. On page load check your sitemap
structure to see if the current page has been visited yet. If so then grab the
data from the structure. If not then load the trail from the DB and display it
and store it in the sitemap structure so it is availble on next page load.

Anonymous

This is nice, thanks for making it available!  
I'd like to use it to show where I am in the site as opposed to where I have
been.  
My site is a database CMS with typical parent/child sections, then an article
or a product can be drilled down to and displayed.  
What suggestions do you have.

