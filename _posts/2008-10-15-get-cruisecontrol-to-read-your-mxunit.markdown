---
layout: post
title: "Get CruiseControl to Read Your MxUnit Test Results"
date: 2008-10-15
comments: false
categories:
 - cruisecontrol
 - mxunit
 - reporting
---
I just had a minor epiphany on getting my test results to appear in
CruiseControl; in my config file I needed to merge the log files.





```xml
        <log>

            <merge dir="projects/${project.name}/testresults/tmp"/>

        </log>


```




That location is where I I had my buildfile putting the MxUnit log files as it generated them.  The only key to remember is to not have your build file cleanup the log files until the next time you run the build.  So, now, my build file, upon starting, removes the old build log directory and then recreates it, populates it, and finishes.  Then CruiseControl sucks those log files into its own log file and displays the results in the dashboard (or in the email that is sent).


Here is an example:





```
Test Suites (2)

lb2.unittests.model.dao.customGuidanceTest

Tests: 1, Failures: 0, Errors: 0, Duration: 16.566

lb2.unittests.model.dao.regionTest

Tests: 6, Failures: 0, Errors: 0, Duration: 16.034


```






