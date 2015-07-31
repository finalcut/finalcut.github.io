---
layout: post
title: "CF 8, CF9, and CF 10 all on the same apache server!"
date: 2013-01-24
comments: false
categories:
 - coldfusion
 - cf8
 - cf10
 - apache
 - cf9
 - cf
---
Today I had the seemingly unfortunate task of adding CF10 to my webserver
while continuing to keep CF 8 and CF 9 running on it.  Before you install CF
10 first follow my [prior post instructions on getting CF 8 and 9 working
together with Apache](http://code.rawlinson.us/2011/02/installing-cf8-and-cf9-side-by-side-on.html).

Once you have that working you just have to install CF10 - I installed to
c:\dev\tools\ColdFusion10.  I told it to automatically connect to my apache
server.  Then, once it was done I had to do a couple tweaks.

First off, I removed the following lines from my httpd.conf:


```apache

        #JRunConfig Errorurl url

        #JRunConfig ProxyRetryInterval 600

        #JRunConfig ConnectTimeout 15

        #JRunConfig RecvTimeout 300

        #JRunConfig SendTimeout 15



        JRunConfig Apialloc false

        JRunConfig Serverstore "C:/dev/tools/JRun4/lib/wsconfig/cf9/jrunserver.store"

        JRunConfig Bootstrap 127.0.0.1:51000

        AddHandler jrun-handler .jsp .jws .cfm .cfml .cfc .cfr .cfswf


```




If I left those in there CF got a little confused my CF 10 stuff wouldn't work properly.  So take those out.   Also, note, to get all of this to work you pretty much have to be using Virtual Hosts.  Thus, if you had a virtual host already defined that was talking to CF 9 then you'll need to add these four lines into those virtual hosts:


```apache
        JRunConfig Apialloc false

        JRunConfig Serverstore "C:/dev/tools/JRun4/lib/wsconfig/cf9/jrunserver.store"

        JRunConfig Bootstrap 127.0.0.1:51000

        AddHandler jrun-handler .jsp .jws .cfm .cfml .cfc .cfr .cfswf


```




Next up, create a virtual host that will be using CF 10.  You don't have to use a different port; you can still use port 80.


Here is an example virtual host that uses CF 10 and exposes the CF 10 administrator:


```apache
#wcs_10

<VirtualHost 127.0.0.1:80>

    DocumentRoot "c:/dev/websites/cften/site/"

    ServerAdmin www.cften.com

    ServerName cften

    ServerAlias *.cften

    ErrorLog c:/dev/websites/cften/log/server.log

DirectoryIndex index.html index.shtml index.php default.htm default.html index.cfm



    <Directory "c:/dev/websites/cften/site">

DirectoryIndex index.html index.shtml index.php default.htm default.html index.cfm

          Options ExecCGI FollowSymLinks

          AllowOverride all

          Allow from all

          Order allow,deny

    </Directory>


        Alias /mxunit /dev/tools/mxunit

        <Directory /dev/tools/mxunit>

        Order allow,deny

        Allow from all

        </Directory>


    # Where to find workers.properties

    JkMountFile "C:\dev\tools\ColdFusion10\config\wsconfig\1\uriworkermap.properties"

    # Select the timestamp log format

    JkLogStampFormat "[%a %b %d %H:%M:%S %Y] "

    AddHandler jakarta-servlet .cfm .cfml .cfc .cfr .cfswf


    Alias /CFIDE "C:\dev\tools\ColdFusion10\cfusion\wwwroot\CFIDE"

    <Directory  "C:\dev\tools\ColdFusion10\cfusion\wwwroot\CFIDE">

      Options Indexes FollowSymLinks

      AllowOverride None

      Order allow,deny

      Allow from all

    </Directory>


</VirtualHost>


```




Finally, go to your apache/conf directory and edit the mod_jk.conf file - you're basically removing a bunch of lines so that your file ends up looking like this:


```apache
# Load mod_jk module

LoadModule    jk_module  "C:\dev\tools\ColdFusion10\config\wsconfig\1\mod_jk.so"

JkWorkersFile "C:\dev\tools\ColdFusion10\config\wsconfig\1\workers.properties"

# Where to put jk logs

JkLogFile "C:\dev\tools\ColdFusion10\config\wsconfig\1\mod_jk.log"

# Where to put jk shared memory

JkShmFile "C:\dev\tools\ColdFusion10\config\wsconfig\1\jk_shm"

# Set the jk log level [debug/error/info]

JkLogLevel info

<Files ~ ".hbmxml$">

Order allow,deny

Deny from all

</Files>


```




Then, restart apache and boom! You'll be all set.  CF8, CF9, and CF10 all will be working along side each other.  To test it you can put a file like this in the root of your different virtual servers and hit them and see what is reported back:


```cfc

<cfdump var="#server.coldfusion.productversion#">


```




Hat tip to <http://kmaiya.blogspot.in/2012/04/co-existence-of-coldfusion9-and.html>  for pointing me in the right direction for getting CF10 working.
