---
layout: post
title: "PHP array_map in practice"
date: 2012-02-29
comments: false
categories:
 - map
 - smart-quotes
 - array_map
 - php
---


Last week I spent some time making sure I understood how map and reduce actually work and what their purposes are. This week I needed to use map while fixing a silly problem. Some of this background info will be pure cruft to most of you but hopefully it will be enlightening in it's own way.

There is an application somewhere in our organization that utilizes an access database to store a catalog of information. This catalog is then made available for consumption within our web properties via a webservice that is written in php and which returns the data contained within the database in either json or xml format.

Here is the basic way the json was being generated previously:

```php

  $rs=odbc_exec($conn,$sql);
  //declare an array to hold the query results
  $data = array();

  //populate the jobs array with the query result set
  while($curRow = odbc_fetch_array($rs)){
    $data[] = $curRow;
  }
  echo json_encode(array('jobs'=>$jobs));

```

Very straight forward and, it appeared to work well until today.  Someone copied and pasted a descriptive field of one of the catalog items from a word document into the access database and a single smart quote (apostrophe really) worked its way into the data.  When this happened that field was rendered in the json as null even though there was clearly data contained within.
It took me a little while to see that it was a smart quote buried in the middle of the paragraph of text but once I did I knew right away how to clean it out - using MAP; or in php paralance, array_map.  Combined with this nice function to <a href="http://shiflett.org/blog/2005/oct/convert-smart-quotes-with-php">convert smart quotes</a> I had a winning solution on my hand without having to add much code at all.  Here is the final version of that same code:


```php

  $rs=odbc_exec($conn,$sql);

  //declare an array to hold the query results
  $data = array();

  //populate the jobs array with the query result set
  while($curRow = odbc_fetch_array($rs)){
    $data[] = array_map("convert_smart_quotes",$curRow);
  }

  echo json_encode(array('jobs'=>$jobs));

```

Just updating that one line in the middle of my while loop let me make sure that every element in every row was clean of nasty smart quotes by telling array_map to call the convert_smart_quotes function on each element.  I have to say I really do like the power and simplicity of map (and reduce).

<h2>Comments</h2>
<div class='comments'>
<div class='comment'>
<div class='author'>Bill Rawlinson</div>
<div class='content'>
anonymous:

I actually ran into a situation sort of like yours today:

since your $curRow is already an array do this:

$data = arary_map("convert_smart_quotes", $curRow);

Then you can output the $data["sae"];  etc. etc.</div>
</div>
<div class='comment'>
<div class='author'>Bill Rawlinson</div>
<div class='content'>
I'm pretty sure this is because my query is just returning one column while yours is returning many; thus my $curRow is a single dimension array while yours is a multi-dimensional array.

I think you would have to just do $data[] = $curRow; in the loop..

You have to do a map on the second dimension of the array.. It's a little more complicated.</div>
</div>
<div class='comment'>
<div class='author'>Anonymous</div>
<div class='content'>

<pre>
  $rs=odbc_exec($con,$sql);

  //declare an array to hold the query results
  $data = array();

  //populate the jobs array with the query result set
  while($curRow = odbc_fetch_array($rs)){
   $data[] = array_map("convert_smart_quotes",$curRow);
  }
  echo json_encode(array(
  "sae" => $data["sae"],
  "bara" => $data["bara"],
  "ghobdg" => $data["ghobdg"],
  "ghobks" => $data["ghobks"],
  "ghocrb" => $data["ghocrb"])
  );

  it doesn't work, help me
</pre>

  </div>
</div>
</div>
