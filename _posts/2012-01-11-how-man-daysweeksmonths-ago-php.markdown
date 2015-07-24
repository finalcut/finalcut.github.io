---
layout: post
title: "How many Days|Weeks|Months Ago? [php]"
date: 2012-01-11
comments: false
categories:
 - php
---
Yesterday I wrote a simple wordpress plugin that checks an rss feed and finds
posts in that feed that contain specific keywords.  Any posts found that are
also younger than n number of days are then displayed at the top of a page
just as if they were posts in the wordpress blog.

  

When I was display the data though I thought it would be nice if the pubdate
sent with the feed actually showed up as "2 days ago..." or "4 months ago.."
or whatever was applicable.  Thus, I did what any good lazy coder does I
googled to see if anyone had written this up in PHP already and sure enough
someone had.

  

I found this function on the [drupal support community message boards posted
by someone named "drenei"](http://drupal.org/node/61565#comment-198230)

    
    
      
       <?php  
       function ago($timestamp){  
       $difference = time() - $timestamp;  
       $periods = array("second", "minute", "hour", "day", "week", "month", "years", "decade");  
       $lengths = array("60","60","24","7","4.35","12","10");  
       for($j = 0; $difference >= $lengths[$j]; $j++)  
       $difference /= $lengths[$j];  
       $difference = round($difference);  
       if($difference != 1) $periods[$j].= "s";  
       $text = "$difference $periods[$j] ago";  
       return $text;  
      }  
       ?>  
    ```
    
    
    
    

