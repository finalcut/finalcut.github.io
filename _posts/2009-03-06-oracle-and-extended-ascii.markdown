---
layout: post
title: "Oracle and Extended ASCII"
date: 2009-03-06
comments: false
categories:
 - sql
 - plsql
 - eclipse
 - extended-ascii
 - ascii
 - html
 - oracle
---
Yesterday I ran across a problem where I needed to compare the resultant
string from a query on a Sybase database and an Oracle database. The Oracle
result involved pulling back a single row that was delimted with an unusual
character, [Extended Ascii Char 0001](http://www.cdrummond.qc.ca/cegep/informa
t/Professeurs/Alain/files/ascii.htm).

Due to the code page of my viewing tool the character appeared as Extended
ASCII character 0218 but, when I tried to paste the character into a
confluence page for documenatation purposes it didn't appear (since it is
actually the non-printable character 0001) likewise it wouldn't appear in
Eclipse where a co-worker needed it.

Why would we need the character? Well because in the Sybase database to get
the equivalent string we need to concatenate about 8 columns. Initially we
were just going to concatenate them with this odd character as the delimiter
(we didn't realize it was ASCII 0001 yet). However, once things started to
resolve into being more complicated we decided, instead that we would use the
Oracle [TRANSLATE](http://www.techonthenet.com/oracle/functions/translate.php)
function to replace the special character with another, safer, printable
delimiter - the pipe | .

This reduced the number of times I needed to be able to print the weird
character in either eclipse or confluence to once however the problem still
persisted that the odd character wouldn't show up (obviously). Thus I had to
use the [ASCII](http://www.techonthenet.com/oracle/functions/ascii.php)
function in Oracle to figure out the character value of each character in a
specific record returned. At this point I had isolated the character as 0001.
However I wasn't entirely sure how to tell the TRANSLATE function to look for
unicode 0001. Fortunately there is [a function for
that](http://www.orafaq.com/forum/t/76872/0/) as well - [UNISTR](http://downlo
ad.oracle.com/docs/cd/B19306_01/server.102/b14200/functions204.htm)('\0001\\)

Thus, my final query had a line it it like so:



```sql

SELECT  TRANSLATE(accountInfo,UNISTR('\0001\'),'|')


```






