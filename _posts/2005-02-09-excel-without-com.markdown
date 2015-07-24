---
layout: post
title: "Excel Without COM"
date: 2005-02-09
comments: false
---
For a couple of minutes today I was in a situation where I might have to
support uploading and processing Microsoft Excel files without having access
to the COM component. One option is to create a Datasource in the CF
administrator - but that isn't very flexible since I need to be able to upload
many, many files and each might be named different etc.  
  
So, I started searching for an alternate and found the customtag [cfx_excel2qu
ery](http://www.emerle.net/programming/display.cfm/t/cfx_excel2query). Using
java it loads your excel file into a CF query object. It has a couple of
parameters including use the first row as header information (very useful to
me). The tag hasn't been updated since february of last year but it is
documented to work with CF MX (as well as 4.5+). Plus, for those that may not
have installed a cfx tag before it comes with instructions for that as well.  
  
Overall it looks like it would be pretty handy. If you have used it before and
have an opinion of it please leave a comment.  

