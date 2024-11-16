---
layout: post
title: "POI Doesn't Like Open Office"
date: 2008-01-18
comments: false
categories:
 - coldfusion
 - excel
 - poi
 - openoffice
---
Late last year I had to work on a project that can read from or write to Excel
spreadsheets. The project was web based and used Coldfusion 7 so, naturally, I
used the Java POI library for the Excel integration. It worked like a champ
until I opened a word document in Open Office and then saved it as an Excel
spreadsheet.  
  
The code I had previously written for the same spreadsheet suddenly barfed. I
haven't had a chance to figure out what is different with the sheet after Open
Office saves it but, for the time being, just consider this a word of warning
- Open Office's Excel format is a touch different than that used by MS Office.  
  
The document will still open and look the same in MS Office - but POI seems to
think there are extra cells with actual content in them after Open Office has
touched it.  
  
Consider yourself warned

## Comments

Anonymous

thanks a lot

Anonymous

I fixed issues with reading open office saved xls files. via the two codes:  
164: // same as 0 Default of "General"  
  
case 165: // Default of "Text"  
same as 0x31: // "@" - This is text format. "Text" - Alias for "@"  
  
but I have a problem, that when I output an xls from POI and then open it with
OpenOffice all the rows with data are hidden.

