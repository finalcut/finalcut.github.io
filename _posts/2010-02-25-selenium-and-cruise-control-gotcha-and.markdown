---
layout: post
title: "Selenium and Cruise Control - GOTCHA and Tutorial"
date: 2010-02-25
comments: false
categories:
 - coldfusion
 - cruisecontrol
 - ant
 - selenium
---
Yesterday, and this morning, I spent quite a bit of time trying to get our
Selenium test results to show up in the Cruise Control build log email.
Nothing I did seem to work. However, after much gnashing of teeth and pulling
of hair I have it working. Here are the steps involved.

First off visit this page [Adding Selenium Results to CC Build
Report](http://wiki.openqa.org/display/SEL/Adding+nice+selenium-
results+to+build+report)

After you've read it you'll probably be thinking, "Ok, looks simple enough,
why all the drama?" Well, I'll tell you - those instructions don't work
exactly in every scenario but they are oh so very close.

First off it is imperative you realize when the instructions say, add this to
the <merge> section you really can only specify one selenium results
file to merge. You can't cheat and just tell it to merge the directory because
it just won't work. So make sure your cruise control config looks like this:




```xml
        <log>

            <merge dir="projects/${project.name}/testresults/tmp"/>

            <merge file="projects/${project.name}/testresults/ui/selenium-results.html"/>

        </log>


```




Yours may not be exactly like that but it is close enough to give you an idea.  The first entry in my merge pulls in my mxunit results (the whole directory) and the second pulls in just my selenium file.


Ok, now that we have that out of the way we can move onto the second bit.  The HTML header.  I'm using the prebuilt selenium ant task and thus I don't really have a way to change the way the selenium task creates the HTML output.  Thus I cheat and am using an ANT task to clean up the results and to prepend the correct header to the file.





```xml
 <target name="fixUITestReportHtml">

  <replace file="${uitests.resultsdir}uiTestResults.html" token="<html>" value="" />


  <concat destfile="${uitests.resultsdir}selenium-results.html">

   <fileset file="${uitests.srcdir}html_header.txt" />

   <fileset file="${uitests.resultsdir}uiTestResults.html" />

  </concat>


  <delete file="${uitests.resultsdir}uiTestResults.html" />

 </target>


```




The first bit drops out the offending "html" tag and the second concat part inserts in the correct xhtml header.  Well, almost.  I actually had to change part of the xhtml header so that it wouldn't point to the W3C copy of the xhtml DTD.  Why?  Well, because the W3C ends up banning you from asking for it if you ask too often and you'll end up getting a 503 request denied error which causes Cruise Control to ignore your selenium results and to never import it into your build file.


That's right - NEVER.  Make sure you pay attention to your CruiseControl.log file!


To work around this I downloaded the DTD and the three related entity files and put them on a webserver we have at work.  Then I changed my xhtml header to point to my copy of the DTD.  Ideally cruisecontrol would cache the DTD and I wouldn't have to do all that but they don't and I do.  Anyway, here the contents of the html_header.txt file:


```html

<!DOCTYPE html

PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"

"http://my.server.com/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">


```




No, I don't own "my.server.com" I just don't want you pointing at my copy of the DTD either.  Download your own copy if you need to.  My server is running IIS and it wouldn't serve up the entity documents without some fiddling so I worked around it and renamed them to .xml files and then updated the DTD to point to the xml instead of the .ent files.  If you download the DTD you'll see what I mean.  The .ent files on the WC3 site are in the exact same directory as the DTD so after you get the DTD make sure you download the three .ent files or none of this will work either.


Whew, well, we have all that out of the way so we should be in good shape.  Well, almost.  The next part deals with creating an xsl file and then updating another file to reference it.


Now, maybe you're a more careful reader than I am but if not let me point out that the code snippet on the page I referenced when this post started shows 2 lines you have to add to the buildresults.xsl file.  That file, by the way, is in my CruiseControl/webapps/cruisecontrol/xsl directory.  Anyway, once you're in that file make sure you add both lines (here's the first):




```xml
  <xsl:import href="selenium.xsl"/>


```



I put that line right after the last existing "import" statement.  Then I jumped to the last of the "apply-template" statements and added:




```xml
    <p><xsl:apply-templates select="$cruisecontrol.list" mode="selenium"/></p>


```




Finally I created my selenium.xsl file in the same directory.  Once that was done I was ready to go.  Almost.


It turns out, and you probably already knew this, but you can't create a suite of suites with Selenium.  Boo Hiss that limitation.  So now I have to create a "Master Suite" that basically is a consolidation of all the rows of my various test suites.  Once that was done I just added this task to my ant build file:



```xml

 <target name="AllUITests" depends="createUITestLogginDirectory">

  <!-- copies the entire test directory tree over to selenium; we dont need one for each subdirectory -->

  <copy todir="${uitests.testdir}" overwrite="true" flatten="false" granularity="1">

    <fileset dir="${uitests.srcdir}" />

  </copy>



  <!--

   this will setup all stuff needed for every test in the test suite..  It could be pretty intensive

  -->

  <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">

   <testcase name="wcs.uitests.setup" packageName="wcs.uitests.setup" />

  </mxunittask>




  <selenese

   suite="${uitests.srcdir}/MasterSuite.html"

   browser="${uitests.browser}"

   results="${uitests.resultsdir}uiTestResults.html"

   multiWindow="false"

   timeoutInSeconds="80"

   startURL="http://${uitests.server}" />



  <!--

   this will teardown all stuff needed for every test in the test suite..  It could be pretty intensive

  -->

  <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">

   <testcase name="wcs.uitests.teardown" packageName="wcs.uitests.teardown" />

  </mxunittask>


  <antcall target="fixUITestReportHtml" />

 </target>
```




Now, be careful just copying and pasting that last little bit.  I have to mysterious mxunit tasks being called that I will explain in detail in my next post.  However, to whet your appetite those tasks are part of a framework I built that lets us easily massage the database the application runs on before we run certain Selenium tests that expect specific data to exist in the application.  I'll be putting that framework on GitHub as well so if you have a similar need it might help you.


Anyway, once you have all your stuff setup and you get CruiseControl to run your tests you should get a success email that looks something like this:



```
             Selenium Tests  passed: 5, failed: 0; Commands passed: 5, failed: 0, broken: 0


---




            All Tests Passed
```






However, if you've screwed up you'll see something like this:




```
             Selenium Tests


---




            No Tests Run    This project doesn't have selenium tests
```





Which, quite frankly is a pain in the ass message.  If you do see this the first place you should look is in your CruiseControl.log file - I always forget this file exists.  Just zoom to the bottom of that file and it will probably tell you what went wrong.  However, if that shows no problems at all then you probably ignored my initial comment about having to specify the exact file to merge into the results.


Also note that if any of your initial unit tests fail or have an error your build results file won't include any selenium tests.  I'm guessing that is because the selenium tests don't even get run if the unit tests fail; however, I'm not entirely sure.  Either way once you get your unit tests to pass you'll start seeing the results of your UI tests again.


Good Luck and Good Testing!




