---
layout: post
title: "Setting up Ubuntu 8.1 For Development"
date: 2008-10-30
comments: false
categories:
 - ruby
 - partition manager
 - linux
 - installation
 - gparted
 - sqlite
 - citrix
 - ubuntu
 - irb
---
I have to dual boot into Linux to do some ruby work. Sure, I **can** do most
of my dev work in windows but, to be honest, it doesn't work that well for all
of my ruby needs. For instance many Gems just won't build on windows
especially with my not having VC++ 6.0 installed. Thus, I have to have
something else to work in; enter Linux.

If you have been following along you'll know that last year (or earlier this
year) I attempted to setup a pure Linux dev environment but one of my projects
(a coldfusion+ms sql server 2005) forced me back to windows. So I went back to
a pure windows setup. Now, finally, I am compromising.

Fortunately my old posts helped me [get my citrix client setup](http://cf-
bill.blogspot.com/2008/05/ubuntu-i-wish-i-could-love-you.html) (though I had
some new issues with my display adapter). Here follows some tips that helped
me get over the hump of getting things installed and working as needed.


  * nVidia Adapter \- I actually had a lot of problems with this. I installed from a newly pressed Beta cd for Ubuntu 8.10 and activated the necessary driver; however no matter how hard I tried I couldn't get my video settings to save in the xorg.conf file properly. Fortunately a perusal of [a forum post](http://ubuntuforums.org/showthread.php?p=6050098) turned up the answer:


```sh

~$ sudo nvidia-xconfig

~$ gksudo nvidia-settings


```



The first line backs up the xorg.conf file and creates a new one that the nvidia driver can understand.  The second opens the settings dialog as super-user and lets you make your changes.  However, before doing this I had to update my system.  Even though I seemed to have the latest and greatest version of the drivers an update was required before my machine would boot with the nVidia settings.

  * synaptic package manager - for whatever reason synaptic just won't see all the software that is out there to install.  I've enabled all the different repos but synaptic shows me almost nothing.  Thankfully, the command line saves the day.  First, if you want to find something useful you can type



```sh
apt-cache search {item of interest}


```


Where {item of interest} is some string to search for.  Then you can use


```sh

sudo apt-get install {x}


```


Where {x} is the package to install.

  * irb - Once ruby was installed I couldn't get irb to run from the command line.  The problem was irb was called irb1.8 in /usr/bin so I created a symbolic link at /usr/bin/irb that points to /usr/bin/irb1.8 like so:



```sh
sudo ln -s /usr/bin/irb1.8 /usr/bin/irb

sudo chmod 755 /usr/bin/irb


```



  * sqllite for ruby If you try to use gem to install sqlite3-ruby it will bitch and moan. You have to use apt-get to install libsqlite3-ruby like so:



```sh
sudo apt-get install libsqlite3-ruby

```



Then anything you try to install that needs sqlite support should work OK.  Sadly, this was also a pain on windows; but thanks to the RubyOnRails wiki:



>
>     Grab <http://www.sqlite.org/sqlitedll-3_6_1.zip> and unzip the contents
to a location on your path. I use c:\ruby\bin.
>
>     Next, install the SQlite3 gem:
>
>     gem install sqlite3-ruby
>
>     Note, as of 30/08/2008 this can fail because the latest sqlite3-ruby gem
does not have a windows version. To get around this, install as so:
>
>     gem install --version 1.2.3 sqlite3-ruby
>




  * partitioning - Honestly, this should have been obvious but don't try to install while you have a large usb drive connected.  The partition manager takes forever to scan the external drive.  The partition manager is also pretty unclear with it's graphical display of what your partitions will look like so I used the manual option and setup a 2gb swap and a 13 gb linux partition mounted at /.  I don't need anything more complicated.







## Comments











A_J780






Thanks for the info,

 my Nvidia adapter has been buggy since my upgrade to 8.1 and this just fixed it


Thanks again !










