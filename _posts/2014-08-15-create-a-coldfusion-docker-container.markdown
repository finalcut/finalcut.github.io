---
layout: post
title: "Create a ColdFusion Docker Container"
date: 2014-08-15 08:23
comments: true
category: [coldfusion, docker]
featured: true
published: true
---
All of what I did in this post is based on the prior work of Peter Bücker and his [GitHub repo](https://github.com/naag/docker-coldfusion11) so a big thanks to him.  Also, if I can I'll put the container on docker's repo site so others can download it and use it without having to recreate all of these steps - I'm just not sure I'm allowed to considering how hard Adobe makes it for you to download the ColdFusion Server binary as a developer.

First off you probably want to clone my [GitHub repository](https://github.com/finalcut/docker-coldfusion10).  But what I'm going to explain here is what I changed from the Peter Bücker repo to get mine to work.


***NOTE*** I used vagrant to set up a virtual machine to work on.  I don't know how to get any of this stuff to work on windows.  I'm using Ubuntu 14.04 to build everything in VirtualBox but I downloaded the ColdFusion binary to my windows machine.


1.  Download the binary from Adobe and put it on your network where it is accessible.  You need to do this so the prepare.sh works.  Once you login to the Adobe site you can get the relevant binary from http://trials3.adobe.com/AdobeProducts/CSTD/11/linux64/ColdFusion_11_WWEJ_linux64.bin  - just change the CSTD/11/ to CSTD/10/ if you want CF 10 and change the 11 in the bin file to 10.  Like so: http://trials3.adobe.com/AdobeProducts/CSTD/10/linux64/ColdFusion_10_WWEJ_linux64.bin
2.  Also download the patch files from adobe.  Here is the [mandatory patch](http://download.macromedia.com/pub/coldfusion/10/cf10_mdt_updt.jar) and here is the [hotfix 13](http://help.adobe.com/en_US/ColdFusion/10.0/Admin/WSe61e35da8d318518-33adffe0134c60cd31c-7ffe.html) file.
2.  Update prepare.sh to point to your ColdFusion binary.
3.  Edit the DockerFile - this file tells Docker how to create your container.  It is the recipe!  I had to add two commands to get my docker build to work properly.

```sh
RUN chmod -R 755 /etc/service/coldfusion10
RUN chmod 755 /tmp/install-cf10.sh

```

4. Find all references to CF 11 and update them to CF 10 in all files.
5. I also renamed any files that mentioned 11 to mention 10.


That was basically it.  Thankfully Peter had already figured out the tricky stuff like turning off ColdFusion admin security during the install phase!  I am not sure I ever would have thought of that.


When you go through the steps in the readme.md file basically what happens is:


1. The ColdFusion binary is downloaded to your working directory when you run `./prepare.sh`
2. The command `docker build -t cf10 .` builds the container.  The -t says "tag this container with the name cf10".  The `.` is just the path saying build the container right here.
3. While the build process is running it basically executes the steps listed in the DockerFile.  Here are what the steps in my DockerFile do
  1. `FROM phusion/baseimage:0.9.9` - this specifies the image that this container will be based on.  The image is named using a convention of author/image_name.  The :0.9.9 is the tag of the image.  You can actually find the phusion/baseimage at the [docker hub](https://registry.hub.docker.com/u/phusion/baseimage/).  Basically an image is a pre-existing container.  A cool thing about these containers is you can make one, change it, then COMMIT the change and that will create a new container image that you can build off of in the future (or use as your container as needed).  This step downloads the base container and sets it up for the rest of the steps.  At this point you have a container running Linux in it!
  2. `MAINTAINER finalcut` - so the maintainer just says who is building this container and who is responsible for updating it.  Make sure you change this if you create your own container.  I use the name finalcut as an alias on a lot of services so finalcut is me.
  3. `EXPOSE 80 8500`  - this exposes the ports 80 and 8500 to other containers.  You can't just connect to these ports publicly thanks to EXPOSE in order to do that you'll need to use some switches when you RUN the container later.  Most of the time you don't want the ports open publicly so this is the way to open a port to another container.
  4. `ENV DEBIAN_FRONTEND noninteractive` - ENV sets an environment variable in the container's OS to the value.  So here we've set the environment variable of DEBIAN_FRONTEND to the value noninteractive.  Honestly, I don't know enough about linux to know why this environment variable is being set.  I'm just trusting Peter on it.  I suspect this makes sure the ColdFusion installer doesn't launch a GUI later but I'm not sure.
  5. `RUN apt-get update` - I know enough about Linux to know this one.  It updates any packages in the container.  Remember the container contains a full clean version of linux so it should be up to date.
  6. `RUN apt-get install -y wget unzip xsltproc apache2`  - Installing some stuff we need; most notably apache2 which will be the web server that ColdFusion will be configured to run with.  I wish we could install ColdFusion with apt!
  7. `ADD ./build/install/ /tmp/` ADD basically copies whatever is at the source to the target.  So in this case the source is `./build/install/` and the target is `/tmp/` in the container.
  8. `ADD ./build/service/ /etc/service/` copying some more files.  This works recursively so here both the apache2 and ColdFusion10 directories will be copied over.
  9. `RUN chmod -R 755 /etc/service/coldfusion10` - RUN executes an arbitrary command within the container.  I neeed to change permissions on the ColdFusion10 directory we just copied over otherwise later on you get some permission denied problems while trying to start ColdFusion when the container starts.
  10. `ADD ./build/my_init.d/ /etc/my_init.d/`  copying another file.  This is a script that gets executed when linux first starts I think.  I don't actually have a ColdFusion configuration file that gets copied over so my script really doesn't do anything.  I'm not entirely sure what a ColdFusion configuration package would contain so hat-tip to Peter for including this.  I'm sure it is useful.  Hopefully I'll figure out how useful soon!
  11. `RUN chmod 755 /tmp/install-cf10.sh` this script needs permissions to execute so I'm giving them otherwise ColdFusion won't get installed and that would suck.
  12. `RUN sudo /tmp/install-cf10.sh` install ColdFusion.  There are actually a bunch of steps in that file.  It is pretty well commented so I'll leave understanding of it to you.  If you have a question just leave a comment and I'll try to answer it.

***NOTE*** the file *build/install/installer.profile* contains answers to questions that ColdFusion will ask during install.  The most important one to remember is the **SILENT_ADMIN_PASSWORD** - you'll need to know that if you want to set admin settings later.  This setup will not expose the CFIDE/administrator directory so you'll have to set all admin properties using the [CF admin API](http://help.adobe.com/en_US/ColdFusion/10.0/Admin/WSc3ff6d0ea77859461172e0811cbf364104-7fcf.html).


Okay, so at this point you have a container that has linux running apache2 with ColdFusion 10 updated to patch 13.  Not too bad.

At this point you'd probably like to test your container.  Well the last step of the readme.md file shows you how to start it.


```

docker run -d -p 8880:80 -v /var/www:/var/www cf10

```


This runs it as a daemon (-d) and makes port 80 in the container available on port 8880 of the host machine.  It also mounts /var/www on the host machine as /var/www on the container.  This way you can edit your source files on the host without having to connect via ssh to the container (we didn't open the ssh port so this works out great).

On your host machine go to /var/www and then create an index.cfm file.  Inside the file just stink in

```

<cfdump var="#server#">

```


That will dump out some ColdFusion server information.  Note the product version is `10,0,13,287689` which indicates hotfix 13!  Great work!

At this point you're basically done creating your container.  You've got a great CF 10 image to work with.  Now, for each project you can do some ColdFusion initialization
and then do a DOCKER COMMIT on the initialized image to save it for your specific needs.  For instance, lets say you have a database driven project.  You can create a quick ColdFusion script that sets up your datasource in the admin api, and the client storage if you need it.  After running the ColdFusion script you can then do `docker commit -m 'added datasource info for project X' cf10 finalcut/cf10:projectx`

That will create a new container based on your ColdFusion container that is specifically setup for projectX.  My next blog post will talk about how to integrate your projectX container with another container that contains ColdSpring and MxUnit and FW/1 (or whatever other ColdFusion framework libraries you might use).  THis other contianer won't have ColdFusion installed on it or apache. It will just be a data container.
