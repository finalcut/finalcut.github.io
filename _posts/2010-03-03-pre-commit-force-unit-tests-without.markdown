---
layout: post
title: "Pre-Commit Force Unit Tests Without Annoying Yourself"
date: 2010-03-03
comments: false
categories:
 - continuous-integration
 - unit testing
 - ant
---
Unit testing is a good thing. I don't think anyone would disagree with that
statement in the general sense. However, once you get a really large library
of unit tests it can be kind of a pain in the but to run them all because they
can take a while to finish up and thus, it is easy to bypass the all important
test build before committing changes. Sure, you run the tests you just wrote
but you might have broken something else and never know it until your
continuous integration server points the ugly finger at you for breaking the
build.  
  
Fortunately, there are some tactics you can take to help you remember to build
when you commit and give you a heads up before your build server blames you.
This article will be discussing the SVN pre-commit hook; specifically when
using TortoiseSVN. I LOVE tortoiseSVN and can't imagine interacting with SVN
without. And recently when I found the hooks section of tortoiseSVN's settings
dialog I feel a little deeper in love.  
  
Before you rush off to set your hook up you need to do some ground work. First
you need to make sure you have an ant task that will do everything you want
and you need a batch file that your hook will execute. The batch file will in
turn fire off the ant task.  
  
I'll show you the code in a second but I want to explain a key concern I had
when I started figuring this all out. I often will be working on many issues
at one time and when I go to check in my code I like to associate the commit
with an appropriate issue number. Thus I'll often make 2-5 commits in a row.
Having each of these commits firing off my entire suite of unit tests is not
acceptable. Thus the solution I came up with had to prevent that situation.  
  
Ok, enough jabber, here's some code. First off is my build task that goes in
my ant build file:  

    
    
      
     <target name="preCommitTest">  
      <available file="${basedir}/test_results.txt" type="file" property="resultsFilePresent"  />  
      <if>  
       <equals arg1="${resultsFilePresent}" arg2="true" />  
       <then>  
        <!-- do nothing -->  
       </then>  
      
       <else>  
        <echo file="${basedir}/test_results.txt" message=".." />  
        <antcall target="runFullTestSuite" />  
        <antcall target="displayResultsIfProblems" />  
        <antcall target="testCleanup" />  
        <delete file="${basedir}/test_results.txt" />  
       </else>  
      </if>   
     </target>  
    ```
      
      
    The only way I could think of to make sure the build didn't get fired off back to back to back was to create some form of "locking" mechanism.  My lock solution is a file.  I create a file in the root of my project when I start building and I delete the file when I'm done building.   
      
    YES I know that a collision could happen and two builds could, theoretically, fire off the unit tests.  However, I'm just not that quick at clicking in Subversion, entering my issue number, and typing in some comments so I doubt this will ever actually occur.  
      
    The ant target I just showed basically looks for my lock file and, if it is there, it does nothing and just exists the target.  However, if it isn't present it creates the file, runs the full test suite, then; if their are problems; it pops up an IE window with the full JUNIT result set.  Next it cleans up after the tests (getting rid of all the .xml files and stuff) and finally it deletes my lock file.  
      
    The next thing I had to do was create a simple batch file.  It's just one line long and it looks like this:  
      
    
    
    
      
    :: can't seem to run a specific ant task without a batch file; update the path to your ant.bat  
    C:\my\ant\install\directory\bin\ant.bat preCommitTest  
    ```
      
      
    As you can see it just calls ant, tells it which target to use and that's it.  Simple eh?  
      
    Ok, the last thing I had to do was create my hook.  To do that I followed these steps:  
    
    
      
    
      * In Windows Explorer go to the root of my project
      
    
      * Right click in the white space of the directory
      
    
      * Select "Tortoise SVN" | "Settings" from the popup menu
      
    
      * Click on the "Hook Scripts" menu item in the dialog
      
    
      * Click the "Add..." Button
      
    
      * Select "Pre-Commit Hook" in the Hook Type dropdown
      
    
      * Put the root of my project in the "Working Copy Path"
      
    
      * Put the full path to my batch file in the "Command Line to Execute" field
      
    
      * Make sure "wait for script to finish" is UNCHECKED
      
    
      * Optionally leave "Hide the Script While Running" UNCHECKED (I do)
      
    
      * Click "OK"
      
      
      
    At this point your pre-commit hook is defined and ready to rock.  NOTE: If your build fails your code is still going to commit so this isn't going to completely save you.  However, it will give you a nice warning that you just broke the build long before anyone else gets a tell tale "Build Broken" email.  So, hopefully you can fix your little mistake before the next build on the CI server happens and you can avoid the "Build Broken" email in the first place.  
      
    I choose to leave the script window open while the build is running as it serves as kind of a "progress" bar to me; so long as the window is open I know the tests are executing.  It is a flag of sorts telling me I can keep on committing without firing off the whole suite again so long as that black window is open.  However, if the window gets on your nerves or messes up your tab order feel free to uncheck that option and never be bothered by your unit testing unless one fails.  
      
    NOTE: You'll want to commit your batch file to SVN too so your whole team has it just make sure they don't commit it again if they make a change to the path or else they'll end up breaking your batch file when you next update.  Fortunately TortoiseSVN also has the cool ability to add files to an "ignore-on-commit" list which I strongly suggest you use for this and other files like it.
    
    
    

