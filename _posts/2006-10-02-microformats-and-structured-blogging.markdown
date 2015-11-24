---
layout: post
title: "microformats and structured blogging"
date: 2006-10-02
comments: false
category: generall
tags: [microformat,hreview,structured-blogging,tails]
---
I've recently hopped on the [microformats](http://microformats.org/)
bandwagon. I think they have some great potential for helping push the web
toward a more semantic one and thus making the content on various pages much
more useful and usable. There are a variety of defined microformats for things
such as addresses, people, reviews, events, and even resumes.

In an effort to adopt microformats on [my personal
blog](http://rawlinson.us/blog/) I installed the wordpress plugin Structured
Blogging. It is a great idea but it is kind of poorly implemented.

For instance I wrote up a review of a movie yesterday and included some of the
metadata such as cast, year, website, imdb link, etc. When the plugin saved my
post it put all of the metadata at the beginning of the blog post and put the
actual review at the end. This seemed kind of backwards to me. I suppose I
could probably either rig together some CSS to flip flop them OR I could hack
the plugin (and make it non-forward compatiable); but neither of those options
are all the great.

First off the HTML created by the plugin is pretty awkward and this isn't even
due to the [hReview](http://microformats.org/wiki/hreview) (review
microformat) standard. In fact it turns out all of that fluff data has no
place in the hReview at all. Here is the actual standard:





hReview (hreview)

```
    * version. optional. text.

    * summary. optional. text.

    * item type. optional. product | business | event | person | place | website | url.

    * item info. required. fn (url || photo ) | hCard (for person or business) | hCalendar (for event)

    * reviewer. optional. hCard.

    * dtreviewed. optional. ISO8601 absolute date time.

    * rating. optional. fixed point integer [1.0-5.0], with optional alternate worst (default:1.0) and/or best (default:5.0), also fixed point integers, and explicit value.

    * description. optional. text with optional valid XHTML markup.

    * tags. optional. keywords or phrases, using rel-tag, each with optional rating.

    * permalink. optional, using rel-bookmark and rel-self.

    * license. optional, using rel-license.


```






Becuase of his strange output behavior (puts all this optional information after the basic standard stuff) I can't really recommend the structured blogging plugin; even though I really wanted to when I found it.  What follows is an hReview of the plugin itself:





 [

  Structured Blogging Wordpress Plugin](http://structuredblogging.org/)




    A wordpress plugin that aims to help people publish micorformatted content. However, due to the odd design choice that puts purely optiona/extended information after the meat of the actual content the user wishes to structure I can not recommened this plugin at this time.




 (1 out of 5)



Review by

  [Bill Rawlinson](http://rawlinson.us/blog),

  October 10, 2006








If you have a firefox plugin called [Tails](http://blog.codeeg.com/tails-firefox-extension-03/) (version 0.3.4+) installed it will discover this review and give you the ability to export it.  This works really well with other microformats such as addresses or events becuase you can easilly import them into your address books or calendars. If you don't use firefox there is a handy [bookmarklet](http://leftlogic.com/info/articles/microformats_bookmarklet) that pulls out addresses and events as well.



  *[1]: 1
  *[October 10, 2006]: 20061002
