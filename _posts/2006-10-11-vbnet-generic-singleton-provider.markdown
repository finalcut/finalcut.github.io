---
layout: post
title: "VB.Net Generic Singleton Provider"
date: 2006-10-11
comments: false
categories:
 - vb.net
 - pattern
 - generics
 - design patterns
 - singleton
---
I took the c# generic singleton provider example found at [The Code
Project](http://www.codeproject.com/csharp/genericsingleton.asp) and converted
it to VB.net syntax using the [power of generics](http://www.ondotnet.com/pub/
a/dotnet/2004/05/25/whidbey_vbnet_pt2.html). Here it is:  
  
```vb  
Public Class SingletonProvider(Of itemtype As {New})  
Public Sub New()  
End Sub  
  
  
Public Shared ReadOnly Property Instance() As itemtype  
  
Get  
Return SingletonCreator.instance  
End Get  
  
End Property  
Class SingletonCreator  
Shared Sub New()  
End Sub  
  
Public Shared ReadOnly instance As itemtype = New itemtype()  
End Class  
End Class  
```  
  
Now, whenever you want to create a singleton object you call this provider.
For example, lets say you want a singleton instance of your DAO Factory which
you conveniently called daoFactory you create it like so:  
  
```vb  
Dim myDaoFactory as DaoFactory = Singleton(Of DaoFactory).Instance  
```  
  
The prior implementation of the Singleton provider has one constraint on it;
that is the objects you want to create as singletons have to have a public New
method that takes in zero parameters.  
  
A cool thing about this is now the code for managing the singleton creation is
removed from all your objects and your objects can focus on what they actually
do instead of how to persist themselves in memory.

