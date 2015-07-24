---
layout: post
title: "MxUnit and CruiseControl on Separate Machines"
date: 2008-10-16
comments: false
categories:
 - coldfusion
 - continuous-integration
 - cruisecontrol
 - unit-testing
 - coldspring
---
In my previous efforts over this week of getting Cruise Control working (for
Continuous Integration) I was doing it on my dev machine and testing against
my dev instance which, obviously, isn't an ideal situation. My Dev instance is
in flux while our Continuous Integration (CI) server should have the latest
checked in code only.  
  
The CI server was actually updating and maintaining a local copy of the files,
it was executing executing its local copy of the test cases, but the tests
were testing my dev copies of the production CFCs. What I needed to do was to
setup a dev webserver elsewhere and have my local CI server try to execute the
tests against that server.  
  
Overall this change was fairly easy but I made a few mistakes along the way so
I just figured I would detail my successful solution for anyone else
interested.  
  

### Build.xml

  
The first thing I did was break my ant Build.xml file up into three separate
ones. The first is the core build file and 95% of the targets stayed in it.
The other two, dev_build.xml and ci_build.xml set some environment specific
properties and call the fullTestSuite target a little differently.  
  
The main differences between the two are the setting of the host and
siteBaseDir which mxUnit needs based on the different types of tests being
run. Plus, in the dev_build.xml I update from svn before running the full test
suite (and sometimes before the others as well) while the ci_build already
gets updated by the CI task.  
  
I can't have the ci_build update from svn because ant doesn't access the
shared drive and using the d:\\... path causes the build to break in most
other targets other than the MxUnit ones.  
  

#### dev_build.xml

  

    
    
      
    <project name="Listbuilder USAF" default="runAllTests" basedir=".">  
       
       
     <import file="base_build.xml" />  
      
      
     <!-- PROPERTY DEFINITIONS -->  
     <property name="host" value="localhost" />  
     <property name="siteBaseDir" value="${basedir}" />  
      
      
      
     <!--- TEST SUITES -->  
      
     <target name="runAllTests" target="svnAntUpdate">  
      <antcall target="testWithReport" />  
     </target>  
      
     <target name="runBeanTests">  
      <antcall target="beanTests" />  
     </target>  
      
     <target name="runDaoTests">  
      <antcall target="daoTests" />  
     </target>  
      
     <target name="runGatewayTests">  
      <antcall target="gatewayTests" />  
     </target>  
    </project>  
    ```
      
    
    
    #### ci_build.xml
    
      
    
    
    
      
    <project name="Listbuilder USAF" default="testWithReport" basedir=".">  
       
       
     <import file="base_build.xml" />  
      
      
     <!-- PROPERTY DEFINITIONS -->  
     <property name="host" value="oak" />  
     <property name="siteBaseDir" value="d:\inetpub\wwwroot\listbuilder" />  
      
      
      
     <!--- TEST SUITES -->  
      
     <target name="runAllTests">  
      <antcall target="runFullTestSuite" />  
     </target>  
      
     <target name="runBeanTests">  
      <antcall target="beanTests" />  
     </target>  
      
     <target name="runDaoTests">  
      <antcall target="daoTests" />  
     </target>  
      
    </project>  
    ```
      
    
    
    ### Webserver
    
      
    Obviously I had to setup a new copy of my website on the dev server, create the proper mapping and datasource entry.  I didn't have to actually configure the site since, at the moment I don't have Selenium or anything working and my unit tests don't really need the site to work, they just need the components to be tested to be available.  I checked out a copy of the website on the dev box and then created a mapping to the server/drive for the dev machine that has the website on it.  
      
    
    
    ### CruiseControl Service
    
      
    I had to tell the **cruise control service on my machine to start as me** so that it could have access to the network drive that my dev machine is sharing.  Without this I couldn't have CruiseControl execute an ant task remotely to update the dev instance of the site.  
      
    To configure the service to start as a specific user I opened the Services Control Panel (Start -> Admin Tools -> Services), find the Cruise Control service, open it, go to the second tab (login) and provide the correct login information.  
      
    
    
    ### CruiseControl config.xml
    
      
    If you have been following my trials and tribulations you'll know i've run into some svn problems due to incompatiable clients.  The problem still exists if I try to use the CruiseControll svnbootstrapper task.  I just can't do it.  Fortunately I figured out a work around.  
      
    Under the schedule task there is a "composite" task that you can wrap a variety of build tasks in.  
      
    
    
    
      
       <composite>  
       <!-- becuase I can't use the svnbootstrapper (too old svn client version) I do this to work around it -->  
                <ant anthome="apache-ant-1.7.0" buildfile="projects\${project.name}build.xml" target="updateBuildFile" />  
       <!-- update our test server (oak) -->  
       <ant anthome="apache-ant-1.7.0" buildfile="\\oak\d$\inetpub\wwwroot\listbuilder\build.xml" target="svnAntUpdate" />  
       <!-- now do the real build -->  
                <ant anthome="apache-ant-1.7.0" buildfile="projects\${project.name}\ci_build.xml" target="testWithoutReport" />  
       </composite>  
    ```
      
      
    The first thing I do is update my local build file to make sure it is solid, then you'll notice that second ant build action is updating my remote site instance.  Finally the actual build happens.  All the logging still happens on my local CI instance and the final reports that are generated by CruiseControl are pretty nice and detailed.  
      
    
    
    ### build.xml
    
      
    Yeah, I already talked about this but my base build.xml file has some changes in it so that I am certain to get as useful of information as possible in my CI build reports.  
      
    
    
    #### Problems>
    
      
    Initially I had a target to test my beans, another to test my daos, another for gateways and so on.  Then my full test suite target would then "depend" on each of those targets.  The problem was the MxUnit logs were overwritten by each subsequent target and I ended up with insufficient information in the build report.  
      
    So then I started having a single target that would run the mxunit task on each directory (recursively) like so:  
    
    
    
      
     <target name="allUnitTests" depends="testSetup">  
        <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">  
       <directory path="${siteBaseDir}\unittests\model\bean" recurse="true" componentPath="lb2.unittests.model.bean" packageName="lb2.unittests.model.bean" />  
       <directory path="${siteBaseDir}\unittests\model\dao" recurse="true" componentPath="lb2.unittests.model.dao" packageName="lb2.unittests.model.dao" />  
      </mxunittask>    
     </target>  
    ```
      
      
    While this solved the problem of overwritten log files it created a new problem.  When a test failed in a specific CFC the report wasn't specific enough about the cfc that failed.  For instance, if the bean directory had a problem then the name of the test that failed would be identified but the class would be "bean" (the last part of the componentPath for the directory).  That makes debugging a broken build kind of difficult; especially if you have some generic tests that run on each object in that directory.  
      
    
    
    #### The Solution
    
      
    In order to get good, solid, precise reporting I had to use the testcase MxUnit task as follows:  
    
    
    
      
     <target name="runFullTestSuite" depends="testSetup">  
        <mxunittask server="${host}" verbose="false" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">  
       <!-- bean test cases -->  
             <testcase name="lb2.unittests.model.bean.clientCustomQuestionTest" packageName="lb2.unittests.model.bean.clientCustomQuestionTest" />  
             <testcase name="lb2.unittests.model.bean.clientRegionTest" packageName="lb2.unittests.model.bean.clientRegionTest" />  
             <testcase name="lb2.unittests.model.bean.facilityTest" packageName="lb2.unittests.model.bean.facilityTest" />  
      
       <!-- dao test cases -->  
             <testcase name="lb2.unittests.model.dao.customGuidanceTest" packageName="lb2.unittests.model.dao.customGuidanceTest" />  
             <testcase name="lb2.unittests.model.dao.regionTest" packageName="lb2.unittests.model.dao.regionTest" />  
      
        <!-- gateway tests -->  
             <testcase name="lb2.unittests.model.gateway.clientEMSGatewayTest" packageName="lb2.unittests.model.gateway.clientEMSGatewayTest" />  
        </mxunittask>  
     </target>  
    ```
      
      
    This makes sure the end report specifies the exact object that had the failed test in the final report.  So if the clientEmsGatewayTest had a failure on the test "testGetXbyY" the report would say failed test "testGetXbyY" in class "clientEmsGatewayTest"  instead of failed test "testGetXbyY" in class "gateway" as the prior technique did.
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    billy
    
    
    
    
    
    Very impressive, Bill! Keep 'em coming. Also keep an eye out for mxunit 2.0 sometime Q1-09, I hope. Many more goodies, and your inupt would be welcome.  
      
    bill  
    mxunit.org
    
    
    
    
    
    
    
    
    

