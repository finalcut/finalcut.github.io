---
layout: post
title: "Bi-Directional MAP in Java with Enumerations"
date: 2010-10-06
comments: false
categories:
 - java
 - enumerations
 - enums
---
I recently had a problem where I needed something like a
HashMap<string,object> but I needed to be able to lookup both the key from the
value and the value from the key.   There are a couple ways of doing this but
my final solution utilized some of the pretty cool features in Java's
enumeration (enum) implementation.  
  
Enumerations are basically just lists of things.  In most languages you'll
have something like:  
  
  
```java enum Boys { JOHN, MARK, TOM, CARL, BILL }  
```  
  
In Java you can do basically the same thing OR you can treat your enumeration
just like a class and add additional methods and constructors to it.  Sounds
crazy so I'll show you an example that solves the initial problem I described.  
  
```java import java.util.EnumSet;  
...  
  
public enum ConnectionStatus {  
UNSPECIFIED(""), CONNECTED("Y"), DISCONNECTED("N"), SHUTDOWN("S");  
  
private static final Map<String, ConnectionStatus> lookup = new
HashMap<String, ConnectionStatus>();  
  
static {  
for (ConnectionStatus s : EnumSet.allOf(ConnectionStatus.class))  
lookup.put(s.getCode(), s);  
}  
  
private String code;  
  
private ConnectionStatus(String code) {  
this.code = code;  
}  
  
public String getCode() {  
return code;  
}  
  
public static ConnectionStatus get(String code) {  
return lookup.get(code.toUpperCase().trim());  
}  
  
}  
```  
  
So what does all that do? It's pretty remarkable really. The initial part  
```java UNSPECIFIED(""), CONNECTED("Y"), DISCONNECTED("N"), SHUTDOWN("S");  
``` calls the private constructor, passing in a string ("", "Y", "N", and
"S"), for the ConnectionStatus enum for each of the items in the list. The
Constructor then sets a private member variable, within the enum, to the
"code" string passed in:  

    
    
    private String code;  
      
            private ConnectionStatus(String code) {   
                this.code = code;   
            }  
    ```
      
    There is also a private member variable, within the enumeration called "lookup" that stores the relationships between the codes and the enumeration values in a map; the static block of code right after the private lookup variable is declared initializes the map.  
    ```java
    private static final Map<String, ConnectionStatus> lookup = new HashMap<String, ConnectionStatus>();  
      
            static {   
                for (ConnectionStatus s : EnumSet.allOf(ConnectionStatus.class))   
                    lookup.put(s.getCode(), s);   
            }  
    ```
      
      
    Notice that both of those portions are static while the code member variable, and obviously, the constructor are not.  The static stuff is a "class variable" and thus is shared across all instances of the class (or enumeration) and the non-static stuff are instance variables and are unique to each instance of the enumeration (UNSPECIFIED, CONNECTED, DISCONNECTED, and SHUTDOWN).  
      
    Because each instance of the enum stores it's code we can very easily get the associated code for each enumeration like so:  
    ```javaString connectionStatusCode = ConnectionStatus.CONNECTED.getCode();  
    ```
      
    Likewise, thanks to our static map we can pass in a code value and get back the corresponding enumeration  
    ```javaConnectionStatus connectionStatus = ConnectionStatus.get("S");  
    ```
      
    The get method is static and uses our static lookup map to efficiently find the corresponding enum for the letter provided; you'll notice I clean up the passed in code string so I can search regardless of case or padding; you may not want to do that.  
    ```javapublic static ConnectionStatus get(String code) {   
                return lookup.get(code.toUpperCase().trim());   
            }  
    ```
      
    Java really gives you a lot of power with their enumeration implementation.  If you wanted to you could add other methods and even "sub-enumerations" to the enumeration (though I can't think of a good use case for sub-enums).   Dig into them and you might be amazed at what you can accomplish.
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    Anonymous
    
    
    
    
    
    for (ConnectionStatus s : EnumSet.allOf(ConnectionStatus.class))  
    should be written as  
    for (ConnectionStatus s : ConnectionStatus.values())
    
    
    
    
    
    
    
    
    

