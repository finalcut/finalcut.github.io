---
firstprop: first
layout: post-with-discussion
title: Distance Between Two Latitude + Longitude Points - PHP
date: 2009-02-09
comments: false
category: development
tags:
  - php
  - algorithims
description: A simple php method for computing the distance between two points on a map using their latitude/longitude values.
blueskyPostURL: https://bsky.app/profile/rawlinson.us/post/3m5f6rnbhni2j
---
Years ago I had a project where the client wanted customers to be able to search
for the nearest vendor to the customers zip code - this project was in PHP but
the algorithm contained here can be translated to other languages pretty
easily (Note, this returns the value in miles):


```php
function computeDistance($lat1,$lon1,$lat2,$lon2){
  $lat1 =  deg2rad($lat1);
  $lon1 =  deg2rad($lon1);
  $lat2 =  deg2rad($lat2);
  $lon2 =  deg2rad($lon2);

  // Find the deltas
  $delta_lat = $lat2 - $lat1;
  $delta_lon = $lon2 - $lon1;

  // radius of earth in miles
  $r = 3963.1;

  // Find the Great Circle distance
  $distance = pow(sin($delta_lat/2.0),2) + cos($lat1) * cos($lat2) * pow(sin($delta_lon/2.0),2);
  $distance = $r * 2 * atan2(sqrt($distance),sqrt(1-$distance));

  return $distance;
}
```







## Comment Archive

<blockquote>
 I'll tell you the same thing i told kinky ben, use a bounding box instead.
 Paul Hastings
</blockquote>
---
That is probably a good suggestion however in my case I don't know if is any more efficient.
I'll have to experiment.

There are only about 10 global distributors and I don't have a zipcode db to compute against. I have the coordinates of the warehouses and then a random zipcode.  I then have to find the warehouse nearest the zipcode

- Bill
