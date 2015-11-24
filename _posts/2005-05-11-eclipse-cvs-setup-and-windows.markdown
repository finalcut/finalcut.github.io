---
layout: post
title: "Eclipse, CVS setup and Windows"
date: 2005-05-11
comments: false
category: Java
tags: [eclipse,cvs,windows,version-control]
---
Minor Update: The following will probably only work if you don't have a
password protected private key file.

This may work on any platform but I can only confirm it works on a Windows XP
machine.

I recently reinstalled Eclipse (it was doing something wierd) and in so doing
I had to reconfigure it to work with our CVS server. Honestly, I don't use
Eclipse that much - I actually use EditPlus (with Tortoise CVS) for almost all
of my development because it is lightweight and has columnar select. However,
I do like Eclipse and really WANT to use it. CFEclipse is pretty darn
impressive.

So, in another effort to embrace Eclipse I tried to get it to work with our
CVS server. I had done it before but couldn't remember the exact right steps.
Thankfully I found a [blog
post](http://www.gnegg.ch/archives/eclipse_cvs_and_putty.html) that helped and
I got back up and running.

However, it requires that I use pageant in order to keep my private key in
memory. I I prefer not having to do that. Fortunately I was able to modify the
settings at gneggs blog to bypass the need for pageant! Here is how its done:


```sh
under Window/Preferences/Team/CVS/Ext Connection Method:  CVS_RSH|
`your\full\path\to\plink.exe`
---|---
Parameters| `-1 -i your\full\path\to\your_private_key user@host`
CVS_SERVER| `cvs`
```


The `-1 -i ``your\full\path\to\your_private_key`` is the key. The -1 says I'm
using ssh1 I think you need -2 if your key was generated using ssh2. If your
not sure try -1 and if it doesn't work, try -2.



Then you add a repository in the repository-view using the following settings:


```sh
Host| `your.host.name`
---|---
Repository path| `/path/to/repos`
User| `username`
Password| empty
Connection type| ext
```


If you have NEVER connected to your repository with another tool before you
will have to fire up plink or putty and connect in order to add the
repositories key to your "key database". Ideally you should read [the post at
gneggs blog](http://www.gnegg.ch/archives/eclipse_cvs_and_putty.html) to get
started then come back here once you have it working with pageant. Just make
sure you shut down pageant when your testing the key option `-1 -i
``your\full\path\to\your_private_key `otherwise you'll get a false positive
success.

## Comments

Bill

I'm not sure why you aren't seeing the labels. So long as my project is
associated with a CVS directory I see a different set of icons near each file.

I get a > for files that are changed, a padlock for locked files, ? for files
that aren't in the repsitory. A padlock with a red dot for readonly files

at the end of each file, in parentheses, it shows my (ASCII -kkv) or whatever
flags are appropriate.

I setup my label decorations under the preferences->team->cvs->label
decorations screen. There are three tabs and I went through and configured
them to my liking.

I hope that helps

Anonymous

It is working. But the files and directories are not showing any labels. Now
in Java perspective or any other perspective there is no way to identify which
one is the added file and which is not. How can I solve this ?

Albin Joseph
