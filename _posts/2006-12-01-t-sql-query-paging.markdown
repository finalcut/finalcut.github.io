---
layout: post
title: "T-SQL Query Paging"
date: 2006-12-01
comments: false
categories:
 - sql
 - t-sql
---
Here is a tip to help you get pages of results back from SQL Server. For
instance, let's say you were trying to display a listing of products with 20
products per page (and you have a couple hundred products).  
  
On option (since this is a CF Blog) is to use the cfoutput startrow attribute.
However, that solution isn't always viable because the size of your dataset
may be too large. Instead, what you need is to just pull the correct 20
results back from the table. Sadly, there isn't an "OFFSET" function in T-SQL
so we need to rephrase the problem a little in order to figure out the
solution.  
  
For example, let's say we want the first page, so the top 20 results. That is
pretty easy, just use SELECT TOP 20 .... but what about the second or
subsequent pages? How do you get the 21-40 items? It's easier than you might
suspect. What you are actually trying to get is the bottom y of the top x
results. To look at that another way you want the top y of the top x results
ordered backwards.  
  

    
    
      
    SELECT * FROM (  
          SELECT TOP y * FROM (  
               SELECT TOP x * FROM sometable  
               ORDER BY somefield ASC  
          )  
          ORDER BY somefield DESC)  
    ORDER BY somefield  
    ```
      
      
    The innermost query, SELECT TOP x, grabs the first x number of rows, the second query SELECT TOP y, gets the last y of x rows, and the outermost query, SELECT * puts the results in the right order.  
      
    However, there is a caveat here, and is only a problem when you get to the last page of results.  To keep the example simple lets say there are 26 products.  If you use this technique as described your second page will show 14 of the products that were on the first page.    
      
    We need some new variables.    
    Let   
    y1 = max number of items to show on a page (20)  
    y2 = actual number of items to show on this page (calculated later)  
    p  = page number (2)  
    x  = subset of items we are getting the bottom y2 of = (y1*p) or (20*2)  
    t  = total number of items (26)  
      
    We need to figure out a way to calculate y2 when p > 1.  y2=y1-x-t  
    ```js  
             if(p==1){  
                y2=y1;  
             } else {  
                y2=y1-x-t  
             }  
    ```
      
    Lets replace those variables with values and see how it works out; starting with page   
    2.   
      
    ```js  
             if(p==1){  
                y2=20;  
             } else {  
                y2=20-(20*2)-26;  
             }  
    ```
      
      
    As you can see on page 2 y2 = 20 -(40-26) = 20-14 = 6 which is exactly what we want to show on page 2.
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    tracker1
    
    
    
    
    
    Here's my post on this.. [Paged Results in T-SQL](http://frugalcoder.us/post/2010/02/23/tsql-paged-result-sproc.aspx).  It's a bit more complicated, but works *very* fast.
    
    
    
    
    
    
    
    
    
    
    corey
    
    
    
    
    
    there is one small problem. your formula works for 1 or 2 pages, but beyond that it will fail.  
      
    you need one small change. in the first IF statement, instead of  
    if p==1  
      
    should be  
      
    if p==1 or x <= t  
      
    this will work for pages beyond 1 and 2
    
    
    
    
    
    
    
    
    
    
    Hrvoje
    
    
    
    
    
    Nice article, but I think you have an error in the formula.  
    Now:  
             if(p==1){  
                y2=y1;  
             } else {  
                y2=y1-x-t  
             }  
    But it should be:  
             if(p==1){  
                y2=y1;  
             } else {  
                y2=y1-(x-t)  
             }  
      
    Later, when you change variables with real numbers, your formula is still wrong:  
             if(p==1){  
                y2=20;  
             } else {  
                y2=20-(20*2)-26;  
             }  
    It should be:  
             if(p==1){  
                y2=20;  
             } else {  
                y2=20-((20*2)-26);  
             }  
      
    In the end, your result is OK:  
    y2 = 20 -(40-26)  
      
    So I assume that you were calculating formula in the right manner, but you just typed it down wrongly.  
      
    Cheers
    
    
    
    
    
    
    
    
    
    
    Bill
    
    
    
    
    
    Perhaps he missed the subject line of the post, T-SQL Query Paging.
    
    
    
    
    
    
    
    
    
    
    Anonymous
    
    
    
    
    
    'cause T-SQL has no LIMIT clause, only TOP. What a pity!
    
    
    
    
    
    
    
    
    
    
    Anonymous
    
    
    
    
    
    Uhh... why not just use  
    LIMIT start,num  
    ?
    
    
    
    
    
    
    
    
    

