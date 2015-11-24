---
layout: post
title: "Command Line FTP"
date: 2007-08-01
comments: false
category: general
tags: [windows,unix,utilities]
---
I was just browsing an article about a guys [frustration with command line
ftp](http://blogs.balliauw.be/blogs/maarten/archive/2007/06/14/commandline-
ftp-folder-download.aspx) options and I wanted to leave him a comment but
couldn't so I 'm posting here for anyone interested.  

There is a [free library full of great and useful *nix
commands](http://unxutils.sourceforge.net/) for windows that are all just
freestanding executables. You download the library, plop the library in your
path, and bam! you can do all sorts of cool stuff such as the other guys
request to do recursive ftp downloads from the command line (using wget).  

wget -r ftp://user:password@host/path/to/directory/to/download  

You don't have to provide the username and password if you are connecting to
an anonymous ftp resource. wget is also useful for copying an entire website
down to your local machine.  

The entire library is very easy to use and well documented. I have been using
this library for years and it is fantastic. I miss it when I don't have it
available. Overall it is a great "compromise" between having cygwin or nothing
at all so if you need some handy command line tools I suggest you check it
out.

## Comments

uxintro

I know this is a bit late, but this is a great tip.  

I just used it to download my entire web page to a new server. Made use of my
SSH connection and the two web host's fat pipe, rather than uploading from smy
computer!  

Thanks. This is one is going straight to del.icio.us.
