---
layout: post
title: "Installing CF8 and CF9 side by side on Apache 2.x"
date: 2011-02-18
comments: false
categories:
 - coldfusion
 - jrun
 - cf8
 - cf9
---
I have a bit of a conundrum; I have some clients who use CF8 some who use CF9
(and yes, some who still use CF 6 and 7). However, for the most part I only
have to do regular work for those clients who use either CF8 or CF9. The
trouble is I only have one development machine and I need to have both CF8 and
CF9 installed in parallel in such a way that I can easily switch between the
two servers when I switch project contexts. The following will explain how I
set this up on my Windows XP machine and it borrows heavily from [a
presentation I found at CF Goth Chic's
website](http://www.cfgothchic.com/blog/post.cfm/presentation-installing-
multiple-versions-of-coldfusion-together).

Before you begin I suggest you just uninstall any copy of CF you already have
setup.  Before I did that I created a Coldfusion Archive that contained all of
my existing datasources and mappings so I could quickly replicate them later.
If you don't know how to create or deploy a coldfusion archive I suggest you
check the CF documentation.  Even without it you can probably guess your way
though the process.  I only included the datasources and mappings in mine but
you may want to back even more stuff up.


Ok, now on to the meat of the operation:



1. Install Coldfusion 9 first.  You want to begin with the newest version so that you have the latest version of the Java Runtime to work with.
  1. As you install you'll want to pick "Enterprise Multiserver Configuration"
  2. Also make sure you select "Use Built In Webserver, Development Only"
    2. Once the install has completed let the installer open the "Configuration Wizard"
    3. Once the Configuration Wizard finishes open the CF Administrator for your install at <http://127.0.0.1:8300/CFIDE/administrator/index.cfm>
    4. Inside the CF Admin Expand the "Enterprise Manager" option in the left menu and select Instance Manager
    5. Create a New Instance
      1. Server Name: CF9
      2. Server Directory will auto-populate
      3. Select "Create Windows Service"
      4. Deselect "Auto Start Service"
      5. Click Submit - this part will take a while; sit back and browse [Reddit ](http://www.reddit.com/)or something while you wait.
      6. Once the setup was done you can visit the CF Admin for your new instance at http://127.0.0.1:8301/CFIDE/administrator  once here you can deploy your Coldfusion Archive if you created one.
2. Install Coldfusion 8
  1. This is a little more tricky.  Pick the J2EE configuration  "EAR" file
  2. Enter the context root of /
  3. Use the default for every other option; if you deviate from the defaults make a note of your changes and apply them as necessary in the later steps.
    1. I provided the same admin and rds passwords I used in the CF9 installation.
  8. Go back to the CF9 admin at <http://127.0.0.1:8300/CFIDE/administrator/index.cfm> and define a second instance under the "Enterprise Manager"
    1. ServerName: CF8
    2. Server Directory will auto-populate
    3. Create for EAR/WAR (optional) - enter the path to your newly created EAR file (C:\Coldfusion8\cfusion.ear is the default)
    4. Select "Create Windows Service"
    5. Deselect "Auto Start Service"
    6. Click submit - again this will take a while - read the news at [newsvine](http://newsvine.com/) and relax.
      9. Once this step is done you can vist the CF Admin for this instance at http://127.0.0.1:8302/cfide/administrator
      10. At this point you're just about done.  We just have to make some apache configuration changes.  So first off go to /JRUN4/bin/wsconfig.exe and setup either your cf8 or cf9 server with your apache install.  This will do a couple things.  1\. It will put the default jrun statements in your apache conf file and it will setup the jrun apache module under /jrun4/lib/wsconfig/1/
      11. next in /jrun4/lib/wsconfig create two directories   one called cf9 and the other cf8
      12. now go to your apache conf file and search for JRUN and you'll find something like this



```conf
    <IfModule mod_jrun20.c>

    JRunConfig Verbose false

    JRunConfig Ignoresuffixmap false

    #JRunConfig Errorurl url <optionally redirect to this URL on errors>

    #JRunConfig ProxyRetryInterval 600 <number of seconds to wait before trying to reconnect to unreachable clustered server>

    #JRunConfig ConnectTimeout 15 <number of seconds to wait on a socket connect to a jrun server>

    #JRunConfig RecvTimeout 300 <number of seconds to wait on a socket receive to a jrun server>

    #JRunConfig SendTimeout 15 <number of seconds to wait on a socket send to a jrun server>


 JRunConfig Apialloc false

 JRunConfig Serverstore "C:/dev/tools/JRun4/lib/wsconfig/cf9/jrunserver.store"

 JRunConfig Bootstrap 127.0.0.1:51000

 AddHandler jrun-handler .jsp .jws .cfm .cfml .cfc .cfr .cfswf

</IfModule>


```



I've actually edited it a little to make those last four lines stand out.    The 51000 is the port that CF9's proxy is listening on.  Basically that is how APACHE talks to JRUN and CF9.  If you have a virtual server setup that you want to use your CF8 install you'd just put the following code inside your virtual server node of the conf file:


```conf
    <IfModule mod_jrun20.c>

 JRunConfig Apialloc false

 JRunConfig Serverstore "C:/dev/tools/JRun4/lib/wsconfig/cf8/jrunserver.store"

 JRunConfig Bootstrap 127.0.0.1:51002

 AddHandler jrun-handler .jsp .jws .cfm .cfml .cfc .cfr .cfswf

</IfModule>


```



Note that both the serverstore was updated to point to /cf8/...  and the BootStrap port was switched to 51002.



NOTE:  If you try to hit a site that is configured for CF8 at this point and it fails with the following error messages in your site.log:




Couldn't initialize from remote server, JRun server(s) probably down.

```sh
  JRun will not accept request.  Check JRun web server configuration and JRun mappings on JRun server.


```


You'll want to check the following things.




  1. First look in your /jrun4/servers/cf8/server-inf/jrun.xml file down near line 377 and make sure the deactivated value is "false".  It probably is.
  2.  You'll then want to go to the JRUN management console at http://localhost:8000 - login with your cfadmin username and password.
  3. Expand the cf8 server node in the left menu and then click on "services" in the right panel you should see "ProxyService" and the status will probably say "Initialized"  That's the problem, it needs to say "Running"
  4. Click on the "Play" icon under "Actions" beside ProxyService.. Once that starts you should be able to load your CF8 site without any problems.
