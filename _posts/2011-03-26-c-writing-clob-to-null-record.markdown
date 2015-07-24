---
layout: post
title: "C# Writing a CLOB to an Oracle Database GOTCHA"
date: 2011-03-26
comments: false
categories:
 - c#
 - oracleclob
 - oracle
 - clob
---
This may not apply to everyone but it did for me using Visual Studio 2008 with
.Net 3.5  
  
I found plenty of examples on how to write a CLOB to an Oracle Database but
none of them worked if the CLOB cell currently had nothing it in to write to.
Thus I came up with this solution.  
  
Sadly, it involves writing to the database twice.  The first  inserts a single
space character into the field and the second actually writes the CLOB.  Here
is some source code to help.  
  
  
Listing 1: Update the clob cell to have a single space in it.  
```cs string sql = "UPDATE table SET mycell = :myval WHERE myid = :myid";  
OracleConnection conn = GetConnection(); //helper method that gets my
connection object.  
conn.Open();  
using(OracleCommand sqlCommand = new OracleCommand(sql, conn);  
{  
OracleParameter myval = sqlCommand.Parameters.Add("myval",
OracleType.VarChar);  
myval.Value = " ";  
  
OracleParameter myid = sqlCommand.Parameters.Add("myid", OracleType.Int16);  
myval.Value = idValue; // assume idValue was predefined..  
  
sqlCommand.ExecuteNonQuery();  
}  
UpdateClob("table", "mycell", "WHERE id = " + idValue.ToString(),
stringValue); // stringValue is predefined and is what will be finally stored
in the CLOB  
```  
  
UpdateClob is a function that will actually write the final value to the CLOB
field:  
```cs protected void UpdateClob(string table, string column, string where,
string value)  
{  
var sql = "SELECT " + column + " FROM " + table + " " + where + " FOR UPDATE";  
  
// you need to convert your string into a byte array to pass into to the CLOB
later  
byte[] newvalue = System.Text.Encoding.Unicode.GetBytes(value);  
  
  
OracleConnection conn = GetConnection();  
OracleTransaction transaction = conn.BeginTransaction();  
using (OracleCommand cmd = conn.CreateCommand())  
{  
cmd.Transaction = transaction;  
cmd.CommandText = sql;  
using (OracleDataReader reader = cmd.ExecuteReader())  
{  
if (reader.Read())  
{  
OracleLob clob = reader.GetOracleLob(0);  
// if I didn't prepopulat the field the clob object would mysteriously have a
null connection object.  
clob.Write(newvalue, 0, newvalue.Length);  
clob.Close();  
}  
}  
transaction.Commit();  
}  
}  
```  
Anyway, overall it's a pretty straight forward process but kind of kludgy
considering you have to write to the table twice. I could not just use a
parameterized query to pass in the CLOB's byte array value. And, if I pre-
wrote with an empty string like "" then it was as if I did nothing so I had to
prepopulate with at least one character.  
  
Oddly enough, if I prepopulated with something like "PLACEHOLDER STRING" and
then tried to write an empty string to it using the clob.Write() the method
call succeeded by the value of the column didn't update.  
  
I can't say it makes a lot of sense but there you have it.

## Comments

Anonymous

Thank You So Much Man, been wasting time until I found your blog.

