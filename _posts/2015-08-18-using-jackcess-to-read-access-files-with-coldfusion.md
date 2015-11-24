---
layout: post
title: "Using Jackcess to read Access Files with ColdFusion"
description:
headline:
date: 2015-08-18 08:53:47 -0400
category: [coldfusion,java]
tags: [msaccess]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
Before I get into the code though let me defend my usage of MS Access.  Basically, I support a legacy Coldfusion application that has to routinely import data from uploaded Access databases into an Oracle database.  Thus, I have to have a script that can read from an access database.  Way back [in 2005 I talked a little bit about how I was reading from an access database that I didn't have a specific datasource defined for](/2005/11/model-glue-waist-deep.html).  What follows is the start of a more modern solution.


[Jackcess](http://jackcess.sourceforge.net/) is a cool Java library that gives you access to Access.  It's at sourceforge which is a problem of sorts but fortunately the download for this is just a `JAR` file and it seems to be contaminate free.

Jackcess has a pretty comprehensive [API](http://jackcess.sourceforge.net/apidocs/index.html) and a handy [Cookbook](http://jackcess.sourceforge.net/cookbook.html) that can help you get started.  But, if you aren't entirely confident in taking Java and embedding it in Coldfusion I'm going to show you the simplest bit of code you might need to read in all the rows from an Access table and putting that information into a Coldfusion `query` object.

**NOTE: I am not including any error handling on purpose here to keep things simple.  This should all be used with care and is not intended, as is, for produciton**

```cfm
<cfscript>
// create a reference to the DatabaseBuilder class.  We dont want to
// initialize it (construct) because we need access to a static method,
// open, with it
builder = CreateObject("java","com.healthmarketscience.jackcess.DatabaseBuilder");

// using java in Coldfusion is clunky. We We need to get the db file.
// Normally I'd do this inline with builder.open but that would be a mess
// to read.  So you have this.  You should probably have some code here to
// make sure the file actually exist before you try to open it.
dbFile = CreateObject("java", "java.io.File").init(arguments.targetPath);

// we are opening the file to read.  You should totally wrap all code after
// this in a try catch and make sure, in the finally, that you close the
// db.  Otherwise that pointer will hang out forever (basically) and you'll
// never be able to delete your temporarily uploaded db file).
db = builder.open(dbFile);

// Now that I am getting the table reference I could bypass the use of a
// Cursor as there is one sort of built into the table object.  However,
// even Jackcess suggests you get the cursor later. The cursor is certainly
// more flexible.  I'm assuming a valid tablename is passed in. The db
// object has a method called getTableNames() you could use to help make
// sure the table you're asking for is valid before moving on.
table = db.getTable(arguments.tableName);
cursor = table.getDefaultCursor();

// this gives you an array of objects.  Cool factoid about this array is
// it is just like a CF array and you can iterate over it just like a CF
// array and with that knowledge we can get a list of column names and
// initialize  a cfquery object.

// I'm not doing it here but the smart developer should also get the
// type of each column and make sure you initialize the cfquery columns
// with the correct type.

columns = table.getColumns();
columnList = "";
for(col in columns){
  columnList = ListAppend(columnList, col.getName());
}
finalQuery = queryNew(columnList);

rowCount = table.getRowCount();

// reset cursor to make sure we are guaranteed to be in the right place.
// which is, in this case, a magic spot right before the first row this
// way we can ask for the next row later and get the first row the first
// time we ask for the next row.
cursor.beforeFirst();

// now we just have to iterate over all of the rows of the table, and get
// each columns value in each row.. Pretty simple stuff really
for(rowIndex=1;rowIndex LTE rowCount; rowIndex=rowIndex+1){
  queryAddRow(finalQuery);
  row = cursor.getNextRow(); // on first iteration moves to first row
  for(col in columns){
    // because I have to use the column name twice I'll grab it first.
    columnName=col.getName();
    querySetCell(finalQuery, columnName, row.get(columnName));
  }
}

// make sure you close that database!!!
db.close();
</cfscript>

```

There, now all of the stuff that was in the Access table of `arguments.tableName` is in a Coldfusion `query` object with the same column names.

Obviously, as I mention in many comments, there are improvements that can be made here.  However, I trust that if you need to use Jackcess in Coldfusion this will be enough to get you started toward making some real production ready code.
