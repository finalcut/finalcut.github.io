---
layout: post
title: "SeleniumMX - A Selenium + MxUnit Framework"
date: 2010-02-26
comments: false
categories:
 - frameworks
 - cruisecontrol
 - ant
 - selenium
 - mxunit
 - seleniumMX
---
### The Problem

  
We do all sorts of development but one area where we do a lot of work is in
ColdFusion. Some of our stuff is pretty old but is still actively being
maintained so as I get onto those projects I try to inject some more rigorous
testing into the mix. The two frameworks we use are MxUnit for our unit
testing and then Selenium for functional testing. We tie all this together
using CruiseControl via an Ant build file. In general this all works together
pretty seamlessly ([once you figure out the kinks](http://cf-
bill.blogspot.com/2010/02/selenium-and-cruise-control-gotcha-and.html)).  
  
Sometimes, when using Selenium we are faced with a choice - do we want the UI
test to go through and setup a scenario that we want to test or do we want to
have the database prepared for the test to be run? In general we've decided
we'd rather have the database prepared in advance, however, I dont want to
have people on the team jump through hoops to do this.. Another problem with
Selenium is that it doesn't support a Suite of Suites type approach; thus we
are forced to update two suite files each time we create a new test.  
  

### The Solution

  
To deal with this mess I've crafted a special little framework to help -
SeleniumMX. The framework is dependant upon the existence and usage of MxUnit.
However, it should be fairly easy to port to other CF unit testing frameworks.  
  
There are six files involved in the framework three of which are "mixins" (all
prefixed with an underscore) and three are actual components that do all the
heavy lifting. I'm not going to go too deeply into each file here; instead
I'll just focus on the one file you have to actually edit to get the framework
to work for you and then I'll talk a bit about how to use it.  
  

#### Conventions

  
To use the framework I demand a bit of convention; that is that you have a
directory where you store all of your Selenium Tests. Sort of like this:  
  

    
    
      
    project  
            uitests (selenium tests go here)  
                    subdirectory1  
                            subsubdir1  
                    subdirectory1  
                            subsubdir2  
                            subsubdir3  
                    subdirectory1  
                    ...  
    ```
      
      
    The convention states that no tests exist in the uitests directory (or whatever you call yours) but that you have all of your tests logically organized in subdirectories under that and all of your test files must be .html files.  
    
    
    #### Settings
    
      
    Once your tests are organized you can just plop the SeleniumMX files into the uitests directory. And get to work.  The first thing you'll need to do is edit the file _seleniumMXSettings.cfm.  Their are four values you can modify and they are each documented inline.  If you don't use ColdSpring with your project then just set the coldspring setting to an empty string.  If you do there are a couple helper functions later that will make using the Coldspring Bean factory a bit easier.  
      
    
    
    #### Setup A Test
    
      
    Once your settings file is updated you're ready to create your first functional test "setup".  Again, I'm a fan of convention so there are certain ways to do things that will make your life a bit easier.  
      
    First, go into one of your test suite directories.  Let's say, for example, one is called "Datasets" so you'd go into the "Datasets" directory and create a setup.cfc and a teardown.cfc each of which should extend the seleniumMxBase.cfc  
      
    The setup.cfc must have one public function - testUIsetup that takes in no arguments.  Here is an example testUIsetup:  
    
    
    
      
     <cffunction name="testUIsetup" access="public">  
      <cfset setupTests('Datasets','testDatasetCreate, testDatasetUpdate, testDatasetDelete') />  
     </cffunction>  
    ```
      
      
    As you can see the testUIsetup calls the function setupTests with two arguments.  The first, 'Datasets', is the name of the directory you are in relative to the uitests root.  So if you were in the subdirectory 'Foo' under 'Datasets' you'd pass in 'Datasets/Foo'  The second argument is a comma separated list of the setup functions you want called.  
      
    
    
    #### What's Going On?
    
      
    Before I explain why you have to pass in the functions to be called in a list let me explain what happens once setupTests is called.  First the SeleniumMX looks in the suite directory for a testSettings.dat file (or whatever you named it in the _seleniumMXSettings.cfm file).  If it finds that file it re-trys the teardown process I'll explain later; just to be on the safeside in case something went wrong with your build earlier.  After that it calls the functions in the order they were passed in.  Each function is called and passed a structure called "data".  This data structure is key value paired so that they key is the function name and the value is any data returned from the function of that name.  Thus, when the first function in the list is called an empty struct is passed in.  However, that first function might return some useful ID values; say a datasetID in our current example.  Thus, after the first function is called the struct looks like this:  
    ```js  
    data  = {  
            testDatasetCreate => {  
                                            datasetID => 1  
                                    }  
            }  
    ```
      
      
    That structure is then passed into the next function and any data returned from it is appended and passed into the next and so on and so forth.  When all of the setup functions are called this structure is then converted into a WDDX packet and stored in the testSettings.dat file in the suite directory.  This way all those useful values are available to you when you get to the sister "teardown" methods to each setup.  
      
    
    
    #### Cleanup After Yourself
    
      
    That leads me to the next convention; in your teardown.cfc for each method you list and pass into the setupTests function you need to also create a teardown equivalent of the function.  Thus if you have testDatsetCreate in the setup.cfc you need a teardownTestDatasetCreate method in the teardown.cfc.  That teardown function will be passed in the node of the data struct that maps to the sister setup function.  Thus tearDownTestDatasetCreate will be passed data.testDatasetCreate (rather than the entire data structure).  
      
    The reason the setup works the way it does is so that you can reuse some of the work you did in prior setups if you want.  It may not be advantagous for you to do so but the option is at least there.  Thus if you have some setup funtions that build on the work done in earlier setup functions you dont have to repeat yourself.  And, remember, if you want to call a function manually as part of your setup process you can do that too; just bear in mind any artifacts you want to keep around for the teardown won't be in the data struct I store for later.  
      
    One convention we use just for simplicity sake, is that we name our setup function the same thing our Selenium test is called that we are setting the stage for.  Thus in my example in the Datasets directory there would be a testDatasetCreate.html file.  You don't have to do this but it makes figuring out what your code does a bit easier.  
      
    Once you've created your setup functions then you can go write your teardown functions in the teardown cfc.  That component also extends seleniumMxBase and it must have a public function called testUIteardown which looks like this:  
    
    
    
      
     <cffunction name="testUIteardown" access="public">  
      <cfset super.tearDownTests('Datasets') />  
     </cffunction>  
    ```
      
      
    This time you only have to pass in the suite name (again, make sure you handle subdirectories thusly 'Datasets/subdirectory').  After your testUIteardown is written just add all your teardown_setupTestname_ functions (make them all private) and you'll be good to go.  
      
    Your setup and teardown classes extend seleniumMxbase which, in turn, extends mxunit.framework.TestCase so you can test each of your setups and teardowns manually (just make them public for a bit) until you're satisfied.  
      
    
    
    ### Tying It All Together
    
      
    Finally, once your setups and teardowns are all written you will probably want to include them in your ant build file along with your selenium test runner.  One thing that the selenimMX framework will do for you is it will automatically build a master suite of tests for you that will end up in your /uitests directory.  Thus you just need to add the following to your ant build file:  
      
    
    
    
      
      <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">  
       <testcase name="siteroot.uitests.seleniumMxSetup" packageName="siteroot.uitests.seleniumMxSetup" />  
      </mxunittask>  
      
                      
                    <!-- copies the entire test directory tree over to selenium; we dont need one for each subdirectory -->  
      <copy todir="${uitests.testdir}" overwrite="true" flatten="false" granularity="1">  
        <fileset dir="${uitests.srcdir}" />  
      </copy>  
      
      <selenese   
       suite="${uitests.srcdir}/MasterSuite.html"  
       browser="${uitests.browser}"  
       results="${uitests.resultsdir}uiTestResults.html"  
       multiWindow="false"  
       timeoutInSeconds="980"  
       startURL="http://${uitests.server}" />  
      
      <antcall target="fixUITestReportHtml" />  
      
      <mxunittask server="${host}" verbose="true" outputdir="${output.dir}" errorproperty="mxunit.error" failureproperty="mxunit.fail">  
       <testcase name="siteroot.uitests.seleniumMxTeardown" packageName="siteroot.uitests.seleniumMxTeardown" />  
      </mxunittask>  
    ```
      
      
    You'll notice I have an ant call in there called "fixUITestReportHtml" that is a solution to [this problem](http://cf-bill.blogspot.com/2010/02/selenium-and-cruise-control-gotcha-and.html).  
      
    The ant task layed out above first calls the seleniumMXsetup with it's one public method which loops through all of your UI test suites and calls any setup.cfc objects it finds and has them do their magic; plus it builds a MasterSuite.html file.  The second step copies your entire test directory (including your MasterSuite.html file) for your selenium server project over to your websites selenium server test directory.  Then the selenese task is called on you the MasterSuite.html and all of your tests are run.  Next the results.html file that selenium creates is fixed to be xhtml compatiable and finally the seleniumMXTeardown is called which finds all of your teardown.cfc and cleans up behind your tests.  
      
    
    
    ### The Goods
    
      
    I'm putting this entire project out at GitHub so feel free to fork it and do what you want with it.  Hopefully it will help someone else out in using Selenium with MxUnit, ColdFusion, and your CI process.  You can get the source, along with a very rudimentary example [at my github repository](http://github.com/finalcut/SeleniumMX)
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    Bill
    
    
    
    
    
    A couple things I didn't mention in the blog post.  
    1. you don't have to use the auto-tear down stuff.  This is probably obvious but you can write teardown functions and just call them manually in your teardown.teardownUITests method.  This is useful when your functional test creates some things and you want to make sure they are deleted when the tests are done.  
      
    2. My main reason for wanting to do all of this was cleanup in case the functional test failed.  Right now the way Selenium tests are done they just aren't repeatable if something fails due to potential constraints in the backend.  
      
    3. I feel like this blog post is a bit confusing.  The readme.txt at GitHub seems a bit more clear to me.
    
    
    
    
    
    
    
    
    
    
    Bill
    
    
    
    
    
    Hi Bill, thanks for your comment.  The code is on GitHub already; though the example apps - base_build.xml file I stuck on there is the wrong one.  However, you could still figure out how it all works pretty easily ignoring the base_build.xml.  
      
    I have not tried to use Selenium 2 at all yet.  I probably should get off my but and do so though as we have some quirks on developers desktops with Selenium and posting results.
    
    
    
    
    
    
    
    
    
    
    bill shelton
    
    
    
    
    
    Great stuff, Bill. Thanks. I'm wiring in some functional tests at work and this looks like it'll help. I look forward to a follow-up and the code up on Github - which I will follow :-)  
      
    One question, have you tested this with Selenium 2 - that is, the Webdriver backed Selenium?  
      
    best.  
    bill shelton
    
    
    
    
    
    
    
    
    

