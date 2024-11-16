---
layout: post
title: "Sublime 3 alias at Windows Command Prompt"
date: 2014-08-20 08:12
comments: true
category: utility
tags: [sublime,text-editor,windows,alias]
---

**UPDATED 29 AUG 2014**

Sublime 3 Build 3059 has an windows command line helper named subl.exe.  You can bypass the below instructions and just add the Sublime3 install directory to your path to take advantage.  The numbered steps below basically show you how to add something to your path so use those for reference.

------


**Original Post**


I try out new editors all the time but I typically end up back at EditPlus 3 or Sublime Text (ver 3 at this point).  I also spend a lot of time at the command line and want to be able to edit files quickly using my text editor of choice (m).  On my Mac it was pretty easy to add the alias of `subl` to the terminal so I could quickly open a file by typing `subl <filename>` but doing the same in windows isn't a straight forward.  It's still fairly easy but I couldn't remember how to do it so now that I do I figured I'd record it for posterity sake.

First I created a directory at c:\dev\tools\aliases - this directory will hold all of the aliases I decide to define.  Within that folder I created a batch file named `subl.bat`  and in that batch file I entered:


```bat
@call "c:\dev\tools\Sublime3\sublime_text.exe" %*

```

Finally, and this is probably the most important step.  Add the directory c:\dev\tools\aliases to your system path.

   1. Right click on computer in start menu
   1. Click properties
   1. Click "Advanced system settings"
   1. Click on the "Advanced" tab
   1. Click on "Environment Variables" button
   1. Find the "Path" variable and double click it
   1. Go to the end of the "Variable Value" field
   1. add a semi colon to the end if there is already data in the field
   1. add c:\dev\tools\aliases
   1. Click OK
   1. Click OK again
   1. Click OK again
   1. Close your console windows
   1. Reopen a console window
   1. boom - you're done.  Now you can type subl <filename> and it will open sublime with the file in it for editing.

Sadly, from the gitbash control is not returned to the console until you close the editor.  I couldn't get it to return control to the window immediately using @call or start.

I found the `@call` syntax in a comment on [this blog post](https://coderwall.com/p/bn2inq).  The blog post does a pretty decent job of showing you how to define bash aliases in a .bashrc file.  However, the original post doesn't show you the trick of having control return to the bash prompt after launching sublime.  Basically, if you append an ampersand `&` to the command it wil return.


```sh
subl <filename> &

```


You can't put the & in the alias or else it will try to execute a bunch of commands based on the contents of the file you're trying to edit.  I just learned that from experience! Whoops.

Sadly, defining the alias batch file doesn't work in gitbash - and defining the alias in .bashrc doesn't work in windows console so you're stuck defining it in both places.
