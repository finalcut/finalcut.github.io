---
layout: post
title: "Weighted Arrays in ColdFusion"
date: 2008-04-10
comments: false
categories:
 - coldfusion
 - weighted arrays
 - random
 - php
 - cf
---
I stumbled across [a blog today that takes a more mathematical
look](http://20bits.com/) at most problems than I do (and I really like math).
The problem he was looking at dealt specifically with [randomly selecting
items from a weighted array](http://20bits.com/2008/02/07/random-weighted-
elements-in-php/).  
  
A weighted array is basically an array where any item in it has a predefined %
chance of being selected if you randomly select an object from it. A standard
array full of distinct items is evenly weighted. However, let's say you have a
10 item array where 8 of the items are "dog" and 2 are "cat" then you have a
20% chance of randomly picking "cat" and an 80% chance of picking "dog".
Obviously though it is pretty ineffecient to have an array with a bunch of
duplicated items in it.  
  
In PHP you can create an array that is weighted so that you only list each
object one time along with an accompanying percent weight for each objects
chance of being selected:  
  

    
    
      
     $weights = array(  
      "one" => 0.09,   
      "two" => 0.11,   
      "pie" => 0.05,   
      "fish" => 0.15,   
      "dog" => 0.30,   
      "oink" => 0.25,   
      "foo" => 0.05);  
    ```
      
      
    In ColdFusion however there are no such things as indexed arrays (at least by that name) so we have to use a Struct to emulate this (using CFSCRIPT):  
      
    ```cfm  
     weights = StructNew();  
     weights["one"] = .09;  
     weights["two"] = .11;  
     weights["pie"] = .05;  
     weights["fish"] = .15;  
     weights["dog"] = .3;  
     weights["oink"] = .25;  
     weights["foo"] = .05;  
    ```
      
      
    Basically, what I have done from here on out is just a syntactic translation of the PHP code provided at the aforementioned link into a ColdFusion interpretation.  I can't really claim any credit for anything presented here.  
      
    The core of the solution is found in this function which basically returns a random key from the provided structure - where the randomness is affected by the keys predefined weight:  
    ```cfm  
    <cffunction name="w_rand" returntype="string">  
     <cfargument name="weights" type="struct">  
      
     <cfset var r = RandRange(1,1000) />  
     <cfset var offset = 0 />  
     <cfset var k = 0 />  
      
     <cfscript>  
      for(k in arguments.weights){  
       offset = offset + arguments.weights[k] * 1000;  
       if(r LTE offset){  
        return k;  
       }  
      }  
     </cfscript>  
      
    </cffunction>  
    ```
      
      
      
    However, What I can say is that PHP is much, much faster and dealing with this in really large chunks.  For instance let's say you are iterating over the struct 200,000 times.  Each iteration in PHP takes apx 0.008ms while in CF it takes 0.028ms - over 3x slower!  Ouch.  
      
    I'm not bringing this up to knock CF - I love CF; particularly when it comes to dealing with databases.  However, it does serve as a good reminder that each language available to you has it's own strengths and advantages; never discount one language simply becuase it isn't good at everything - pick the right language for the task at hand.  
      
    Finally, just as a little bonus - becuase I wanted to mess with Ruby a little here is the same function in ruby.  By the way, the Ruby performance is comparable PHPs at apx 0.008ms per iteration:  
      
    
    
    
      
    def w_rand(weight)  
     r = 1 + rand(10000)  
     offset = 0  
      
     weight.each { |k, w|  
      offset += (w * 10000)  
      if(r <= offset)  
       return k  
      end  
     }  
    end  
    ```
      
      
    It would be nice, really, if I had a good way to share the full source of each file.  I'm not really sure how best to share the full demo file here on blogger.  If I come up with a solution to it (that doesn't involve me hosting the files elsewhere) I'll update this post.
    
    
    

