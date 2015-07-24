---
layout: post
title: "CF5 and Excel - a real pain"
date: 2005-02-14
comments: false
categories:
 - coldfusion
 - excel
---
Well I have been struggling with CF5 and MS Excel interoperability now for a
few days and I have to say, "I'm annoyed!"

I have tried to invoke a COM component to read the Excel file since the
customer does have Excel installed on their server:


```cfc
<!--- Create an Excel component --->
<cfobject action="Create" type="COM" class="Excel.Application"
name="objExcel">

```


but something as simple as:


```cfc
<!--- Load the file into the component and save ast a comma seperated list
--->
<cfset displayalerts=" 0">

```


fails with the error:

    Unable to set the DisplayAlerts property of the Application class






Doesn't matter if I'm using Excel 2000, 2003, or XP. So I thought, I'll give the option suggested by a commenter - create a DSN and query the uploaded Excel file.


So, I setup a DSN using CF Admin and the Merant Excel drivers but then I get a different error:


```cfc

 ODBC Error Code = S1000 (General error)

 [Microsoft][ODBC Excel Driver]General error Not enough information to connect to this DSN with SQLConnect.

 Use SQLDriverConnect.

 SQL = "SELECT * FROM [CF$] IN 'C:\WINNT\TEMP\ACF3C3.tmp' 'Excel 8.0;'" Data Source = "EXCEL_DSN"

```




So, I thought, well I'll try and use the MS Excel Driver (.xls) and see what happens. So I headed to the ODBC Administrator of Windows and setup a System DSN


```cfc

 Error Diagnostic Information

 ODBC Error Code = S1C00 (Driver not capable)

 [MERANT][ODBC Excel driver]Optional feature not implemented.

 SQL = "SELECT * FROM [CF$] IN 'C:\WINNT\TEMP\ACF3C4.tmp' 'Excel 8.0;'"

 Data Source = "EXCELDSN"

```




First off, I know the DSN names between the two are different - that's intentional. Secondly I have also tried both with the queries in these two formats:






```sql
 SELECT *

 FROM [CF$]

 IN '#attributes.inputFile#' 'Excel 8.0;'

 AND

 SELECT *

 FROM "Excel 8.0; DATABASE=#attributes.inputFile#; HDR=YES".[1]


```




The first format I found on the [Macromedia site](http://www.macromedia.com/cfusion/knowledgebase/index.cfm?event=view&id=KC.tn_18656&amp;amp;extid=tn_18656&dialogID=3070366&iterationID=2&sessionID=4830a5c3a1b4$3F$3F$3&stateID=1%200%2019642060&mode=simple) the second format I aquired from [Samuel Neff](http://www.rewindlife.com/) in an example he had on his site.  Both generate the same errors for the corresponding Excel driver.


So, now I'm going to try the [cfx_excel2query](http://www.emerle.net/programming/display.cfm/t/cfx_excel2query) tag I posted about before. The problem is I have to now have the excel file modified before I can use it because the header row is actually the second row. If I could have used the COM option then the end user wouldn't have to change the spreadsheet. Who knows, maybe the custom tag won't work either!


If you have any ideas on why this isn't working - please feel free to share your thoughts with me.  I'm going crazy!





## Comments











Bill






No sorry, the only solution I found was to upgrade to CFMX 6 (or 6.1) and it worked fine then.


I fear it just won't work with CF5.











Anonymous






Found your site by having my own Excel/CF/COM issues.


Ever make it work?










