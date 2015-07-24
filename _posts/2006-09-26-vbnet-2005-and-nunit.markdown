---
layout: post
title: "VB.Net (2005) and nUnit"
date: 2006-09-26
comments: false
categories:
 - nUnit
 - xUnit
 - vb.net
 - development
 - .net
 - tdd
 - testing
---
I have recently been put on another project, this one with VB.Net (a windows
client app) and decided this would be a good opportunity to learn a bit about
the xUnit testing framework for .Net apps called nUnit. nUnit, as of this
writing, is at version 2.2.8 and their sites documentation is pretty spartan
when it comes to actually using nUnit or writing unit tests for VB.net. This
post is intended to help fill that gap for the absolute newbie to nUnit and
VB.Net using Visual Studio 2005.

To start with you need to [download
nUnit](http://www.nunit.org/index.php?p=download). Once you have downloaded it
install it using the default options; doing this really is the easiest option.
Once that is installed fire up VS 2005.


## VS 2005 Integration


There are a three ways to integrate with VS 2005. The first, and one I won't
cover here, is to buy [testdriven.net](http://www.testdriven.net/) and install
it. While testdriven.net is by far the most feature rich option I don't have
$95 to mess around with it right now so we will stick with the poor mans
choice and that is a VS 2005 "external tool"

Once you have a project created in VS 2005 (or you open an existing project
you want to start incorporating unit testing into) open the "tools" menu and
select the external tools option. This will pop up a small dialog box that
lets you add/edit custom tools. By default in my version of VS 2005 one custom
tool already existed (Dotfuscator) so I needed to add a new one. To do so you
just click on the "Add" button.

There are four five fields you are interested in.


Title


nUnit

I called mine nUnit kinda makes sense)

Command


C:\Program Files\NUnit-Net-2.0 2.2.8\bin\nunit-console.exe

I used the browse button to find nunit-console.exe, if you installed in the default place it should be what I entered

Arguments


$(TargetPath)

Initial Directory


$(TargetDir)


Since this setup is using the console option I also checked the "Use Output
Window" checkbox. For the "command" option you can also use the nunit-gui.exe
if you want to see a nice graphical representation of test success/failure or
just want to run certain tests; for the remainder of this article I will be
referencing the console version but the gui version works just as well.

Once done entering my custom tool settings I hit the "OK" button. Then I
return to the "tools" menu and pick "customize". Another dialog pops up that
lets you create new toolbars and to put buttons on existing toolbars. Lets not
worry about creating a new toolbar just for our nUnit button. Instead click on
the "commands" tab then in the left pane (Categories) scroll down and select
"tools". The right pane (Commands) will populate. Scroll through there until
you find "External Command 2" (if your nUnit was the second custom command)
and then drag that command onto any of your existing VS 2005 toolbars.
Finally, click the close button on the dialog and you will see your new
buttons label change to "nUnit" (or whatever you called this tool).

Great, you now have a button, that currently, won't do much. But just for the
heck of it give it a click. You will see some stuff fly by in your "output"
pane. If a command window pops up instead that is becuase you didn't check
"Use Output Window" when adding the custom tool. Go back and edit the custom
tool, check that option, then click the button again. Eventually you should
see some text appear in the output pane that looks something like this:




```sh
Tests run: 0, Failures: 0, Not run: 0, Time: 0.016 seconds
```






Ok we are almost ready to write a test and really get this party started.  However, before you do that you need to add a reference to nUnit to your project.  There are a couple ways to do this but I will go with the first one I discovered.  Open the "Project" menu and select the "Add Reference" option.  A new dialog will popup, within this dialog make sure the .NET tab is selected.  In the datagrid pane scroll down until you find "nunit.framework"  and select it. Then hit "OK"  So far this has been pretty painless hasn't it?


Next you need a test class to run. This is something I had trouble finding any examples of so I'm not going to go into great detail on how you should write your tests instead I'm going to give you some sample code.  This first is a class I want to test called AppSetting the second is my test harness which runs two tests against the only two public properties of my AppSetting class.




### AppSetting.vb


```vbnet

Public Class AppSetting


    Private displayName As String

    Private settingID As String


    Public Sub New(ByVal id As String, ByVal name As String)

        displayName = name

        settingID = id


    End Sub


    ReadOnly Property name() As String

        Get

            Return displayName

        End Get

    End Property


    ReadOnly Property id() As String

        Get

            Return settingID

        End Get

    End Property


    Public Overrides Function ToString() As String

        Return displayName

    End Function


End Class


```






### AppSettingTests.vb


```vbnet

Imports NUnit.Framework


<TestFixture()> _

Public Class AppSettingTests

    Private mAppSetting As AppSetting

    Private idval As String = "test234567"

    Private nameval As String = "test"


    <SetUp()> _

    Public Sub SetUp()

        mAppSetting = New AppSetting(idval, nameval)

    End Sub


    <TearDown()> _

    Public Sub TearDown()

        'nothing to do here

    End Sub



    <Test()> _

    Public Sub id()

        Assert.AreSame(mAppSetting.id, idval, "ID value loaded was " & mAppSetting.id & " and not the expected value of : " & idval)

    End Sub


    <Test()> _

        Public Sub name()

        Assert.AreSame(mAppSetting.name, nameval)

    End Sub

End Class


```





Once this is all in your project save, then "build", and finally hit the "nUnit" button again.  This will cause some new stuff to show up in the output window:




```

Tests run: 2, Failures: 0, Not run: 0, Time: 0.031 seconds


```






Great, they both passed.  If you want to see one fail just change one of the tests from Assert.AreSame to Assert.AreNotSame, build, and hit nUnit.  For instance I did that to the id() test and this was the result:





```
Tests run: 2, Failures: 1, Not run: 0, Time: 0.031 seconds


Failures:

1) testSettings.AppSettingTests.id : ID value loaded was test234567 and not the expected value of : test234567

Objects should be different

 both are: <"test234567">

   at testSettings.AppSettingTests.id()


```






That's about it.  If I figure out any other little "tricks" or how to create a full testSuite as per jUnit I'll post again with the details.





## Comments











Greg Finzer






Bill, I created a utility to create NUnit tests.  What features do you think would be useful to add?  Do you think MBUnit or XUnit will eventually replace NUnit?


http://www.kellermansoftware.com/p-30-nunit-test-generator.aspx











Bill






Because I was under the impression I would need the VS Team Edition (or whatever it is actually called) and we don't have that license.











Developer Books






Why don't you use the built in functionality in VS 2005? While it works similarly to nUnit, it has some advantages including the ease of setup.











Bill






Roger - your right that the syntax shown won't work becuase some of the code isn't being shown (I forgot to escape the brackets when I posted it).


However, the intent of this post isn't really to show how to write a test case as much as it is to show how to get nUnit to work with VS 2005.


I'll fix the code sample.











Roger Pearse






Out of the box this doesn't work.  Note all the orphaned underscores in your test case?  Your page is not displaying the nUnit attributes that precede them....!  Things like <TestFixture()>











Anonymous






It'd be helpful to add proper class attributes to the class definition and methods.











Anonymous






on click of button, open next window in vb.net










