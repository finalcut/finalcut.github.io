---
layout: post
title: "Coldspring - Config Bean Inheiritance"
date: 2008-10-18
comments: false
categories:
 - coldfusion
 - oop
 - coldspring
---
In one of my apps a large chunk of the basic config data is the same but 2
fields are different depending on which client you are logged in as: the
datasource and the clientSchema name. However, each client still needs the
rest of that config data; so I rolled a means of supporting inheritance in my
coldspring bean. Inheritance of ColdSpring defined properties as opposed to
inheritance of functionality specifically.  
  
Every configService bean I have has to extend this:  

    
    
      
     <bean id="baseConfigService" class="LB2.config.beans.baseConfigService" singleton="true">  
      <property name="properties">  
       <map>  
        <entry key="importDSN"><value>SpecialAccessDBDataSourcePlaceHolder</value></entry>  
          
        <entry key="rootPath"><value>C:\dev\websites\WEBSITE\PATH\</value></entry>  
        <entry key="relRoot"><value>/MySiteRoot/</value></entry>  
          
        <entry key="siteEmailAddress"><value>AdminEmailAddress</value></entry>  
        <entry key="commonSchema"><value>SHARED_SCHEMA_NAME</value></entry>  
       </map>  
      </property>  
     </bean>  
    ```
      
      
    Normally I would have to have that exact same stuff pasted into each clients config bean definition which, frankly, sucked because the paths and datasource names change depending on how the customer wants them all setup so then he had to make a bunch of duplicate edits.  Not a good plan at all.  Now a client specific configService bean looks like this:  
      
    
    
    
      
     <bean id="clientXConfigService" class="LB2.config.beans.configService" singleton="false">  
      
      <property name="properties">  
       <map>  
        <entry key="dsn"><value>CLIENT_DATASOURCE</value></entry>  
        <entry key="clientSchema"><value>CLIENT_SPECIFIC_SCHEMA</value></entry>  
       </map>  
      </property>  
      
      <property name="baseConfigService">  
       <ref bean="baseConfigService"/>         
      </property>  
     </bean>  
    ```
      
      
    Now, this might seem kind of obvious so far but really, what I want to be able to do is call my client level config service, and ask for a property that might exist in either the base service or the client service and have it return it without any of my code caring at which level the property is defined.  This is taken care of through my baseConfigService.cfc and the configService.cfc.  
      
    
    
    ### baseConfigService.cfc
    
      
    
    
    
      
    <!---   
    --->  
      
    <cfcomponent name="baseConfigService"  
        hint="Config Service API.">  
      
     <cffunction name="init" access="public" returntype="LB2.config.beans.baseConfigService" output="false"  
        hint="Constructor. I create a new ConfigService">  
      <cfset variables.properties = structnew()/>  
      <cfreturn this/>  
     </cffunction>  
      
     <cffunction name="setProperties" access="public" returntype="void" output="false"  
        hint="I overwrite all propertie in the configuration service">  
      <cfargument name="properties" type="struct" required="true" />  
        
      <cfset variables.properties = arguments.properties  />  
      
     </cffunction>  
      
     <cffunction name="setProperty" access="public" returntype="void" output="false"  
        hint="I set a property in the configuration service">  
      <cfargument name="PropertyName" type="string" required="true" />  
      <cfargument name="PropertyValue" type="any" required="true" />    
        
      <cfset variables.properties[arguments.propertyName] = arguments.propertyValue />  
        
     </cffunction>  
      
     <cffunction name="getProperty" access="public" returntype="any" output="false"  
        hint="I get a property from the configuration service">  
      <cfargument name="PropertyName" type="string" required="true" />  
      
      <cfif structKeyExists(variables.properties,arguments.propertyName)>  
       <cfreturn variables.properties[arguments.propertyName]/>  
      <cfelse>  
       <cfthrow type="ConfigSerivce.PropertyNotFoundException" message="Property: #arguments.propertyName# is not known to the config service and thus cannot be retrieved." />  
      </cfif>  
      
     </cffunction>  
       
      
     <cffunction name="removeProperty" access="public" returntype="any" output="false"  
        hint="I remove a property from the configuration service">  
      <cfargument name="PropertyName" type="string" required="true" />  
       
      <cfif structKeyExists(variables.properties,arguments.propertyName)>  
       <cfset structDelete(variables.properties,arguments.propertyName)/>  
      <cfelse>  
       <cfthrow type="ConfigSerivce.PropertyNotFoundException" message="Property: #arguments.propertyName# is not known to the config service and thus cannot be removed." />  
      </cfif>  
        
     </cffunction>  
       
      
    </cfcomponent>  
    ```
      
      
    My configService cfc actually has a child object in it of type baseConfigService while also extending the baseConfigService at the same time.  
      
    
    
    ### configService.cfc
    
      
    
    
    
      
    <cfcomponent name="ConfigService"  
        hint="Config Service API."  extends="baseConfigService">  
      
     <cffunction name="init" access="public" returntype="LB2.config.beans.ConfigService" output="false"  
        hint="Constructor. I create a new ConfigService">  
      <cfset variables.properties = structnew()/>  
      <cfset variables.baseproperties = "" />  
      <cfreturn this/>  
     </cffunction>  
      
     <cffunction name="getProperty" access="public" returntype="any" output="false"  
        hint="I get a property from the configuration service">  
      <cfargument name="PropertyName" type="string" required="true" />  
      
      <cfset var val = "" />  
      
      
      <cfif structKeyExists(variables.properties,arguments.propertyName)>  
       <cfset val = trim(variables.properties[arguments.propertyName])/>  
      <cfelse>  
       <cfset val = trim(getBaseProperty(arguments.propertyName)) />  
       <cfset setProperty(arguments.propertyName, val) />  
      </cfif>  
      
      <cfif NOT LEN(val)>  
       <cfthrow type="ConfigSerivce.PropertyNotFoundException" message="Property: #arguments.propertyName# is not known to the config service and thus cannot be retrieved." />  
      </cfif>  
        
      <cfreturn val />  
     </cffunction>  
       
     <cffunction name="getBaseProperty" access="private" returntype="any" output="true"  
       hint="I try to get a property from the base setting object if it exists">  
      <cfargument name="PropertyName" type="string" required="true" />  
      
       <cfset var val = "" />  
      
      
        <cfif isObject(variables.baseproperties)>  
        <cftry>  
         <cfset val = variables.baseproperties.getProperty(arguments.PropertyName) />  
         <cfcatch>  
          <!--- do nothing if the base fails --->  
         </cfcatch>  
        </cftry>  
        </cfif>  
      
       <cfreturn val />  
      
     </cffunction>  
      
      
     <cffunction name="setBaseConfigService" access="public" returntype="void" output="false">  
      <cfargument name="settings" type="any">  
        
      <cfset  variables.baseproperties = arguments.settings />  
     </cffunction>  
      
    </cfcomponent>  
    ```
      
      
    Now you can see, my clientConfig service tries to find the property locally and if that fails then it tries to find it in the baseConfigService.  If it finds it in the baseConfigService it caches it locally so it doesn't have to dig down later.  If it can't find the property at either level then an exception is thrown.  
      
    
    
    #### Incorporating Parent Beans
    
      
    When ColdSpring 1.2 first came out I had hoped that I could simplify this setup by using the [parent attribute](http://www.coldspringframework.org/coldspring/examples/quickstart/index.cfm?page=parentbeans) and then I could just have the main properties defined in one bean and have the secondary properties defined in each client bean.  This basically ends up defining the properties node twice within one bean.  It turns out, unsurprisingly, that you can't really do this.  What did suprise me was that ColdSpring doesn't throw an exception it just ignores the second properties node (that which is defined in the baseConfigService bean definition).  
      
    You could pretty easily refactor what I have done though to support the idea of the parent bean but I'm not sure anything would be gained from it; in fact I think it would probably just cause me to have a less readable coldspring configuration.  
      
    Sadly, I can't incorporate the Parent Bean to help improve this method.  Both my baseConfigService and my configService define a property element named properties.  By defining the parentBean the properties element in the baseConfigService is just ignored.
    
    
    

