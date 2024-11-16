---
layout: post
title: "My Virtual Machine Hell"
date: 2009-01-23
comments: false
categories:
 - virtual-machine
 - cruisecontrol.rb
 - vm
 - virtualization
 - ubuntu
---
Normally when I first hear about a new technology I jump right on it. I am
always installing new software to try things. Yet, for some reason I have
never installed a virtual server technology. I've never done anything with any
virtual machines. Heck, in [ma.gnolia.com](http://ma.gnolia.com/people/finalcu
t/tags/virtualization%20vmware%20development%20server) I have had the link to
the free version of VMWare server bookmarked for almost 3 years but until this
week I had never even tried to install it. What's up with that?  
  
As I mentioned in my prior blog posting however I have decided to dive into
the land of virtual machines. My first effort was to download and install
[VMWare Server 2.0](http://www.vmware.com/download/server/). It is a pretty
sizable download and it runs via a web-interface and is built upon tomcat. It
is kind of a beast. I installed it and got it running but it was painfully
slow for me. Then, when I tried to connect to my virtual machine from within
Chrome I was told to download and install a plugin but the whole server seemed
to crash. Also, the normal instructions for a VMWare image didn't work
(clicking on the .vmx file) Instead I had to copy the image files into a
directory under the "virtual machines" directory created by VMWare Server.  
  
After the crash I decided to uninstall VMWare Server 2.0 and try something
else. I had thought about checking out VirtualBox when I had installed Ubuntu
on it's own partition so I decided to see if a version existed for windows and
sure enough one did. So I installed it and then installed Ubuntu inside a new
VM. Well, I tried to. It took me about 3 or 4 efforts to get the install to
actually work. And when I say installs that means re-installing VirtualBox as
well. Heck, VirtualBox itself just seemd to hang on installing a few times.
Finally I managed to get Ubuntu 8.1 installed but any interaction with it was
painfully slow and laggy. I also couldn't work with it in anything greater
than 800x600 resolution (though I didn't get to try the guest user tools). I
tried to update the ubuntu install but it took over 13 hours to not even
complete the update download (on a strong connection) so I finally aborted and
decided to try something different.  
  
A co-worker had a copy of [VMWare Server
1.8](http://www.vmware.com/download/server/) handy that I decided to install.
It isn't webbased and a few other co-workers have had some good luck with it.
It installed without a problem and the [ubuntu
image](http://chrysaor.info/?page=ubuntu) I already had worked just fine. Now
I'm finally able to start working with Ubuntu inside my VM so I can begin to
dig into CruiseControl.rb - I will detail how I get that all setup in a later
post. Stay Tuned.

