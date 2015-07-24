---
layout: post
title: "Visual Studio: Sharing one file between 2 projects"
date: 2007-10-05
comments: false
categories:
 - visual-studio
 - .net
 - c#
---
This may be old hat to some folks but for the others I hope you find it
useful; particularly when doing unit tests.  
  
I have a project we will call "MainApp" and another project "MainAppTest" that
is responsible for unit testing MainApp. Some of the classes I am testing
depend on some application configuration settings existing in the app.config
file of the MainApp - but I didn't want to have to keep a copy of app.config
in MainAppTest (if you don't have an app.config in the test project the app
settings won't be found when you try to load them).  
  
What to do? I don't want to copy app.config what I really want is for my test
project to "point" at the App.config in the MainApp project. It turns out this
is possible and actually pretty easy to do even if the option is a little
hidden.  
  
Using VS 2005 just right click on the project you want to add the file to,
select "Add -> Existing Item" and then browse for the file you want to
"point" to once the open file dialog appears. However, before you click the
"ADD" Button notice that on the right side of the button is a little arrow.
Click on it and you will get two options: "Add" and "Add as Link" - select the
second "Add as Link" option and you'll be good to go.  
  
Now the file will be included in your project but the file icon will have a
small arrow overlay.  
  
If you want to remove the file link from your project just right click on the
linked file, selected remove, and bam! You're done. The file will still exist
in the original project but it won't be in your alternate project anymore.  
  
Perfect

## Comments

Anonymous

In a Windows Forms project in VS2010 and Windows XP SP3, the little dropdown
does nothing.  
  
Clicking it clicks the entire button and the file is added to the project (not
a link to it).  
  
The file I am trying to link to is outside the "project tree".

Joe Meirow

This made my day, today. Thanks!!!

brian

Wow, super rad! I can't believe I never noticed that little arrow on the Add
button!  
  
Trying to keep a number of XML config files synchronized between projects was
a PITA.  
  
Thanks again!

Anonymous

Thanks, this made it easy.

Anonymous

THANK YOU SO MUCH THIS TOOK ME AGES TO FIND!

Anonymous

Thanks for the blog. It was very helpful.  
  
NOTE TO EVERYONE: The Link Dropdown Option on the Add button will not appear
when trying to place a linked file inside a Visual Studio WebSite It will work
in a Web Application.

Anonymous

The links are stored in the project file (.csproj or .vbproj). So if you check
in the project file and the other users have the original location project
then they should be fine.

Simon

I notice that the 'links' can't be checked in/out from source control so once
I've set this up in my project, how do I share this with other members of the
development team? - do they have to go through the same process locally?

AP

Awesome...Thanks to remind me again

Yasir

Hi,  
I did not see any option that u tell in VS2005 or VS 2008 can any one tell me
how this option is available ?

Anonymous

thanks ... saved me a lot of effort ... good work.

Kapil

Hi,  
This was quite simple to share Config files across projects.  
I hav query on this, In project solution I have to 2 Service class libraries
and are executable on its own which are having the AppConfig. Can I have
common AppConfig for those ?

AHT

Hi!  
  
Thanks for post. One more click and check As Link but very useful click =)

