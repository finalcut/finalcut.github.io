---
layout: post
title: "HTML IDs are Anchors"
date: 2007-05-01
comments: false
category: programming
tags: [html,anchor,semantic]
---
It is said you learn something new everyday. Sure enough, today is one of
those days for me. An id is the same thing as an anchor within a webpage. "So
what?" you might be saying. The only way I can answer is to provide an
example.

Let's imagine you were creating a webpage and you wanted to provide someone
with a link to a specific portion of that webpage. Typically you might add an
anchor tag <a name="someanchor" /> to the page and then use the url:
http://somedomain.com/somepage.html#someanchor. No problem right? Well,
actually there is a little problem from a purely semantic perspective. The
anchor is probably latched onto nothing at all, or, as Tantek Celik puts it,
you have an [Anorexic
Anchor](http://tantek.com/log/2002/11.html#L20021128t1352).

The anchor really should be wrapped around the content you are trying to
anchor but you probably don't want to wrap an entire paragraph (or collection
of paragraphs) in an anchor tag. Instead you can just wrap the content in a
div and give the div an ID value (remember, IDs are unique on the page). So
instead of our earlier anchor we would now have:




```html
<div id="someanchor">

 <p>

  some content

 </p>

</div>


```




The same url will still work even though there isn't an anchor there.  The ID serves as an anchor and your favorite browser will still navigate to the correct page and set the focus to the correct part of the page.  So ban those Anorexic Anchors and get in bed with Fat Anchors that actually do what they are supposed to!





## Comments











Anonymous






Just found this out after 15 minutes of: "I don't get it, there's no anchor named that on the page!"

thanks!











Officer Leeroy






this saved me a lot of time, thanks for posting this.











Bill






actually that number is the name of an anchor element inside the div.


You can use an anchor tag without specifying an href.  That is the only way I had known how to link to content in a page before I discoved this "id" technique.











Dov






Apparently, the name attribute works as well. Try:


[

http://cf-bill.blogspot.com/2007_05_01_archive.html#5429223066276640284

](http://cf-bill.blogspot.com/2007_05_01_archive.html#5429223066276640284)


where that number is that value of the name attribute of the div containing this initial blog post.











Dov






Apparently, the name attribute works as well. Try:


[

http://cf-bill.blogspot.com/2007_05_01_archive.html#5429223066276640284

](http://cf-bill.blogspot.com/2007_05_01_archive.html#5429223066276640284)


where that number is that value of the name attribute of the div containing this initial blog post.











Todd Sharp






I only recently learned this myself and was as surprised as you seem to be.  Nice post.











mostly






Interesting, even when you think you are a DOM wiz :) and it even works in IE6. A small note though, the URL should be absolute. E.G. http://lunarmedia.dev/#navigation doesnt work but http://lunarmedia.dev/default.aspx#navigation does :)











Bill






barry, good question - I will have to run a quick test tomorrow to find out.











barry.b






I wonder how far this can be pushed?


eg: whether you can use the id of a form control as an anchor, so when the user clicks on it it not only goes to the correct page section but gives focus to a particular form control? saves messing around with JS if they're coming from outside the page











Ben Nadel






Awesome. I just learned something new also :) Thanks for putting that up, this will be ultra useful.
