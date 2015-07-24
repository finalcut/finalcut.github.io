---
layout: post
title: "Breaking up my Coldspring.xml file"
date: 2008-10-14
comments: false
categories:
 - coldfusion
 - coldspring
---
About a month ago I upgraded my coldspring copy so that I could reference
external xml files in the ColdSpring.xml file that I was using with my Model
Glue application. My primary motivation was so that it would be easier to
deploy the application and to separate the small bit of locale specific
configuration data out so that end users could more easily configure the app.  
  
I mucked around with it for a bit but wasn't entirely happy with the way I was
including additional files:  

    
    
      
     <import resource="./config.xml"></import>  
    ```
      
      
    I really didn't like that ./ part.  I also didn't put 1 and 1 together and realize I could have many different included files if I wanted.  Well, today I had a bit of an epiphany.  My app requires a CF Mapping of "LB2" and ColdSpring evaulates out the full path of the included xml file so now I can just do the following (plus I broke out major chunks of my configuration into separate files).  
    
    
    
      
     <import resource="/lb2/config/config.xml"></import>  
     <import resource="/lb2/config/pages.xml"></import>  
     <import resource="/lb2/config/menus.xml"></import>  
     <import resource="/lb2/config/gateways.xml"></import>  
     <import resource="/lb2/config/services.xml"></import>  
     <import resource="/lb2/config/dao.xml"></import>  
     <import resource="/lb2/config/aop.xml"></import>  
     ...  
    ```
      
    Now it is much easier to find a bean definition and it will be much cleaner when adding additional definitions in the future.
    
    
    

