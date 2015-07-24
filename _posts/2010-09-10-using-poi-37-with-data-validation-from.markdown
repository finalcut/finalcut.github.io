---
layout: post
title: "Using POI 3.7 with Data Validation from CF"
date: 2010-09-10
comments: false
categories:
 - coldfusion
 - java
 - poi
---
I have been using POI (The Java library for reading/writing Microsoft Office
documents) on and off for a few years but just recently I needed to build a
Spreadsheet that had data validation rules built in; specifically I needed the
ability to constrain the input to a field to a specific range of values.
Prior to POI 3.7 this wasn't possible.  Now it is and here is how you do it.  
  
In this example I'm actually going to use an Excel Formula to limit the values
that can be entered in a cell.  The formula just identifies a range of cells
that have valid values.  I also am using a helper function I previous wrote to
get the sheet from my currently active workbook.  If you need to know how to
get an active workbook or to get a sheet from the book I encourage you to
check out the [POI API
documentation.](http://poi.apache.org/apidocs/index.html)  
  
  
```cfm <cfscript>  
var l = structNew();  
var sheet = getSheet(1);  
var formula = "=$P$8:$P$14";  
var startRow = 1;  
var endRow = 10;  
var startCell = 4;  
var endCell = 4;  
l.helper = createObject("java",
"org.apache.poi.xssf.usermodel.XSSFDataValidationHelper").init(sheet);  
l.constraint = l.helper.createFormulaListConstraint(formula);  
l.range = createObject("java","org.apache.poi.ss.util.CellRangeAddressList").i
nit(startRow,endRow,startCell,endCell);  
l.validation = l.helper.createValidation(l.constraint,l.range);  
l.validation.setShowErrorBox(true);  
l.validation.setErrorStyle(0);  
l.validation.createErrorBox("Invalid Selection","Please select a value from
the dropdown options.");  
sheet.addValidationData(l.validation);  
</cfscript>  
```  
Here's what's going on. I have actually extracted this from a cffunction that
takes in the sheetIndex, the formula, the startRow, endRow, startCell, and
endCell as arguments. The indexes (inc row and cell) are all zero based.  
  
You can create a XSSFDataValidation object without the helper but it is safer
and a better idea to use the helper class. The helper class has a few
different methods to make it easier for you to get the correct type of
DataValidation object without having to know about, or have access to, some
different enumerations.  
  
As you can see, once I have the helper class I tell it to create a Formula
Constraint. If you look at my formula I'm just providing a range of cells.
Those cells are prepopulated with the values that can be used in the cell(s)
I'm applying the constraint to.  
  
After creating constraint I then define a range of cells that I want to apply
the constraint to. Then I create a validator object passing in the constraint
and the range of cells. Next I define a few rules for how to handle the
validation; for instance I want an error box to popup with a custom message.
The ErrorStyle part is using a value of 0 which means "STOP" don't let the
invalid change happen to the field.  
  
Finally I add the validation rules to the sheet. Eventually I write the
workbook to a file and when I open it I am greeted with a range of cells on
the second sheet (index 1) from the second row (index 1) to the 11th row
(index 10) in the "E" column (index 4) that limits my entry to a dropdown list
of choices.  
  
If you have any questions just ask and I'll try to respond.

## Comments

Bill

Jason,  
  
the stuff I wrote in CF gets converted to Java so I assume it works. However,
I didn't try it with a string array; instead I used cell values to constrain a
different cell.  
  
I'll try it in Java only and let you know.  
  
Bill

Anonymous

Has anyone successfully been able to get the XSSF Data Validation working in
POI 3.7 in Java? I'm trying to create a simple drop down list...  
  
I have tried something like this:  
_  
final XSSFWorkbook wb = new XSSFWorkbook();  
final XSSFSheet sheet = wb.createSheet("Project Data");  
final Row r = sheet.createRow(0);  
final Cell cell = r.createCell(0);  
  
final String[] excelListValues = new String[] { "Robin", "Chris", "Jason",
"Rajat", "Greg" };  
  
final XSSFDataValidationHelper h = new XSSFDataValidationHelper(sheet);  
final CellRangeAddressList addressList = new CellRangeAddressList(0, 0, 0, 0);  
final DataValidationConstraint dvConstraint =
h.createExplicitListConstraint(excelListValues);  
final DataValidation dataValidation = h.createValidation(dvConstraint,
addressList);  
dataValidation.setSuppressDropDownArrow(false);  
sheet.addValidationData(dataValidation);  
_  
and wrote out the file, but when I open it in Excel, there is no data
validation (drop down list). If I literally change the "XSSF"s to "HSSF"s
above, it works fine when reading it back to Excel...e.g. the list shows up.  
  
Any help/examples would be appreciated. I'm using 3.7 beta 2.  
  
Thanks,  
  
Jason

