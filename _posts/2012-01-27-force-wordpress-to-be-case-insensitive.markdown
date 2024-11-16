---
layout: post
title: "Force Wordpress to be Case-Insensitive"
date: 2012-01-27
comments: false
---
We recently had a minor annoyance happen when some marketing material was sent
out that had a url with a capital "B" in it; such as
http://www.mysite.com/Bill instead of http://www.mysite.com/bill.  Our
webserver runs IIS so it is case-insensitive but wordpress, which is being
used to host the hypothetical "bill" website is written in PHP which is case
sensitive.

Fortunately it is fairly easy to change this default behavior without using
URL rewrite rules (which are limited to suckness on IIS 6 anyway).  Wordpress
Plugins to the rescue!

Our wordpress install uses a multi-site setup with over 150 sites so clearly
this is a plugin you'd want to network activate.  Sadly, for some reason,
network activate didn't do the trick. Instead the plugin had to go in the mu-
plugins directory (mu-plugins = must use plugins; they are forced onto every
site and loaded before anything else basically).

I found the perfect plugin code over at [unfocus.com's
website](http://www.unfocus.com/2007/08/31/case-insensitive-permalinks-plugin-
for-wordpress/) but I renamed it to something that made a little more sense
for us (from a maintenance perspective) in the future. Here is the code of the
plugin in case that site goes away someday.





```php
 <?php

  /*

  Plugin Name: case-insensitive-url

  Plugin URI: http://www.unfocus.com/projects/

  Description: A plugin to make wordpress case insensitive in regards to urls.

  Version: 1.0a

  Author: Kevin Newman

  Author URI: http://www.unfocus.com/projects/

  */

  function case_insensitive_url() {

   if (preg_match('/[A-Z]/', $_SERVER['REQUEST_URI'])) {

    $_SERVER['REQUEST_URI'] = strtolower($_SERVER['REQUEST_URI']);

    $_SERVER['PATH_INFO']   = strtolower($_SERVER['PATH_INFO']);

   }

  }

  add_action('init', 'case_insensitive_url');

 ?>


```



That's it.  This now runs automatically at the beginning of every page load and insures that each request is handled in a case-insensitive manner.  I'm not sure what, if any real, performance impact this has, but it is worth the cost for the reliability of knowing all incoming urls are treated the same regardless of case.  It's too expensive in terms of reputation and marketing dollars to have pamphlets, postcards, and flyers printed that point to a 404 error if we don't do it.





## Comments











arudd






LIFE SAVER!










