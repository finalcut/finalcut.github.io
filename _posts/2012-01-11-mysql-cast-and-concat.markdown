---
layout: post
title: "MySQL CAST and CONCAT"
date: 2012-01-11
comments: false
categories:
 - sql
 - mysql
---
CAST  
This is just here to help me remember. In MySQL if you want to CAST an int
into a string you use:  
  

    
    
    CAST(x AS CHAR)```
    I had assumed it would be VARCHAR but I was wrong.  As a further [reference here is info on all of the TYPES supported by MySQL](http://dev.mysql.com/doc/refman/5.0/en/data-type-overview.html).  What I find interesting is the fact that MySQL does have a VARCHAR type but you can't cast an int to it.  Why Not?  In the end it doesn't matter too much; the CHAR option worked.    
      
     CONCAT  
      
    A similarly odd behavior is how you concatenate strings in MySQL.  I had thought I would use & or || but  both of those return a 0 if you use them to concatenate.  Instead you have to wrap all of the strings you want to concatenate up into a call to the CONCAT function like so:  
      
      
    
    
    
    CONCAT('http://www.rawlinson.us/blog', page_name, '/datafiles/?file_id', CAST(file_id AS VARCHAR)) as url```
    
    
    
    

