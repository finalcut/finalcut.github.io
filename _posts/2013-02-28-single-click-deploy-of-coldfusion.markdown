---
layout: post
title: "Single Click Deploy of a Coldfusion Project from ANT"
date: 2013-02-28
comments: false
category: coldfusion
tags: [svn,svnant,ant,ant-zip,ant-subversion,ant-email,one-click-deploy]
---
Sometimes I'm way behind the power curve.  Today is one of those days.  I've
been using ant and cruise control for years to do some continuous integration
testing of some ColdFusion projects but until today I didn't have any where
there was a single click deploy process.

The project I set it up on is being managed in subversion - so if you use Git
or some other version control system you'll have to adapt this to suit your
own needs.

Before I start sharing the ant scripts here is some important background
information you need to know and understand in order to actually make sense of
the ant stuff.  First up is our branching and tagging policy for the project.

We use trunk as the main development branch.  We don't do big feature
development on it but any quick bug fixes or what-not end up happening on
trunk.  We also have a UAT and a PRODUCTION branch.  New features that our
customer wants to test before delivery get merged from trunk to the UAT
branch.  New features are developed on feature branches but once they are
ready for UAT they get merged into TRUNK and then merged into UAT.  Once the
feature is finished in the feature branch and we are making simple bug fixes
to the features we typically make those just in TRUNK and merge to UAT.

We don't merge into production until things have cleared UAT.  Once we are
ready to merge into UAT we make one final edit - to a file in the root of the
projects directory called application.version.tag.cfm - this file just
contains the new version number for the application.  This version number will
also be used to create a release tag in subversion as part of the deployment
process.  Once that version file is updated and commited we then merge all of
the relevant changes from trunk to production for that release.  It is really
important to have good comments and, ideally, issue numbers related to each
commit for that feature set that is about to be pushed to production.

Once the merge into production is done and we are confident we want to push
the changes to production we go to our continuous integration server (we
recently moved from cruisecontrol to jenkins) and fire off the production job
for that project.

The production job does the following things:

  1. updates the local production test webserver with the latest version of the production branch
  2. runs our suite of tests against the production test webserver
  3. if the tests pass...
  4. reads in the contents of application.version.tag.cfm to get the version number
  5. checks to see if a tag in subversion already exists for that version number
  6. if the tag exists the build stops and the user is prompted to either update the version number or manually delete the tag from subversion.
  7. if the tag doesn't exist...
  8. create a tag in subversion based on the production branch named the same as the version number
  9. export the newly created tag to a staging directory
  10. delete any subdirectories or files we manage in subversion but which we don't deploy to production
  11. create a zip file of the remaining tag export files/directories
  12. delete the exported files that remain but keep the zip handy
  13. copy the zip file to a place where the customer can get it*
  14. delete the zip file from the staging location
  15. send out an email to the customer (and us) letting folks know the production zip file is ready.

The purists among you may say - wait this isn't a one click deploy -
production isn't actually updated by this. And to you I say, "I know.  It
sucks but I must work within the limitations I have"

The customer only lets us connect to them via special laptops they provide and
only when those machines are connected to their vpn using a timed key token.
There just isn't a practical way to connect to them, then map to their
webserver, and then copy the files over the network to them within those
constraints.   Thus we get as close to copying the files to the webserver as
we can.



I'm not going to explain every property that these ant tasks use.  You'll just
have to figure them out on your own sorry but hopefully they are fairly
obvious.  I'm also not showing the task that runs the tests or the one that
updates our production test webserver in order to run the tests.



This task gets the party started:







```xml
 <target name="releaseIfNoProblems">

  <if>

   <equals arg1="${mxunit.error}" arg2="false" />

    <then>

     <if>

      <equals arg1="${mxunit.fail}" arg2="false" />

      <then>

       <antcall target="createTagInSvn" />

       <antcall target="package" />

       <antcall target="pushPackagetoPublicWebsite" />

       <antcall target="sendEmailAboutNewRelease" />

      </then>

     </if>

    </then>

  </if>

 </target>


```



Next up is the set of steps involved with tagging the release in subversion:





```xml
 <target name="readTagFromFile">

  <loadfile property="svn.tag.name" srcFile="application.version.tag.cfm"/>

 </target>


 <target name="createTagInSvn" depends="readTagFromFile">

  <property name="svn.url.tag" value="${svn.url.tags}/${svn.tag.name}" />


  <echo message="source branch: {$svn.url.prod}" />

  <echo message="destionation tag: {$svn.url.tag}" />




   <condition property="svn.tag.exists" value="true" else="false">

          <svnExists javahl="false" svnkit="false" target="${svn.url.tag}" />

      </condition>


  <echo message="svn tag exists: ${svn.tag.exists}" />

  <if>

   <equals arg1="${svn.tag.exists}" arg2="true" />

    <then>

     <!--

      IF we wanted to delete the tag, just in case, before proceeding we could make this block active...

     -->

     <svn username="${svn.username}" password="${svn.password}" javahl="false" svnkit="false" failonerror="false">

      <delete url="${svn.url.tag}" message=" [Build Script] delete previous tag: ${svn.tag.name}" />

     </svn>

     <fail message="The tag ${svn.tag.name} already exists in Subversion.  Please update the application.version.tag.cfm file OR delete the tag in subversion" />

    </then>

    <elseif>

     <equals arg1="${svn.tag.exists}" arg2="false" />

     <then>

      <echo message="the tag doesn't exist yet so let's proceed..." />


      <svn username="${svn.username}" password="${svn.password}" javahl="false" svnkit="false" failonerror="true">

       <copy srcurl="${svn.url.prod}" desturl="${svn.url.tag}" message=" [Build Script] created tag: ${svn.tag.name}" />

      </svn>

     </then>

    </elseif>

  </if>

  <echo message=" ... tagging completed." />

 </target>


```



Here is the packaging process:


```xml

 <target name="prepPackagingArea">

   <delete dir="${package.dir}${ant.project.name}/" />

   <delete file="${package.dir}${package.name}" />

 </target>


 <target name="cleanupPackaging">

   <delete dir="${package.dir}${ant.project.name}/" />

 </target>


 <target name="zipPackage" depends="delDirFromPackage">

  <zip destfile="${package.dir}${package.name}" basedir="${package.checkdir}" />

 </target>


 <target name="delDirFromPackage">

  <delete dir="${package.checkdir}_Database/" />

  <delete dir="${package.checkdir}_DetailImport/" />

  <delete dir="${package.checkdir}_Documentation/" />

  <delete dir="${package.checkdir}uitests/" />

  <delete dir="${package.checkdir}testresults/" />

  <delete dir="${package.checkdir}MVInstall/" />

  <delete dir="${package.checkdir}Replication/" />

  <delete dir="${package.checkdir}styles/" />

  <delete dir="${package.checkdir}unittests/" />

  <delete dir="${package.checkdir}Updater/" />

  <delete>

   <fileset dir="${package.checkdir}" includes="*.xml*" />

   <fileset dir="${package.checkdir}" includes="*.bat" />

   <fileset dir="${package.checkdir}" includes="application.lines.cfm" />

   <fileset dir="${package.checkdir}Config/" includes="config.*" />

  </delete>

 </target>


 <target name="package" depends="prepPackagingArea, readTagFromFile">

  <svn username="${svn.username}" password="${svn.password}" javahl="false" svnkit="false" failonerror="false">

    <export srcurl="${svn.url.tags}/${svn.tag.name}" revision="HEAD" destPath="${package.checkdir}" />

  </svn>

  <antcall target="zipPackage" />


  <antcall target="cleanupPackaging" />

 </target>


```



Then we need to push the package to the deployment directory and delete the zip file from staging:




```xml
 <target name="pushPackagetoPublicWebsite">

  <echo message="pushing the package to an accessible location ${deploy.dir}\${package.name}"/>


  <copy file="${package.dir}${package.name}" tofile="${deploy.dir}\${package.name}" overwrite="true" force="true" />


  <delete dir="${package.dir}" />

 </target>


```



Finally I need to send out the email(s):


```xml

 <target name="sendEmailAboutNewRelease" depends="readTagFromFile">

  <echo message="sending email"/>

  <mail from="XXX" tolist="XXX" mailhost="SOMEHOST" message="Please go to ... and download the zip file for deployment.  Remember, this doesn't include the production config.xml file so you need to preserve the config file at ${ant.project.name}\config\config.xml" subject="${ant.project.name} has a new release ready for installation: version ${svn.tag.name}" />

 </target>


```


 As you might imagine I had to add some extra libraries to ANT.  First was the svnant library and then I also had to add ant contrib and finally two jar files from oracle in order to get the mail stuff to work [mail.jar](http://www.oracle.com/technetwork/java/index-138643.html) and [activation.jar](http://www.oracle.com/technetwork/java/javase/downloads/index-135046.html)





## Comments











Jim Priest






Added to the old Ant wiki:  http://www.thecrumb.com/wiki/ant
