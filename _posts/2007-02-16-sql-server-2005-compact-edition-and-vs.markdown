---
layout: post
title: "Sql Server 2005 Compact Edition and VS 2005 Tools"
date: 2007-02-16
comments: false
categories:
 - sql
 - compact-edition
 - visual-studio
 - sql-server-2005
---
Today I needed to install the Sql Server 2005 Compact Edition SDK and the Sql
Server 2005 Compact Edition Tools for Visual Studio 2005 (sp1), ugh, what a
mouthful. Anyway, I made sure I had installed VS 2005 SP1, and that the smart
devices SDK directory existed, and then tried to install the tools for the
Compact Edition of SQl Server. It failed with this error message:  
  

>  
"The upgrade patch cannot be installed by the Windows Installer service
because the program to be upgraded may be missing, or the upgrade patch may
update a different version of the program. Verify that the program to be
upgraded exists on your computer and that you have the correct upgrade patch."

  
  
Annoying to say the least considering I hadn't installed any of the Compact
Edition stuff in the past (and I had, what appeared to be, all of the
prerequisites installed (based on the shoddy documentation at the download
page). It turns out that in order to install this patch file,
SqlServerCE31VSTools-ENU.exe, you first need to install an extra from the
Visual Studio 2005 DVD.  
  
You need to go to "X:\vs\wcu\SQLCE", where x is your dvd drive letter, and
install sqlmobile30devtoolsenu.msi first. Once that is installed the upgrade
will install fine. A bunch of people were reporting that they were
uninstalling VS 2005 and then reinstalling the whole thing so hopefully this
will spare some of you that pain.

## Comments

Anonymous

tanks!!

Phylter

It was very helpful. Thanks.

Anonymous

Thanks !!! I've been stuck on this error for hours installing every service
pack going.

Anonymous

Wish I had found this sooner... I just reinstalled the whole thing... :-P

Anonymous

Me too! Thanks!!!

Anonymous

Appreciate the info. It certainly helped me out.

