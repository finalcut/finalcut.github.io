---
layout: post
title: "CruiseControl and Selenium with Coldfusion"
date: 2008-12-17
comments: false
categories:
 - continuous-integration
 - cruisecontrol
 - ant
 - selenium
 - mxunit
---
If you've been paying attention you'll know I've been getting a decent
continuous build process in place for a CF project. So far I've been using
mxunit, cruise control, ant, and subversion to get things going. The project
uses ModelGlue and ColdSpring 1.2.  
  
My small team (2 of us) have been doing a good job of getting quality unit
testing code coverage but we didn't have any automated user interface testing
in place until a couple of weeks ago when I finally found some time to look
into [Selenium](http://seleniumhq.org/).  
  
The first thing we did was install the Firefox plugin for Selenium. This
seemed like the quickest and easiest way for us to start defining some tests
and it works like a charm. We haven't had to manually write any tests yet as
the plugin is working pretty well. However, the plugin's utility ends as soon
as writing tests is done. In order to run the tests automatically as part of
our build process we had to do a few things.  
  

### Selenium Core

  
We had to install Selenium Core on the testing webserver. This was pretty
straight forward and shouldn't require any special instructions from me. Once
you have it installed just remember the path to the "tests" directory because
that will be required when we try to run the tests remotely.  
  

### Selenium Remote Control

  
Selenium Remote control comes with an Ant task. The most recent version won't
work with FF 3. Once you have the newest Selenium RC you'll need to put it's
jar file in your ant lib directory on your build server (makes life easier).
Then you'll just need to add a few new lines to your build.xml to make it
available to you.  
  

    
    
      
     <taskdef resource="selenium-ant.properties">  
      <classpath>  
       <pathelement location="selenium-server.jar"/>  
      </classpath>  
     </taskdef>  
    ```
      
      
    
    
    ### Tying it Together
    
      
      
    All of my UI tests are defined in a subdirectory of my project.  I've broken that subdirectory down into additional directories to help organize them based on the portion of the site the tests relate to.  However, when the tests are run they have to end up in the Selenium Core "tests" directory.  Thus I have defined an ant task to clean out the test directory and then in each of my ant tasks for running a directory of UI tests I first copy the tests over to the tests directory.  Here is an example:  
      
    
    
    
      
     <target name="uspsAuditUITests" depends="deleteUITests, createUITestLogginDirectory">  
      <copy todir="${uitests.testdir}">  
        <fileset dir="${uitests.srcdir}usps/auditTests/" />  
      </copy>  
        
      <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">  
       <testcase name="lb2.uitests.usps.auditTests.setup" packageName="lb2.uitests.usps.auditTests.setup" />  
      </mxunittask>  
      
      <selenese   
       suite="${uitests.srcdir}usps/auditTests/uspsTestSuite.html"  
       browser="*firefox"  
       results="${uitests.resultsdir}uiTestResults.html"  
       multiWindow="false"  
       timeoutInSeconds="900"  
       startURL="http://${uitests.server}" />  
      
      <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">  
       <testcase name="lb2.uitests.usps.auditTests.tearDown" packageName="lb2.uitests.usps.auditTests.setup.tearDown" />  
      </mxunittask>  
        
      <antcall target="deleteUITests" />  
      <antcall target="displayUITestResults" />  
     </target>  
    ```
      
      
    You might notice a bit of an mxunit kludge in there.  Basically, what I'm doing is creating a simple mxunit test to be run simply to clean up behind the UI test.  Some of the UI tests actually create data in the site and the mxunit teardown seemed like a good way to undo those changes when all was done.  A nice bonus is if something goes wrong with the cleanup my test will fail and I'll be notified.  
      
    That's it.  Overall it was pretty darn simple.  There are some caveats to how I'm doing things though and the foremost is that I'm only testing against FF 2.x automatically.  I should be testing against many browsers but for the time being this is what I have and it is better than nothing.  
      
    My tests only work in Firefox 2 due to the fact that we are using the Selenium IDE I guess.  Some of them might work in other browsers but so far we have definitely run into some problems executing the tests in IE.  
      
      
    
    
    ### Acknowledgements
    
      
    Thanks to [this post](http://www.henke.ws/post.cfm/Coldfusion-with-Selenium-ant-script) by Mike Henke I was able to get this all running fairly quickly with only a few small changes.
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    Bill
    
    
    
    
    
    One thing missing from this tutorial is getting the selenium results to actually show up in the build log email.  I'm still trying to get that to work.    
      
    This is the only reference I've found so far: http://wiki.openqa.org/display/SEL/Adding+nice+selenium-results+to+build+report  but cruisecontrol doesn't seem to merge my selenium results with the build log so, so far, the xsl isn't finding anything to transform.
    
    
    
    
    
    
    
    
    

