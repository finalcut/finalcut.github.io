---
layout: post
title: "WSO2 API Manager with Remote Governance : The Mostly Complete Guide"
date: 2012-11-29
comments: false
categories:
 - remote-governance
 - java
 - api
 - mysql
 - registry
 - greg
 - wso2
 - api-manager
---
This is a mostly complete rewrite of the article that I previously wrote with
the same name. I am doing this because I made some mistakes the first time
around.
As you might have seen in[ my last post](http://code.rawlinson.us/2012/11
/configure-wso2-api-manager-to-run-on.html) I'm mucking around with the [WSO2
API manager](http://wso2.com/products/api-manager/).  To be honest I don't
really know what every component of the WSO2 stack is for yet but I'm slowly
coming to terms with a few.  Today, was the day to try to tie the[ WSO2
Governance Registry](http://wso2.com/products/governance-registry/) into the
mix by having my various API Manager nodes use remote governance.  Now,
honestly, I'm not sure what the governance registry does.  However, some WSO2
people have suggested it should be setup as part of my distributed effort so I
pursued it.  Their website has a lot of jargon on it that makes the Governance
Registry sound pretty important but; again, I'm just not sure what role it
actually plays within the API Manager. I suspect it is what actually does the
API consumption throttling based on the rules set in the API Publisher.
Anyway, I started the process of setting up the remote governance by using
[this blog post by Ajith](http://ajithvblogs.blogspot.com/2012/09/create-jdbc-
mount-to-wso2-governance.html) whom, as of this writing, is an employee of
WOS2.  However, there are some small errors in the blog posting and some areas
where some clarification is needed so I'm basically going to rehash that
article here with my corrections.
Before I get into configuration specifics here is the basic setup. I'm running
four api manager (APM) nodes and a single Governance Registry (GREG) node. I'm
also using mysql as my database for all data storage. I am not currently using
a Business Activity Monitor (BAM) becuase I haven't been able to get one to
work.
My four APM nodes are broken down like this - a store, a publisher, a
keymanager, and a gateway. The store and publisher are Jaggery (server side
javascript) apps that depend on some core WSO2 carbon stuff on the server.
Both the store and the publisher are configured to use the gateway and
keystore. The gateway is where API requests are sent by those people using
APIs they subscribe to via the store. The keymanager serves two roles; first
it controls user authentication into the Store, the Publisher, and the "Carbon
Console" which is sort of a management application all of the various WSO2
carbon apps have built in. The second role of the keymanager is to issue API
keys and authenticate applications that are attempting to use an API - thus
the gateway is also configured to use the keymanager.
I've created four mysql databases for the purpose of this example - and I
advise you to separate out your databases in a similar fashion.

api_mgr


This is where API information stored and fetched by the four APM nodes
api_grg


This is a registry database used by the GREG and the various APM nodes.  User information will also end up being stored here.
NOTE: The structure of the api_usr, api_reg, and api_grg databases are all
identical. However, not all tables are actually used within each database.

### Database Setup

Here is a quick script to create the databases, create the user "wso2carbon"
with password (identified by) "wso2carbon" and to grant access to that user
from any other remote host to the four databases


```sh





mysql> create database api_mgt;

Query OK, 1 row affected (0.00 sec)


mysql> create database api_grg;

Query OK, 1 row affected (0.00 sec)


mysql> grant usage on *.* to wso2carbon@'%' identified by 'wso2carbon';

Query OK, 0 rows affected (0.00 sec)


mysql> grant all privileges on api_mgt.* to wso2carbon@'%';

Query OK, 0 rows affected (0.00 sec)


mysql> grant all privileges on api_grg.* to wso2carbon@'%';

Query OK, 0 rows affected (0.00 sec)


```



For the most part the APM and GREG nodes, when started the first time (with a special switch of -Dsetup) will create the necessary tables for each of those databases with the exception of the api_mgr table.  There is a script in the {APM_NODE}/dbscripts/apimgt directory named mysql.sql that will create the api_mgr tables.  Thus, from the command line (shell) switch to the {APM_NODE}/dbscripts/apimgt directory, then connect to mysql and run the following commands:


```sh

$ mysql -uroot -ppassword

mysql> \u api_mgt

mysql> \. mysql.sql


```


That will 1. log you into mysql as root (using default authorization credentials) 2. tell mysql to use the api_mgt database and 3. execute the mysql.sql script in the current directory ({APM_NODE/dbscripts/apimgt}). Once the script is completed you'll have the following tables



```
+-------------------------------+

| table_name                    |

+-------------------------------+

| AM_API                        |

| AM_API_LC_EVENT               |

| AM_APPLICATION                |

| AM_APPLICATION_KEY_MAPPING    |

| AM_SUBSCRIBER                 |

| AM_SUBSCRIPTION               |

| AM_SUBSCRIPTION_KEY_MAPPING   |

| IDN_BASE_TABLE                |

| IDN_OAUTH1A_ACCESS_TOKEN      |

| IDN_OAUTH1A_REQUEST_TOKEN     |

| IDN_OAUTH2_ACCESS_TOKEN       |

| IDN_OAUTH2_AUTHORIZATION_CODE |

| IDN_OAUTH_CONSUMER_APPS       |

+-------------------------------+


```


TIP: That list of tables was aquired with the query:



```sql
 SELECT table_name FROM information_schema.tables WHERE table_schema = 'api_mgr';


```


Later, after ALL the configuration is done, we will be starting the keymanager APM node and the GREG node with the switch -Dsetup which will create the the necessary tables in the other three databases.



### Setting up the Governance Registry (GREG)


Overall setting the GREG up and getting it running is pretty straight forward.  We just have to edit a couple files before we start it up.



#### Define your Datasources


In order to define the datasources you need to edit the file at {GREG_ROOT}/repository/conf/datasources/master-datasources.xml.  There are some sample configuration values in there which you'll be editing as well as adding a new one.



##### WSO2_CARBON_DB


This is the datasource that will point at the api_grg database we created earlier.



```xml
        <datasource>

            <name>WSO2_CARBON_DB</name>

            <description>The datasource used for registry and user manager</description>

            <jndiConfig>

                <name>jdbc/WSO2CarbonDB</name>

            </jndiConfig>

            <definition type="RDBMS">

                <configuration>

                    <url>jdbc:mysql://{MYSQL_IP_ADDRESS}:3306/api_grg?autoReconnect=true&amp;relaxAutoCommit=true</url>

                    <username>wso2carbon</username>

                    <password>wso2carbon</password>

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


NOTE: Every mysql datasource you define will need to have the ?autoReconnect=true&amp;relaxAutoCommit=true arguments included.  If you forget them you'll see all sorts of errors later about how the database couldn't commit something that is already committed.  Also note the &amp; part has to be encoded because it is in an XML file.


Now that the datasources are defined you're almost done configuring the GREG.  The WSO2_CARBON_DB changes will be picked up automatically.


Now, we need to set the "port offset" so that you minimize the risk of having one WSO2 node conflict with another that ends up being on the same server.  For the case of these examples we will use an offset value in the 40's.  To set the offset go to {GREG_ROOT}/repository/conf/carbon.xml and find the node titled Ports.  A subnode of that is Offset; change it like so:


```xml

    <Ports>


        <!-- Ports offset. This entry will set the value of the ports defined below to

         the define value + Offset.

         e.g. Offset=2 and HTTPS port=9443 will set the effective HTTPS port to 9445

         -->

        <Offset>49</Offset>

        ...


```


I set the GREG offset to be at the end of the 40's and I will use the lower part of the 40's for the APM nodes.

There is just one last step - the GREG needs to have clustering turned on (even if it is the only GREG node). To turn on clustering edit {GREG_HOME}/repository/conf/axis2/axis2.xml:



```xml
    <clustering class="org.apache.axis2.clustering.tribes.TribesClusteringAgent" enable="true">


```


At this point the GREG is setup.  You can start it by going to the {GREG_ROOT}/bin directory then running the setup script appropriate for your platform.




```sh

$ cd {GREG_HOME}/bin

$ ./wso2server.sh -Dsetup


```


NOTE: In the future if you have to restart it make sure you don't use the -Dsetup switch.


NOTE: If you get errors about being unable to connect to the database server refer to[ this article on enabling remote access to mysql server](http://www.cyberciti.biz/tips/how-do-i-enable-remote-access-to-mysql-database-server.html).



### APM Setup


When all is said and done you'll have four APM nodes created but I suggest you just start with one.  We have to do some identical configuration on each of them so this way you can just do some changes to one node, then copy it three more times thus saving you from having to edit the same files in each node.  This initial node I'll refer to as APM_NODE and it's root directory as {APM_NODE_ROOT}.



#### Setting up the databases


Just like with the GREG we have to edit the {APM_NODE_ROOT}/repository/conf/datasources/master-datasources.xml file.  First off just leave the WSO2_CARBON_DB alone - it points to an H2 database.  We will just let it continue to do so.  It doesn't matter that each of the nodes will point to separate H2 databases.


We need to update the WSO2_AM_DB to point to our api_mgr database:



```xml
        <datasource>

            <name>WSO2AM_DB</name>

            <description>The datasource used for API Manager database</description>

            <jndiConfig>

                <name>jdbc/WSO2AM_DB</name>

            </jndiConfig>

            <definition type="RDBMS">

                <configuration>

                    <url>jdbc:mysql://{MYSQL_IP_ADDRESS}:3306/api_mgt?autoReconnect=true&amp;relaxAutoCommit=true</url>

                    <username>wso2carbon</username>

                    <password>wso2carbon</password>

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


And lastly we need to create a WSO2_GREG_DB datasource that points to the api_grg database:



```xml
        <datasource>

            <name>WSO2_GREG_DB</name>

            <description>The datasource used for registry </description>

            <jndiConfig>

                <name>jdbc/WSO2_GREG_DB</name>

            </jndiConfig>

            <definition type="RDBMS">

            <configuration>

                    <url>jdbc:mysql://{MYSQL_IP_ADDRESS}:3306/api_grg?autoReconnect=true&amp;relaxAutoCommit=true</url>

                    <username>wso2carbon</username>

                    <password>wso2carbon</password>

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


Honestly, the name you use for the WSO2_GREG_DB isn't that important so long as it is unique within that file. Just make it something recognizable for it's purpose. At this point all of our datasources are defined so we need to put them into affect.

We need to update the user-mgt.xml file in {APM_NODE_ROOT}/repository/conf/user-mgt.xml because we are storing our user information in the shared GREG database.



```xml

        <Configuration>

                <AdminRole>admin</AdminRole>

                <AdminUser>

                     <UserName>admin</UserName>

                     <Password>admin</Password>

                </AdminUser>

            <EveryOneRoleName>everyone</EveryOneRoleName> <!-- By default users in this role sees the registry root -->

            <Property name="dataSource">jdbc/WSO2_GREG_DB</Property>

            <Property name="MultiTenantRealmConfigBuilder">org.wso2.carbon.user.core.config.multitenancy.SimpleRealmConfigBuilder</Property>

        </Configuration>


```




Just as an FYI - the GREG database looks like this:


```
+-----------------------+




| TABLES                |

+-----------------------+

| REG_ASSOCIATION       |

| REG_CLUSTER_LOCK      |

| REG_COMMENT           |

| REG_CONTENT           |

| REG_CONTENT_HISTORY   |

| REG_LOG               |

| REG_PATH              |

| REG_PROPERTY          |

| REG_RATING            |

| REG_RESOURCE          |

| REG_RESOURCE_COMMENT  |

| REG_RESOURCE_HISTORY  |

| REG_RESOURCE_PROPERTY |

| REG_RESOURCE_RATING   |

| REG_RESOURCE_TAG      |

| REG_SNAPSHOT          |

| REG_TAG               |

| UM_CLAIM              |

| UM_CLAIM_BEHAVIOR     |

| UM_DIALECT            |

| UM_HYBRID_REMEMBER_ME |

| UM_HYBRID_ROLE        |

| UM_HYBRID_USER_ROLE   |

| UM_PERMISSION         |

| UM_PROFILE_CONFIG     |

| UM_ROLE               |

| UM_ROLE_PERMISSION    |

| UM_TENANT             |

| UM_USER               |

| UM_USER_ATTRIBUTE     |

| UM_USER_PERMISSION    |

| UM_USER_ROLE          |

+-----------------------+


```


The tables prefixed with REG are registry tables.  The tables prefixed with UM are user management tables.


Next we need to tie the GREG into the APM node.  To do that we have to edit the {APM_NODE_ROOT}/repository/conf/registry.xml.  There are three xml nodes we will be adding; I put them right near the top just after the opening wso2registry tag.



```xml
    <dbConfig name="mounted_registry">

        <dataSource>jdbc/WSO2_GREG_DB</dataSource>

    </dbConfig>


    <remoteInstance url="https://{GREG_HOST_IP}:9492/registry">

                    <id>instanceid</id>

                    <dbConfig>mounted_registry</dbConfig>

                    <readOnly>false</readOnly>

                    <enableCache>true</enableCache>

                    <registryRoot>/</registryRoot>

    </remoteInstance>


    <mount overwrite="true" path="/_system/governance">

                <instanceId>instanceid</instanceId>

                <targetPath>/_system/governance</targetPath>

    </mount>


```



Some online tutorials will havea  mount for /_system/config - don't include that.  It is a holdover from where the API Manager is based on the WSO2 ESB.  The API Manager doesn't share config info between nodes. It is possible that including the config node could cause problems.


You'll notice that I have the port number of 9492 listed in that example. That is based on you using the OFFSET value of 49 that I mentioned in the GREG setup example above.  If you used a different offset value you'll need to figure out the port.  The easiest way is to start the GREG and, when it is done starting look for a line like this:



```sh
 INFO {org.wso2.carbon.ui.internal.CarbonUIServiceComponent} -  Mgt Console URL  : https://GREG_IP_ADDRESS:9492/carbon/


```


The port that the console is available on is the same port the registry is available on.

At this point you've done all the generic setup we can do on the APM nodes.  So it's time to copy the node in order to create the various nodes we need.



```sh
$ cp -r node store

$ cp -r node publisher

$ cp -r node gateway

$ cp -r node keymanager


```




### The Key Manager


Setting up the key manager is pretty straight forward.  We just have to edit a few configuration files.  The configuration files are all located in the {KEYMANAGER_HOME}/repository/conf directory (or subdirectories) so I'll refer to that directory as {KEY_CONF_HOME}.

First things first let's set the Port Offset to 41. To do that edit {KEY_CONF_HOME/carbon.xml like so:



```xml
        ...

    <Ports>


        <!-- Ports offset. This entry will set the value of the ports defined below to

         the define value + Offset.

         e.g. Offset=2 and HTTPS port=9443 will set the effective HTTPS port to 9445

         -->

        <Offset>41</Offset>

        ...


```


Next up we need to edit the {KEY_CONF_HOME}api-manager.xml file.  Basically just search for each of the nodes listed here and change them to the appropriate values:


```xml

    ...

    <SignatureAlgorithm>SHA256withRSA</SignatureAlgorithm>

    ...

    <EnableTokenGeneration>true</EnableTokenGeneration>

    ...

    <EnableKeyMgtValidationInfoCache>false</EnableKeyMgtValidationInfoCache>

    ...


```


Assuming you'll be putting these nodes in production the WSO2 folks advise you make the following changes as well.  First off we need to edit the {KEY_CONF_HOME}/axis2/axis2_client.xml file:


```xml

    ...

    <parameter name="defaultMaxConnPerHost">1000</parameter>

    <!-- commons-http-client maxTotalConnections -->

    <parameter name="maxTotalConnections">30000</parameter>

    ...


```


Then you need to edit {KEY_CONF_HOME}/tomcat/catalina-server.xml and change the following attributes of the Connector tag:


```sh

    maxThreads="750"

    minSpareThreads="150"

    disableUploadTimeout="false"

    connectionUploadTimeout="120000"

    maxKeepAliveRequests="600"

    acceptCount="600"


```


At this point the keymanager configuration is completed.  So let's start it up to make sure everything is kosher.  Plus, we can take this opportunity to use have it initialize the other two databases (api_usr and api_reg).  In order to start it go to the {KEYMANAGER_HOME}/bin and run the startup script:


```sh

$ cd {KEYMANAGER_HOME}/bin

$ ./wso2server.sh


```




### The Gateway


The gateway is responsible for handling all API requests, verifying the API key included in the request with the keymanager, and making sure the requestor has remaining quota left with the GREG and then finally passing the request tot he actual API endpoint, getting the response from the API endpoint,and sending that response back to the initial requester.  To set it up we will be editing the same files as we did the keymanager but with a few different modifications.

I'll refer to the {GATEWAY_HOME}/repository/conf directory as {GATEWAY_CONF}.  To start with we need to edit the {GATEWAY_CONF}/carbon.xml file to set the Port Offset.



##### Port Offset


```xml
        ...

    <Ports>


        <!-- Ports offset. This entry will set the value of the ports defined below to

         the define value + Offset.

         e.g. Offset=2 and HTTPS port=9443 will set the effective HTTPS port to 9445

         -->

        <Offset>42</Offset>

        ...


```


Honestly, even when I'm installing all of these things on different servers I'd do this - it isn't necessary but it gets me in the habit and that way I don't forget to change the Offset when I do install things on the same server.  You should probably keep a log file that is shared by your team/department of what component has what offset on what server for ALL of your WSO2 installs so that you don't end up creating a conflict inadvertently down the road.



##### API Manager Config File


Right off the bat we need to point the gateway at the keymanager; otherwise it can't verify key values that are passed to it.  To do this you'll need to edit {GATEWAY_CONF}/api-manager.xml.  After you make that change keep the file open as I'll discuss a few more changes:


```xml

    <APIKeyManager>

        <ServerURL>https://{KEYMANAGER_IP}:9484/services/</ServerURL>

        <Username>admin</Username>

        <Password>admin</Password>

        <EnableJWTCache>false</EnableJWTCache>

        <EnableKeyMgtValidationInfoCache>true</EnableKeyMgtValidationInfoCache>

        <KeyValidatorClientType>ThriftClient</KeyValidatorClientType>

        <ThriftClientPort>10397</ThriftClientPort>

        <ThriftClientConnectionTimeOut>10000</ThriftClientConnectionTimeOut>

        <ThriftServerPort>10398</ThriftServerPort>

        <EnableThriftServer>false</EnableThriftServer>

       <!-- <RemoveUserNameToJWTForApplicationToken>true</RemoveUserNameToJWTForApplicationToken>-->

    </APIKeyManager>


```


Your api-manager.xml file will have a bunch of comments in between the various settings. I just removed them to condense the values for display here.


NOTE: you MUST turn off the ThriftServer by setting the <EnableThriftServer> value to false.

NOTE: the port of 9484 used in the ServerURL is based on the keymanager having a Port Offset of 41.  If you didn't use 41 you can see the value in the terminal for your keymanager:


```sh

[2012-11-28 14:42:27,031]  INFO - CarbonUIServiceComponent Mgt Console URL  : https://198.183.217.190:9484/carbon/


```


Next up we need to enable the Gateway key cache in the APIGateway node:


```xml

    <APIGateway>

        <ServerURL>https://${carbon.local.ip}:${mgt.transport.https.port}/services/</ServerURL>

        <Username>admin</Username>

        <Password>admin</Password>

        <APIEndpointURL>http://${carbon.local.ip}:${http.nio.port},https://${carbon.local.ip}:${https.nio.port}</APIEndpointURL>

        <EnableGatewayKeyCache>true</EnableGatewayKeyCache>

    </APIGateway>


```


Basically, you're just changing the value of the "EnableGatewayKeyCache" tag in that cluster.  Leave everything else in the APIGateway section alone.  We will actually revisit that section when we configure the publisher and store nodes.

Because the gateway isn't responsible for some things, such as key security, you can comment out the sections titled  and .

The final tweak in this file is to set the SignatureAlgorithim:



```xml
    ...

    <SignatureAlgorithm>SHA256withRSA</SignatureAlgorithm>

    ...


```


In my experience the value is already SHA256withRSA but it is commented out; so just uncomment it.



##### Performance Tuning


At this point the gateway node is setup to act as a gateway but the WSO2 folks also have some production recommendations to improve performance.  These are similar to, if not identical to, the suggestions made earlier for the keymanager.  First off we edit the {GATEWAY_CONF}/axis2/axis2_client.xml file:


```xml

    ...

    <parameter name="defaultMaxConnPerHost">1000</parameter>

    <!-- commons-http-client maxTotalConnections -->

    <parameter name="maxTotalConnections">30000</parameter>

    ...


```


Next, we need to edit the {GATEWAY_CONF}/tomcat/catalina-server.xml:



```sh
    maxThreads="750"

    minSpareThreads="150"

    maxKeepAliveRequests="600"

    acceptCount="600"


```


You may notice that we didn't modify some of the same values we tweaked for the keymanager; that's okay - they serve different roles. Finally, we need to edit the {GATEWAY_CONF}/nhttp.properties file.


```sh

    http.socket.timeout=60000

    #http.socket.buffer-size=8192

    #http.tcp.nodelay=1

    #http.connection.stalecheck=0


    # Uncomment the following property for an AIX based deployment

    #http.nio.interest-ops-queueing=true


    # HTTP Sender thread pool parameters

    snd_t_core=200

    snd_t_max=250

    #snd_alive_sec=5

    #snd_qlen=-1

    snd_io_threads=16


    # HTTP Listener thread pool parameters

    lst_t_core=200

    lst_t_max=250

    #lst_alive_sec=5

    #lst_qlen=-1

    lst_io_threads=16


```


I've include the contents of my entire nhttp.properties file showing what is commented out as well (comments are prefixed with a #).

The gateway is now configured.  Feel free to start it up to make sure there are no syntax errors and so that it is ready for the store and publisher nodes we are about to put together:


```sh

$ cd {GATEWAY_HOME}/bin

$ ./wso2server.sh


```


NOTE: we didn't use the -Dsetup switch when starting this time.  Remember, after you've done it once you don't want to do it again as it will reinitialize your database.   Thus the next time you start the keymanager you shouldn't use that switch either.



### The Publisher


Setting up the publisher is pretty easy.  It's just a matter of telling that node where the keymanager and gateway are within the api-manager.xml file.  I'll call {PUB_HOME}/repository/conf {PUB_CONF} so go to {PUB_CONF}/api-manager.xml and make the following changes:


```xml

    <AuthManager>

        <ServerURL>https://{KEYMANAGER_IP}:9484/services/</ServerURL>

        <Username>admin</Username>

        <Password>admin</Password>

    </AuthManager>


```


The keymanager is actually serving two roles in the overall installation.  The first role is to provide login authentication to the various Carbon applications (including the Jaggery based front-end for the publisher and store).  The second is to generate and validate API keys; which is initiated within the store. This change tells the publisher to log people in via the keymanager.  Next we tell the publisher about the Gateway:


```xml

    <APIGateway>

        <ServerURL>https://{GATEWAY_IP}:9485/services/</ServerURL>

        <Username>admin</Username>

        <Password>admin</Password>

        <APIEndpointURL>http://${carbon.local.ip}:${http.nio.port},https://${carbon.local.ip}:${https.nio.port}</APIEndpointURL>

        <EnableGatewayKeyCache>false</EnableGatewayKeyCache>

    </APIGateway>


```


The publisher really only cares about the ServerURL, Username, and Password values.  Basically, after you create an API in the publisher you can change the API status from CREATED to PUBLISHED or BLOCKED (or a couple other values).  When you make these "lifecycle" changes you can have the publisher push the change information to the gateway.  Remember, the port associated with the {GATEWAY_IP}, 9485, is based on an offset of 42 and can be found in the gateway terminal like so:


```sh

[2012-11-29 09:01:42,295]  INFO - CarbonUIServiceComponent Mgt Console URL  : https://{GATEWAY_IP}:9485/carbon/


```





Next up, comment out the APIKeyManager section. The publisher doesn't this part at all.  At a minimum set **EnableThirftServer **to false.  If you don't it will conflict with the keyserver and you'll have problems.


There is just one more thing we have to do - change the Port Offset! Don't forget this step!.  Jump into the {PUB_CONF}/carbon.xml file and change it:



```xml
        ...

    <Ports>


        <!-- Ports offset. This entry will set the value of the ports defined below to

         the define value + Offset.

         e.g. Offset=2 and HTTPS port=9443 will set the effective HTTPS port to 9445

         -->

        <Offset>43</Offset>

        ...


```


Optionally, can remove the store jaggery app so that any attempts to access this node as a store will redirect to the carbon management console. To do this you would go to the {PUBLISHER_HOME}/repository/deployment/server/jaggeryapps and delete the store directory:


```sh

$ cd {PUBLISHER_HOME}/repository/deployment/server/jaggeryapps

$ rm -Rf store


```


Now you're ready to start the publisher:


```sh

$ cd {PUBLISHER_HOME}/bin

$ ./wso2server.sh


```




### The Store


We have reached the final node for configuration.  Let's start by setting the Port Offset in {STORE_CONF}/carbon.xml:



```xml
        ...

    <Ports>


        <!-- Ports offset. This entry will set the value of the ports defined below to

         the define value + Offset.

         e.g. Offset=2 and HTTPS port=9443 will set the effective HTTPS port to 9445

         -->

        <Offset>44</Offset>

        ...


```


The only other file we need to edit for the store is the api-manager.xml file at {STORE_CONF}/api-manager.xml.  First we need to tell the store where the keymanager is for the purpose of logging in:

```xml


    <AuthManager>

        <ServerURL>https://{KEYMANAGER_IP_ADDRESS}:9484/services/</ServerURL>

        <Username>admin</Username>

        <Password>admin</Password>

    </AuthManager>


```


Next we need to identify the keymanager again but this time for the purposes of generating API keys:


```xml

    <APIKeyManager>

        <ServerURL>https://{KEYMANAGER_IP_ADDRESS}:9484/services/</ServerURL>

        <Username>admin</Username>

        <Password>admin</Password>

        <EnableJWTCache>false</EnableJWTCache>

        <EnableKeyMgtValidationInfoCache>false</EnableKeyMgtValidationInfoCache>

        <KeyValidatorClientType>ThriftClient</KeyValidatorClientType>

        <ThriftClientPort>10397</ThriftClientPort>

        <ThriftClientConnectionTimeOut>10000</ThriftClientConnectionTimeOut>

        <ThriftServerPort>10398</ThriftServerPort>

        <EnableThriftServer>false</EnableThriftServer>

       <!-- <RemoveUserNameToJWTForApplicationToken>true</RemoveUserNameToJWTForApplicationToken>-->

    </APIKeyManager>


```


NOTE: you MUST turn off the ThriftServer by setting the <EnableThriftServer> value to false.

The final configuration step is to tell the store where the gateway is - that is done like so:



```xml
    <APIGateway>

        <ServerURL>https://{GATEWAY_IP_ADDRESS}:9485/services/</ServerURL>

        <Username>admin</Username>

        <Password>admin</Password>

        <APIEndpointURL>http://{GATEWAY_IP_ADDRESS}:8322,https://{GATEWAY_IP_ADDRESS}:8285</APIEndpointURL>

        <EnableGatewayKeyCache>false</EnableGatewayKeyCache>

    </APIGateway>


```


When doing this you might notice I changed the APIEndpointURL as well to point to the gateway as well as some different looking port numbers.  When the gateway starts up there are a couple of log messages that look like this:



```sh
[2012-11-29 09:01:39,063]  INFO - HttpCoreNIOListener HTTPS Listener started on port : 8285

[2012-11-29 09:01:39,115]  INFO - HttpCoreNIOListener HTTP Listener started on port : 8322


```


These tell us what ports the gateways is listening on for API requests.  Basically, any app that uses the API will end up calling the gateways IP at the appropriate port (based on HTTP or HTTPS needs) along with some form of API path in the url to identify the API being called.  If you had a load balancer in front of a bunch of gateway nodes you'd set the APIEndPointURL value to your load balancer's IP address and use the ports you've mapped in your load-balancer that point to the correct protocol (http or https).

At this point you've finished the required configuration for your store. You can optionally remove the publisher jaggery app so that people don't try to access the publisher on your store node.:



```sh
$ cd {STORE_HOME}/repository/deployment/server/jaggeryapps

$ rm -Rf publisher


```


Now you're ready to start the store!


```sh

$ cd {STORE_HOME}/bin

$ ./wso2server.sh


```


If you made it this far then congratulations.  You should now have four APM nodes running; a gateway, a keymanager, a publisher, and a store.  All of which are being governed by a Remote Governance Registry (GREG).  While none of these changes were hard to make there were a lot of them to make and thus plenty of opportunities to miss something.  If one of your nodes isn't working check the Port Offset and then check each of the xml files you edited to make sure there are no syntax errors.


NOTE: If, after trying to load the store in your browser, you see a bunch of errors in the corresponding terminal relating to executing queries against the remote governance registry try the following steps to fix them:




1. Make sure the GREG has the same instance ID in all of your nodes and that no other installation of the WSO2 components has the same GREG instance ID name.

2. comment out the GREG parts of the {STORE_HOME}/repository/conf/registry.xml file; then start the store with the -Dsetup option.  Then stop the store, uncomment the GREG section of the registry.xml and then restart the store without the -Dsetup option













