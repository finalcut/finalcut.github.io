---
layout: post
title: "SQL SERVER CE - Change a Column Name"
date: 2008-08-01
comments: false
categories:
 - sql
 - sql server ce
 - column renaming
---
Lets say you have a column that is currently storing just integers but you
really want it to store nvarchars in SQL Server CE - what do you do?  
  
Well, you can't just modify the column definition (it seems, though I could be
wrong). Instead you have to alter the table to create the new column, copy the
data over from the int column to the nvarchar column, drop the int column,
recreate it as a nvarchar column, copy the data back, and then delete the temp
column you started with. Something like this:  
  

    
    
    alter table myTable add tempCol nvarchar(10);  
    update myTable set tempCol = myIDcol;  
    alter table myTable drop column myIDcol;  
    alter table myTable add myIDcol nvarchar(10);  
    update myTable set myIDcol = tempCol;  
    alter table myTable drop column tempCol;  
    ```
      
      
      
    Fun isn't it?  If there is a better way to do this in SQL Server CE please share!  Thanks.
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    Anonymous
    
    
    
    
    
    Last line should be --  
    alter table myTable drop column tempCol;
    
    
    
    
    
    
    
    
    
    
    Yoo-sang
    
    
    
    
    
    it's best(just) way.
    
    
    
    
    
    
    
    
    

