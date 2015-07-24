---
layout: post
title: "MxUnit and Custom Mappings"
date: 2010-05-06
comments: false
categories:
 - coldfusion
 - custom-mappings
 - mxunit
---
Try to imagine a scenario where you need two copies of the same CF application
running on your dev machine at the same time but both copies aren't exactly
the same. However, both need to use the same mapping value; for argument sake
we'll call the mapping "wcs" Now, also imagine that the production copy of the
application is using an application.cfm not an application.cfc so you can't
use application specific mappings. How do you test your components using a
great tool like mxunit?  
  
Well, it turns out there is a way. It just took some effort to figure it out.
The first thing I did, in the development branch (wcsdev) was to port the
application.cfm file to an application.cfc file so that at least the dev copy
could use application specific mappings. Doing this saved me from having to
have multiple instances of CF installed on my machine. However, in the cf
administrator I still need to keep the wcs mapping that points to wcsprod.
This causes some other problems that popup when running my unit tests in the
browser.  
  
To be honest, once I had the application specific mapping setup I thought I
was golden. But, when I tried to run a test, like: http://localhost/wcsdev/uni
ttests/com/some_component_tests.cfc?testMethod=testValidSSN&amp;method=runTest
Remote&amp;output=html I was given the error message "could not find the
component some_component_tests. I was a little perplexed. I did a little
digging and thought, well, maybe I need a custom remotefacade in my test root
so I put one in there that looks like this:  
  
```cfm <cfcomponent extends="mxunit.framework.RemoteFacade"
output="false">  
</cfcomponent>```  
  
Sadly, that didn't fix the problem either. After screwing around for a bit I
finally asked on the mxunit mailing list and Mike Rankin offered up this
nugget "Setting up separate websites, using virtual websites, on my
workstation." I use apache so creating these virtual websites was pretty easy.
First I updated my c:\windows\system32\drivers\etc\hosts file and then I
updated mdy httpd.conf file like so:  
  

    
    
    #wcs_prod  
    <VirtualHost 127.0.0.1>  
     DocumentRoot "c:/dev/websites/wcs_prod/site/"  
     ServerName wcsprod  
     ServerAlias *.wcsprod  
     ErrorLog c:/dev/websites/wcs_prod/log/server.log  
     <Directory "c:/dev/websites/wcs_prod/site">  
        Options ExecCGI FollowSymLinks  
        AllowOverride all  
        Allow from all  
        Order allow,deny  
     </Directory>  
      
            Alias /mxunit /dev/tools/apache2/htdocs/mxunit  
            <Directory /dev/tools/apache2/htdocs/mxunit>  
            Order allow,deny  
            Allow from all  
            </Directory>  
      
    </VirtualHost>  
      
    #wcs_dev  
    <VirtualHost 127.0.0.1>  
     DocumentRoot "c:/dev/websites/wcs_wcs_dev/site/"  
     ServerName wcsdev  
     ServerAlias *.wcsdev  
     ErrorLog c:/dev/websites/wcs_wcs_dev/log/server.log  
     <Directory "c:/dev/websites/wcs_wcs_dev/site">  
        Options ExecCGI FollowSymLinks  
        AllowOverride all  
        Allow from all  
        Order allow,deny  
     </Directory>  
      
            Alias /mxunit /dev/tools/apache2/htdocs/mxunit  
            <Directory /dev/tools/apache2/htdocs/mxunit>  
            Order allow,deny  
            Allow from all  
            </Directory>  
      
    </VirtualHost>```
      
      
    You'll notice I added a directory alias for mxunit to both virtual hosts.  I didn't actually do that at first but I ended up needing to later so just run with it.  
      
    At this point I just restarted Apache and everything seemed to be working wonderfully.  My tests were running fine in the browser and I was happy.  Well, I was happy until I decided to use my ant build file to run a full integration test before commiting some changes to wcsdev.  Then a bunch of tests failed with a 500 error being returned from the server.  The first problem was that I didn't have the alais to mxunit defined and the ant runner tries to go to http://wcsdev/mxunit/runner...   The second problem was related to my per-application mappings again.  Because the ant task runs the tests under the mxunit application my per-application mapping wasn't being recognized and thus, the server defined wcs mapping (that pointed to wcsprod) was being used.  When this happened my new components in wcsdev that were being tested couldn't be found and I got a 500 error.  
      
    To give you a little more background, before I give you my solution to that problem, I want you to know that I have an application.cfc in the root of wcsdev but then I have to have a second application.cfc in the wcsdev/unittests directory.  That's because the core application.cfc does some security checks and makes you login to the site including when you just try to load a unit test in the browser.  The unittest/application.cfc helps alleviate that and is a much lighter weight file in general.  It basically just defines my mapping and a couple of other little things (such as initializing coldspring).  
      
    ```cfm
    <cfcomponent  
     displayname="WARP"  
     output="true">  
      
      
    <cfset THIS.Name = "MXUnitFramework" />  
    <cfset THIS.ApplicationTimeout = CreateTimeSpan( 0, 0, 1, 0 ) />  
    <cfset THIS.SessionManagement= true />  
    <cfset THIS.mappings["/wcs"] = getDirectoryFromPath(getCurrentTemplatePath()) & "..\">  
      
      
      
    <cffunction  
     name="OnRequestStart"  
     access="public"  
     returntype="boolean"  
     output="false"  
     hint="Fires at first part of page processing.">  
      <!--- setup coldspring --->  
    ...  
      
      
    <cfreturn true />  
      
    </cffunction>  
      
    </cfcomponent>```
      
      
      
    Because I have this great, lightweight application.cfc sitting in my unittest directory I decided to add a new ant task that would copy that application.cfc to the mxunit root directory.  MxUnit uses a very simple Application.cfm and, if CF sees both files it uses the .cfc file in lieu of the .cfm file.  Thus, my ant task copies the .cfc file and then, when my tests are run, it deletes the appliation.cfc file from the mxunit directory.  
      
    However, I had to be a little creative and change my application.cfc file just a touch to get it to work.  My mapping path obviously wouldn't work since it was dependent on where the file was located on the file system.  Nor could I just do   
      
    ```cfm
    <cfset THIS.mappings["/wcs"] = ExpandPath("/wcs") \>```
      
      
    Because, the mapping stored in coldfusion server would win and I would have the same problem.  Thus I needed to define my mapping like this:  
      
    ```cfm
    <cfset THIS.mappings["/wcs"] = ExpandPath("/") & "/wcs" \>```
      
      
    At this point my unit tests were working fine in both the browser and from the ant task!   For those curious here are my ant tasks for copying and deleting the application.cfc file:  
      
    
    
    
     <target name="copyApplicationCfC" depends="deleteApplicationCfC">  
      <copy tofile="${mxunit.dir}/Application.cfc" file="${basedir}/unittests/application.cfc" />  
     </target>  
     <target name="deleteApplicationCfC">  
      <delete file="${mxunit.dir}/Application.cfc" />  
     </target>```
      
      
    EDIT:  THIS IS IMPORTANT!  
    I was approaching this from the wrong way in the solution I posted before.  While it works it is a hack and it's a stupid way to do it.  This hack was a result of me not really knowing what the hell I was doing.   
      
    Instead of having an ant task that copies your application.cfc over to the mxunit directory - you just need to make a couple small changes to your project.  
      
    
    
      1. copy the HttpAntRunner.cfc file from the mxunit/samples directory and put it in the root of your unittests directory.  This file will remain a part of your project.
      2. Update your ant file by defining a property named mxunit.runner with a value of "${application.name}/${test.dir}/HttpAntRunner.cfc
      3. Update all of your calls to the mxunittask to have the defaultrunner property set like so:  
    defaultrunner="${mxunit.runner}"
    
    Now you'll be using the right method and you'll be avoiding my stupid hackery.
    
    
    

