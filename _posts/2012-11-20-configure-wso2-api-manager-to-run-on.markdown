---
layout: post
title: "Configure WSO2 API Manager to Run on Multiple Nodes"
date: 2012-11-20
comments: false
categories:
 - java
 - mysql
 - wso2
 - api-manager
---
I'm working on some unusual stuff right now; stuff with a lot of promise but
not enough documentation thus I've decided to document some of the more
complicated things here on my blog.  They are a bit out of the realm of my
normal blog posts.  
  
The WSO2 suite of products is basically an extension on a whole range of
Apache projects that are setup in a way that is supposed to be easy to deploy
and extend in a distributed environment. These apps are each built on top of
the WSO2 carbon framework. I'm not really sure it is as easy as they try to
suggest in their marketing materials.  
  
The API Manager is actually a pretty interesting product.  It creates a facade
to your API's that enables you to give out metered access to the API.
Basically external developers can subscribe to the API (thus get an API key)
and then you, as the owner of the API, can offer several levels of service and
even monetize the API access if you choose.  
  
The API manager is broken down, basically, into three parts.  The API Manager
- which is really an Enterprise Service Bus that meters access to the API
based on rules defined in the  API Publisher.  The author of the API can
publish their APIs through the publisher which is a Jaggery (server side
javascript framework made by WSO2) web application.  Once an API is in the
"published" status in the publisher it is then available to developers via the
API Store.  Registered users of the API store can browse and search across the
various APIs and subscribe to those APIs they need for their application.  
  
The download from WSO2 comes with all three of these things; the Manager,
Publisher, and Store, within one application deployment.  Thus when you start
up the app (via a shell script) all three elements are available within the
same node.  That is okay when you need to put together a quick deployment but
if you want the flexibility of clustering and or distributed clustering then
you'll want to break the API Manager package up so that the API Manager piece
runs on one or more machines while the API Store runs on some other machines
and the API publisher runs on yet another set of machines.  
  
There are probably other ways to do this but I approached the problem as
follows.  First, I wanted to just remove the Publisher and Store components
from an installation to get just the API Manager running.  In order to do this
I went into the {apimanager} installation and deleted the following
directories: {apimanager}/repository/deploymentserver/jaggeryapps/publisher
and {apimanager}/repository/deploymentserver/jaggeryapps/store  
  
That at least removes the public face of the publisher and store so that
people can't go to either and start using that API Manger node in the
publisher or store roles.  I'm honestly not sure if there is anything else you
should delete but those seemed to be a good minimum.  
  
To create a node that serves as a publisher I just deleted the store jaggery
app and to create store I just deleted the publisher jaggery app.  Again, I'm
not sure if that is totally sufficient - especially since both are also
running in the management role at that point as well - but I was very
reluctant to delete more as I am not sure how much of the background "carbon"
stuff the publisher and store both need.  
  
At this point, if you don't do anything else, you'll have a Manager node, and
Publisher node, and a Store node all running but not communicating with each
other.  Thus, if you start up the publisher node and publish an API then start
the store node you won't see the published API.  You need to also setup a
shared datasource.  
  
It maybe possible to have all three point to one of the default "H2"
datasources that the API Manager uses by default but rather than pursue that I
decided to create a mysql server instance that the three could point to.
I'm not going to go into the details on mysql setup here beyond a few caveats:  
  

  1. make sure your new database is accessible by a user from various hosts.  Thus I created a new database sort of like this using the mysql command line:  
  

    
        $ mysql -u root -p  
    mysql> create database apimanager;  
    mysql> grant usage on *.* to username@'%' identified by 'somepassword';  
    mysql> grant all privileges on apimanager.* to usrename@'%';  
      
    ```
    That first grant command will let the user connect from different hosts.
      2. you also need to make sure the mysql server is listening for remote connections.  To do that edit your my.conf file and change the bind-address is set to the machines actual IP address as opposed to the 127.0.0.1 or 0.0.0.0 address. 
    
    After you have your database setup you need to configure you're three (or more) nodes to point to the correct database.  To do this you need to edit the file {apimanager}/repository/conf/datasources/master-datasources.xml
    
    Both the WSO2_CARBON_DB and the WSO2AM_DB nodes should have a configuration similar to this:  
    
    
    
          <configuration>  
              <url>jdbc:mysql://MYSQLIPADDRESS:3306/apimanager?autoReload=true&amp;relaxAutoCommit=true</url>  
              <username>USERNAME</username>  
              <password>PASSWORD</password>  
              <driverClassName>com.mysql.jdbc.Driver</driverClassName>  
              <maxActive>50</maxActive>  
              <maxWait>60000</maxWait>  
              <testOnBorrow>true</testOnBorrow>  
              <validationQuery>SELECT 1</validationQuery>  
              <validationInterval>30000</validationInterval>  
          </configuration>  
    ```
    Once you've setup your configuration you also need to make sure the mysql JDBC driver is present.  You can fetch it from the [mysql site](http://dev.mysql.com/downloads/connector/j/).  Extract the files then copy the .jar file in the root directoy to {apimanager}/repository/components/lib/ directory of each node.  At this point you're nearly ready to go.  First start up one node with the switch -Dsetup like so (from within the {apimanager}/bin directory)    
    ```js
        ./wso2server.sh -Dsetup  
    ```
    That will start the node and create some of the tables that are necessary.  As of the writing of this post there is a problem though and it doesn't create the API manager specfic tables it just creates the carbon tables.  Thus you then have to go to the {apimanager}/dbscripts/apimgr directory, then connect to mysql and execute the mysql.sql script in the {apimanager}/dbscripts/apimgr.    
    
    
    
    $ mysql -u root -p  
    mysql> \u apimanager  
    mysql> \. mysql.sql  
    mysql> exit  
    ```
    Once your first node has finished starting stop it then start it again but without the -Dsetup switch.  In fact, don't use that switch again as it will wipe out the core tables and recreate them if you.  Then start up the other nodes and try to visit the publisher and store.  If you try to go to a publisher/store on a node where you removed the publisher/store jaggery app you'll be redirected to the carbon management console for the API manager.  However, when you start those nodes the log will still tell you the store or publisher exists.  Just ignore the false positives.  If you try to go to a publisher/store you think should exist and you are redirected to the carbon console then double check your ip address and port and try again - most likely you're attempting to visit a node that isn't setup in the role you're attempting to access it in.  NOTE: In the xml configuration you might have noticed that I have two flags set  on the connection string; autoReconnect and relaxAutoCommit.  These both have to be set to true when connecting to mysql or else the store will throw an exception every time you try to do anything that involves a database write operation.  Thus, if you see this error:    
    
    
    
    java.sql.SQLException: Can't call commit when autocommit=true  
    ```
    Then make sure you have setup the two flags in your connection string.
    
    
    

