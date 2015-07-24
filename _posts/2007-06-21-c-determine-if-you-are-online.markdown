---
layout: post
title: "C# - Determine If You Are Online"
date: 2007-06-21
comments: false
categories:
 - .net
 - c#
---
You can use the following code to determine if you are online or not:  
  
```cs  
using System.Net.NetworkInformation;  
  
  
...  
  
  
  
public static bool IsOnline()  
{  
bool isConnected = false;  
NetworkInterface[] adapters = NetworkInterface.GetAllNetworkInterfaces();  
foreach (NetworkInterface n in adapters)  
{  
if (n.OperationalStatus == OperationalStatus.Up && n.NetworkInterfaceType !=
NetworkInterfaceType.Loopback)  
{  
// Since we have a non loopback interface up, we have a network connection  
isConnected = true;  
break;  
}  
}  
  
  
return isConnected;  
  
}  
```  
  
Update: I added a "break" to the loop so that I exit as soon as I find a good
connection.

## Comments

Bill

Thanks Paul.  
  
Here are [the documentation for
GetIsNetworkAvailable](http://msdn2.microsoft.com/en-us/library/system.net.net
workinformation.networkinterface.getisnetworkavailable.aspx)

Paul Lo

There is a more simple way:  
  
bool isNetworkAvailable =
System.Net.NetworkInformation.NetworkInterface.GetIsNetworkAvailable();

starsky

ignore me, I read it wrong :D

starsky

That function will only tell you if the last adapter in your collection is
online.

