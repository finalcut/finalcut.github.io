---
layout: post
title: "@@identity, scope_identity(), ident_current"
date: 2005-08-19
comments: false
categories:
 - sql
---
I have been seeing more and more posts lately that discuss the pitfalls of
@@identity, the boon of using scope_identity(), and never mentioning
ident_current. So, consider this my entry into the conversation.  
  
I just wanted to clarfiy what the three functions do by reposting a part of
the transact-sql reference:  
  

> IDENT_CURRENT is not limited by scope and session; it is limited to a
specified table. IDENT_CURRENT returns the value generated for a specific
table in any session and any scope. For more information, see IDENT_CURRENT.  
  
SCOPE_IDENTITY and @@IDENTITY will return last identity values generated in
any table in the current session. However, SCOPE_IDENTITY returns values
inserted only within the current scope; @@IDENTITY is not limited to a
specific scope.

  
  
You can learn more about scope_identity at [MSDN -
SCOPE_IDENTITY()](http://msdn.microsoft.com/library/default.asp?url=/library
/en-us/tsqlref/ts_sa-ses_6n8p.asp)  
  
Information on ident_current is at [MSDN - IDENT_CURRENT('tablename')](http://
msdn.microsoft.com/library/default.asp?url=/library/en-us/tsqlref/ts_ia-
iz_82i1.asp)  
  
The pitfall of @@identity is that you won't necessarilly get the id value back
you expect. For instance, if the insert into TABLE A fires a trigger that
inserts another value into TABLE B you will get the new id for TABLE B when
you really wanted the id from TABLE A  
  
SCOPE_IDENITY() will give you the id from TABLE A even though the trigger
fired.  
  
You can use IDENT_CURRENT to get the id from both tables if you want:  

    
    
      
    select IDENT_CURRENT('tableA') as tableAID, IDENT_CURRENT('tableB') as tableBID  
    ```
    
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    Bill
    
    
    
    
    
    yes that is a restriction of IDENT_CURRENT - I don't know of a way to get a scope dependent identity where you specify the table name.
    
    
    
    
    
    
    
    
    
    
    Laury Burr
    
    
    
    
    
    Hi   
      
    Is the usefulness of IDENT_CURRENT actually restricted by being scope-independent? I'm just wondering how it might be used given the possibility of another user insering a record between your insert and the recall of that identity (other than, perhaps, wanting to be able to ascertain that such an insert has happened, maybe?)  
      
    I guess I'd like to see a real belt-and-braces - a scope-dependent identity where we actually specify the table name.
    
    
    
    
    
    
    
    
    

