---
layout: post
title: "Setting Up MxUnit, Ant, and CruiseControl"
date: 2008-10-15
comments: false
categories:
 - coldfusion
 - continuous-integration
 - unit testing
 - cfeclipse
 - eclipse
 - cruisecontrol
 - unit-testing
 - ant
 - mxunit
 - editplus
---
This is probably going to be a long post. Hopefully it will all be explained
OK.


## Getting Things Installed



### MxUnit


MxUnit is actually pretty easy to setup. Download it and then extract the zip
file into your webroot. Once it is there it is basically setup. However, in
order to get it to work with Ant there are a couple other small steps.

First, go to your mxunit directory (c:\inetpub\wwwroot\mxunit\\) and drill
down to the \ant\lib directory. Inside that folder is the file mxunit-ant.jar.
Copy this file to your personal user ant directory.

Secondly, go back to your mxunit directory and copy the ant/xsl directory to
whatever project you are working on. You'll need those files later if you want
to make sense of the mxunit ant output.


#### Your Personal Ant Directory


On windows this is c:\documents and settings\\{username}\\.ant\lib. In order
to create the .ant directory you probably have to use the command line.


### Ant


I had Ant on my machine already thanks to Eclipse. CruiseControl also comes
with Ant so you don't really have to do anything special to get Ant up and
ready. However, I suggest you also download the [ant-contrib](http://ant-
contrib.sourceforge.net/) which has a bunch of helpful tasks you will end up
needing. Once you have this file plop it into your user ant directory as well
(see above).


#### SVN and ANT


If you are using [TortoiseSVN](http://tortoisesvn.tigris.org/) 1.5.0 you can
use [SvnAnt](http://subclipse.tigris.org/svnant.html) 1.2 RC 1 without
problem. Just make sure you have removed all legacy SvnAnt files. Just note
that you can't use the SVN config options in CruiseControl (not too big of a
deal) becuase the build process will fail saying you need to upgrade your svn
client.


### CruiseControl


Cruise Control is pretty easy to install and overall isn't too hard to
configure. However, there are a couple of small caveats. If you try to base
your build config off the example provided you will need to copy all of the
Jar files you already put in your personal Ant directory and put them in the
CruiseControl/apache-ant-xxx/lib directory. Else your Ant build will probably
fail.



## Tying It All Together


Ok so now everything is installed but you aren't sure how to get each thing
working as a synchronous whole. Hopefully this will help. First off, I really
did mean it when I suggested you get the ant-contrib earlier; it comes in
handy when using MxUnit with Cruise Control becuase, MxUnit seems to return
fairly useless information to its Ant Task.


First off Here is my very simple Build.xml - it only updates stuff from SVN
and then runs the MxUnit tests. It has some conditional logic in there so that
you can opt to not see the report if you don't want (best option for
CruiseControl). While developing I prefer to see the report if an error
occurs:




```xml

<project name="Listbuilder USAF" default="testWithReport" basedir=".">



 <taskdef name="mxunittask" classname="org.mxunit.ant.MXUnitAntTask" />

 <taskdef resource="net/sf/antcontrib/antcontrib.properties"/>




 <!-- PROPERTY DEFINITIONS -->

 <property name="host" value="localhost" />

 <property name="junit.out.dir.xml" value="${basedir}/testresults" />

    <property name="junit.out.dir.html" value="${basedir}/testresults/html" />

    <property name="output.dir" value="${basedir}/testresults/tmp" />

 <property name="style.dir" value="styles/ant/xsl" />


 <property name="mxunit.error" value="false" />

 <property name="mxunit.fail"  value="false" />



 <!-- SVN INTEGRATION -->

 <target name="updateSource"><!-- if svnant wont work.. try this -->

  <exec executable="C:\Program Files\TortoiseSVN\bin\TortoiseProc.exe">

   <arg value="/command:update" />

   <arg value="/closeonend:3" /> <!-- force the dialog to close -->

  </exec>

 </target>


 <typedef resource="org/tigris/subversion/svnant/svnantlib.xml"  />

 <target name="svnAntUpdate">

  <svn username="USERNAME" password="PASSWORD">

    <update dir="${basedir}" recurse="true" />

  </svn>

 </target>




 <!-- TEST WRAPPERS -->

 <target name="testWithoutReport" depends="allUnitTests">

  <if>

   <equals arg1="${mxunit.error}" arg2="true" />

    <then>

     <antcall target="junitreport" />

    </then>

   <elseif>

   <equals arg1="${mxunit.fail}" arg2="true" />

    <then>

     <antcall target="junitreport" />

    </then>

   </elseif>

  </if>

  <antcall target="testCleanup" />

 </target>


 <target name="testWithReport" depends="allUnitTests">

  <antcall target="displayResultsIfProblems" />

  <antcall target="testCleanup" />

 </target>



 <!-- TEST SUPPORT -->

 <target name="testSetup" depends="svnAntUpdate">

     <mkdir dir="${junit.out.dir.html}" />

     <mkdir dir="${output.dir}" />

   </target>

 <target name="testCleanup">

  <if>

   <equals arg1="${mxunit.error}" arg2="true" />

    <then>

     <fail message="Mxunit Had one ore more errors" />

    </then>

   <elseif>

   <equals arg1="${mxunit.fail}" arg2="true" />

    <then>

     <fail message="Mxunit Had one ore more failures" />

    </then>

   </elseif>

   <else>

         <delete dir="${junit.out.dir.xml}" />

   </else>

  </if>

   </target>


 <!--- TEST SUITES -->

 <target name="allUnitTests" description="Run a dir of tests recursively"  depends="testSetup, beanTests, daoTests" />


 <target name="beanTests" depends="testSetup">

    <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">

         <testcase name="lb2.unittests.model.bean.clientCustomQuestionTest" packageName="lb2.unittests.model.bean.clientCustomQuestionTest" />

         <testcase name="lb2.unittests.model.bean.clientRegionTest" packageName="lb2.unittests.model.bean.clientRegionTest" />

     </mxunittask>

 </target>


 <target name="daoTests" depends="testSetup">

    <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">

         <testcase name="lb2.unittests.model.dao.customGuidanceTest" packageName="lb2.unittests.model.dao.customGuidanceTest" />

         <testcase name="lb2.unittests.model.dao.regionTest" packageName="lb2.unittests.model.dao.regionTest" />

    </mxunittask>

 </target>





 <!-- UNIT TEST RESULT REPORTING -->

 <target name="junitreport" description="Create a report for the test result">

     <mkdir dir="${junit.out.dir.html}"/>

     <junitreport todir="${junit.out.dir.html}">

        <fileset dir="${output.dir}">

           <include name="*.xml"/>

         </fileset>

         <report format="frames" todir="${junit.out.dir.html}" styledir="${style.dir}"/>

      </junitreport>

 </target>



 <target name="displayTestResults" depends="junitreport">

   <exec executable="C:\Program Files\Internet Explorer\iexplore.exe">

     <arg value="${junit.out.dir.html}/index.html"/>

   </exec>

 </target>


 <target name="displayResultsIfProblems">

  <if>

   <equals arg1="${mxunit.error}" arg2="true" />

    <then>

     <antcall target="displayTestResults" />

    </then>

   <elseif>

   <equals arg1="${mxunit.fail}" arg2="true" />

    <then>

     <antcall target="displayTestResults" />

    </then>

   </elseif>

  </if>


 </target>



</project>


```





Once I had my build file running properly (I use [EditPlus with Ant](http://cf-bill.blogspot.com/2008/10/configure-editplus-with-ant.html) but this same setup will work fine with (CF)Eclipse) I worked on getting my project configured on Cruise Control.


First I went to the CruiseControl/projects directory and checked out my project to a new folder named after my project.  Then I went to the CuriseControl/logs directory and created a folder that matches my project name.  Then backup to the CruiseControl directory to edit the cruisecontrol.config to add my project.


Here is my basic config file for this project:





```xml
<cruisecontrol>

 <project name="listbuilder_usaf" requireModification="false">

        <listeners>

            <currentbuildstatuslistener file="logs/${project.name}/status.txt"/>

        </listeners>


  <modificationset quietperiod="30">

            <filesystem folder="projects/${project.name}" />

        </modificationset>


        <schedule interval="600">

            <ant anthome="apache-ant-1.7.0" buildfile="projects/${project.name}/build.xml" target="testWithoutReport" />

        </schedule>


        <log>

            <merge dir="projects/${project.name}/target/test-results"/>

        </log>


  <publishers>

   <onfailure>

    <email mailhost="smtp.gmail.com" mailport="465" username="USERNAME" password="PASSWORD" subjectprefix="BUILD FAILED: " buildresultsurl="http://MYSERVER:8080/dashboard/tab/build/detail/listbuilder_usaf" usessl="true" returnaddress="bill.rawlinson@gmail.com">

     <always address="EMAILADDRESS1" />

     <always address="EMAILADDRESS2" />

    </email>

   </onfailure>

  </publishers>

 </project>

</cruisecontrol>


```




Once you add a project you have to restart the CruiseControl service.  However, once it is added you can edit it and the changes will be picked up on each subsequent build run.


To test my build I open the CruiseControl/logs/wrapper.log file in my text editor (EditPlus) and then load CruiseControls dashboard in my browser (http://localhost:8080/dashboard is the default address).  Then I open my projects page and click on a small "refresh" looking arrow icon which forces a build.  Watching the log file helps you figure out if anything is going wrong with the build process and how to fix it.  Particularly useful if you have just done something wrong with the CruiseControl config.


I'm using CruiseControl version 2.7.3 and the SVN client that is built in is NOT compatiable with any other SVN clients at version 1.5 - thus I can't use any of the handy SVN options (such as detecting a change and instigating a build).  Thus I am forced to just do a timed build every 10 minutes or so.  It's not ideal but it is better than nothing.  If anyone knows a solution to that problem please let me know!  Whatever the solution is it has to work with Tortoise 1.5.0 and SvnAnt (or at least two equally compatible versions of those two clients.


It is important to note the two different methods I have for running all of my tests.  The one I use in development launches IE with the results html files.  If you run this same target in CruiseControl be prepared for grief and a neverending build cycle.  IE Launches, somewhere in memory, but never actually draws, and thus you will have to kill the process.  Thus, whatever you do, don't let CruiseControl start IE.  Interestingly enough, however, if CruiseControl launches TortoiseSVN via the Ant build it works just fine.  I'm not sure what the difference is between how the two apps launch.


Finally, also pay attention to my use of conditionals in my build file.  I do this so that I can report a "FAILURE" of some sore if an error or fail is reported by MxUnit.  Ant, otherwise, reports a nice clean "BUILD SUCCESSFUL" build which is really misleading.  True, you do have the option of using the "haltonfailure" attribute but then you don't get the nice report document at the end.  I'm still undecided on which option I prefer.


I hope, eventually, that mxunittask is updated to report the actual Unit test failures back to ANT on a "haltonfailure" - until then it seems fairly useless.


I know there i a lot to consume here and that I barely scratched the surface.  However, if you have any questions just leave a comment and I'll try to help.


**UPDATE**

HAHA! Success.  One of the older versions of SvnAnt came with a JavaSVN jar.  Once I removed it all of my svn needs work.  Tortoise, SvnAnt, CruiseControl... Boo YA!





## Comments











Bill






Eric,

Thanks.  Hopefully my experience will help make yours a little smoother.











Eric Gregory






Awesome post!  I'm setting up a similar project with CruiseControl, SVN, and Ant, and (ideally) getting some unit tests to work with the whole mess.



So far, just getting svn to work with Ant took almost half a day (ouch.)


In the end I went with Ant 1.7.1 and SVNant 1.2.1.  All you really have to do is copy Jars from SVNant into Ant's lib folder.  You get to choose between svnkit and javahl -- I'm told svnkit is better but have no real means of comparison.


My ant script contains:



<typedef resource="org/tigris/subversion/svnant/svnantlib.xml" />

  <target name="svnAntUpdate">

   <svn username="YourUsername" password="YourPassword">

     <update dir="." recurse="true" />

   </svn>

  </target>










