---
layout: post
title: "Create a C# Model From a SQL Server Table"
date: 2011-09-29
comments: false
categories:
 - .net
 - c#
 - sql-server
---
If you aren't using a framework of some sort that helps make this even easier
here is a sql script that will help you generate a set of getters/setters for
a SQL Server table in C#.  
  
I haven't tested it much (nil) but it looks like it will work ok.  Basically
you can just cut and paste the records returned into your class definition and
you'll be good to go.  You may, however, wish to fix the case of the property
names to match the proper convention.  I'm not sure how to fix the case using
just SQL.  
  
  

    
    
      
    SELECT 'public '  +  
    		CASE data_type  
    			WHEN 'bigint'		THEN 'int'  
    --			WHEN 'binary'		THEN 'raw'  
    			WHEN 'bit'		THEN 'int'  
    			WHEN 'char'		THEN 'char'  
    			WHEN 'datetime'		THEN 'DateTime'  
    			WHEN 'decimal'		THEN 'decimal'  
    			WHEN 'float'		THEN 'float'  
    --			WHEN 'image'		THEN 'long raw'  
    			WHEN 'int'		THEN 'int'  
    			WHEN 'money'		THEN 'double'  
    			WHEN 'nchar'		THEN 'string'  
    			WHEN 'ntext'		THEN 'string'  
    			WHEN 'nvarchar'		THEN 'string'  
    			WHEN 'numeric'		THEN 'int'  
    			WHEN 'real'		THEN 'decimal'  
    			WHEN 'smalldatetime'	THEN 'DateTime'  
    			WHEN 'smallmoney'	THEN 'double'  
    			WHEN 'smallint'		THEN 'int'  
    			WHEN 'text'		THEN 'string'  
    			WHEN 'timestamp'	THEN 'Date'  
    			WHEN 'uniqueidentifier' THEN 'string'  
    			--WHEN 'varbinary'	THEN 'raw'  
    			WHEN 'varchar'		THEN 'string'  
    			ELSE 'CHECK THIS.. ' + data_type + ' DataType'  
    		END + ' ' + COLUMN_NAME + ' { get; set; }'  
    	  
    FROM information_schema.columns  
    WHERE table_name = 'class'  
    ```
     There are also a  few data types in here I'm not sure I converted properly; this was just a quick one-off thing I put together for a friend.  So, if you have any suggestions or corrections please leave them in the comments and I'll update it as I go.
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    Anonymous
    
    
    
    
    
    This is exactly what I was looking for. Thanks!  
      
    I made some changes to the data types:  
      
    SELECT 'public '  +  
     CASE data_type  
      WHEN 'bigint' THEN 'long'  
      WHEN 'binary' THEN 'byte[]'  
      WHEN 'bit' THEN 'bool'  
      WHEN 'char' THEN 'string'  
      WHEN 'date' THEN 'DateTime'  
      WHEN 'datetime' THEN 'DateTime'  
      WHEN 'datetime2' THEN 'DateTime'  
      WHEN 'datetimeoffset' THEN 'DateTimeOffset'  
      WHEN 'decimal' THEN 'decimal'  
      WHEN 'float' THEN 'float'  
      WHEN 'image' THEN 'byte[]'  
      WHEN 'int' THEN 'int'  
      WHEN 'money' THEN 'decimal'  
      WHEN 'nchar' THEN 'char'  
      WHEN 'ntext' THEN 'string'  
      WHEN 'numeric' THEN 'decimal'  
      WHEN 'nvarchar' THEN 'string'  
      WHEN 'real' THEN 'double'  
      WHEN 'smalldatetime' THEN 'DateTime'  
      WHEN 'smallint' THEN 'short'  
      WHEN 'smallmoney' THEN 'decimal'  
      WHEN 'text' THEN 'string'  
      WHEN 'time' THEN 'TimeSpan'  
      WHEN 'timestamp' THEN 'DateTime'  
      WHEN 'tinyint' THEN 'byte'  
      WHEN 'uniqueidentifier' THEN 'Guid'  
      WHEN 'varbinary' THEN 'byte[]'  
      WHEN 'varchar' THEN 'string'  
      ELSE 'CHECK THIS.. ' + data_type + ' DataType'  
     END + ' ' + COLUMN_NAME + ' { get; set; }'  
       
    FROM information_schema.columns  
    WHERE table_name = 'class'  
      
      
      
    Cheers,  
    Chris
    
    
    
    
    
    
    
    
    

