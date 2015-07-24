---
layout: post
title: "WSO2 API Manager with Remote Governance"
date: 2012-11-21
comments: false
categories:
 - java
 - mysql
 - registry
 - wso2
 - governance
 - api-manager
---
NOTE: this article is superceded by my revised version at [WSO2 API Manager
with Remote Governance : The Mostly Complete
Guide](http://code.rawlinson.us/2012/11/wso2-api-manager-with-remote-
governance_29.html) \- Please refer to it instead of this! As you might have
seen in[ my last post](http://code.rawlinson.us/2012/11/configure-wso2-api-
manager-to-run-on.html) I'm mucking around with the [WSO2 API
manager](http://wso2.com/products/api-manager/).  To be honest I don't really
know what every component of the WSO2 stack is for yet but I'm slowly coming
to terms with a few.  Today, was the day to try to tie the[ WSO2 Governance
Registry](http://wso2.com/products/governance-registry/) into the mix by
having my various API Manager nodes use remote governance.  Now, honestly, I'm
not sure what the governance registry does.  However, some WSO2 people have
suggested it should be setup as part of my distributed effort so I pursued it.
Their website has a lot of jargon on it that makes the Governance Registry
sound pretty important but; again, I'm just not sure what role it actually
plays within the API Manager. I suspect it is what actually does the API
consumption throttling based on the rules set in the API Publisher.  
  
Anyway, I started the process of setting up the remote governance by using
[this blog post by Ajith](http://ajithvblogs.blogspot.com/2012/09/create-jdbc-
mount-to-wso2-governance.html) whom, as of this writing, is an employee of
WOS2.  However, there are some small errors in the blog posting and some areas
where some clarification is needed so I'm basically going to rehash that
article here with my corrections.  
  
Just like in Ajith's blog I am connecting to a mysql database.  Except I'm
connecting to it from some remote machines instead of from nodes on the same
machine as the Governance Registry.  This tutorial assumes mysql is already
installed.  I will refer to the Governance Registry as "GREG" at times.  
  

### Setting up the Governance Registry

  1. Create a new database within your mysql server:  

    
        $ mysql -u root -p  
    mysql> create database api_greg;  
    mysql> grant usage on *.* to username@'%' identified by 'somepassword';  
    mysql> grant all privileges on api_greg.* to usrename@'%';  
    ```
    NOTE: I use the @'%' instead of @localhost so that my database doesn't have to know what hosts might be connecting.  I'd suggest you limit yours to a subnet or defined set of hosts for security purposes. 
      2. Update the GREG database configuration:  
    {GREG_HOME}/repository/conf/datasources/master-datasources.xml like so:  
    
    
                <datasource>  
                <name>WSO2_CARBON_DB</name>  
                <description>The datasource used for registry and user manager</description>  
                <jndiConfig>  
                    <name>jdbc/WSO2CarbonDB</name>  
                </jndiConfig>  
                <definition type="RDBMS">  
                    <configuration>                                    <url>jdbc:mysql://{GREG_MYSQL_IP_OR_HOSTNAME}:3306/wso_greg?autoReconnect=true&relaxAutoCommit=true</url>  
    <username>standardstacks</username>  
                        <password>standardstacks</password>                    <driverClassName>com.mysql.jdbc.Driver</driverClassName>  
                        <maxActive>50</maxActive>  
                        <maxWait>60000</maxWait>  
                        <testOnBorrow>true</testOnBorrow>  
                        <validationQuery>SELECT 1</validationQuery>  
                        <validationInterval>30000</validationInterval>  
                    </configuration>  
                </definition>  
            </datasource>  
      
    ```
    
      3. edit {GREG_HOME}/repository/conf/datasources/axis2/axis2.xml and enable clustering by setting the enable attribute to true.  This is around line 541:  
    
    
         <clustering class="org.apache.axis2.clustering.tribes.TribesClusteringAgent" enable="true">```
    
      4. Make sure the[ mysql jdbc driver](http://dev.mysql.com/downloads/connector/j/) jar file is in the {GREG_HOME}/repository/component/lib directory
      5. Start GREG with the -Dsetup switch:  
    
    
        $ cd {GREG_HOME}/bin  
    $ ./wso2server -Dsetup  
    ```
    
    
    ### Setting up an API Manager Node to use the Remote Governance
    
    I'll refer to the API Manager as APIM from here on out.  All of the APIM nodes that will talk to the previously configured GREG need to be configured as follows:  
    
    
      1. Add a GREG datasource to your {APIM_HOME}/repository/conf/datasources/master-datasources.xml file  
    
    
        <datasource>  
        <name>WSO2_CARBON_DB_GREG</name>  
        <description>The datasource used for registry </description>  
        <jndiConfig>  
            <name>jdbc/WSO2CarbonDB_GREG</name>  
        </jndiConfig>  
        <definition type="RDBMS">  
        <configuration>  
                <url>jdbc:mysql://{GREG_MYSQL_IP_OR_HOSTNAME}:3306/wso_greg?autoReconnect=true&relaxAutoCommit=true</url>  
    <username>standardstacks</username>  
                <password>standardstacks</password>  
                <driverClassName>com.mysql.jdbc.Driver</driverClassName>  
                <maxActive>50</maxActive>  
                <maxWait>60000</maxWait>  
                <testOnBorrow>true</testOnBorrow>  
                <validationQuery>SELECT 1</validationQuery>  
                <validationInterval>30000</validationInterval>  
        </configuration>  
        </definition>  
    </datasource>  
    ```
    
      2. Edit your {APIM_HOME}/repository/conf/registry.xml file and insert the following four nodes at the end of the file just before the closing node </wso2registry>  
    
    
        <dbConfig name="mounted_registry">  
        <dataSource>jdbc/WSO2CarbonDB_GREG</dataSource>  
    </dbConfig>  
      
    <remoteInstance url="https://{GREG_IP_OR_HOSTNAME}:9464/registry">  
                    <id>instanceid</id>  
                    <dbConfig>mounted_registry</dbConfig>  
                    <readOnly>false</readOnly>  
                    <enableCache>true</enableCache>  
                    <registryRoot>/</registryRoot>  
    </remoteInstance>  
      
    <mount overwrite="true" path="/_system/config">  
                <instanceId>instanceid</instanceId>  
                <targetPath>/_system/nodes</targetPath>  
    </mount>  
      
    <mount overwrite="true" path="/_system/governance">  
                <instanceId>instanceid</instanceId>  
                <targetPath>/_system/governance</targetPath>  
    </mount>  
    ```
    
      3. Enable clustering in axis2 {APIM_HOME}/repository/conf/datasources/axis2/axis2.xml  
    
    
         <clustering class="org.apache.axis2.clustering.tribes.TribesClusteringAgent" enable="true">```
    
      4. Make sure the[ mysql jdbc driver](http://dev.mysql.com/downloads/connector/j/) jar file is in the {GREG_HOME}/repository/component/lib directory
      5. Start the APIM node  
    
        $ cd {APIM_HOME}/bin  
    $ ./wso2server```
    
      6. Once the APIM starts you'll see some records like this in the console log: 
    
        [2012-11-21 10:03:52,652]  INFO - EmbeddedRegistryService Configuredry in 674ms  
    [2012-11-21 10:03:52,875]  INFO - EmbeddedRegistryService Connected to mount at mounted_registry in 9ms  
    [2012-11-21 10:03:53,675]  INFO - EmbeddedRegistryService Connected to mount at mounted_registry in 0ms  
    [2012-11-21 10:03:53,834]  INFO - RegistryCoreServiceComponent Registry Mode    : READ-WRITE  
    ```
    Those should appear fairly early in the log - but they can be hard to see sometimes.  You can also check the management console by going to the Main tab | Resources Accordian | Browse Option.  Once there expand the _system node in the main panel.  If the config and governance have a folder with an arrow on them they are connecting to the remote governance registry.  Congratulations! 
    
    [![](http://2.bp.blogspot.com/-55nUVo1hTPY/UKz9IQ0gjvI/AAAAAAADDtU/jlZHbi5LvCk/s320/api_manager_remote_governance.gif)](http://2.bp.blogspot.com/-55nUVo1hTPY/UKz9IQ0gjvI/AAAAAAADDtU/jlZHbi5LvCk/s1600/api_manager_remote_governance.gif)
    
      
    
    
      
    NOTE: please make sure the camelCase used in all of my example XML matches what you are putting into your files.  If you don't use the right case the settings won't be picked up and you'll potentially see errors like  
    
    
    
    WARN {org.wso2.carbon.registry.core.config.RegistryConfigurationProcessor} -  The instance     identifier was not specified for the mount: /_system/config {org.wso2.carbon.registry.core.config.RegistryConfigurationProcessor}  
    ```
      
      
    
    
    
    

