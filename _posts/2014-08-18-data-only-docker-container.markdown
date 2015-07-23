---
layout: post
title: "Data Only Docker Container"
date: 2014-08-18 10:23
comments: true
categories: [docker,coldfusion, data]
published: true
---
This post is about creating a docker container that has data in it that other containers need to access.  You can use the exact same technique to connect a container that other containers would write to.  In this example I will just be reading from the data container.

In [my last post](http://code.rawlinson.us/2014/08/create-a-coldfusion-docker-container.html) I discussed setting up a container that runs a process (or two) for getting a ColdFusion server up and running.  The next container I needed, for rapidly getting an environment up and running, was one which just contained a variety of ColdFusion libraries that my applications and testing depend upon.  I'm a big fan of [mxunit](mxunit.org), [coldspring](https://github.com/markmandel/coldspring), and [FW/1](https://github.com/framework-one/fw1).  Most of the applications I build with ColdFusion use, at a minimum, mxunit - but there is a strong chance I'm also using coldspring and/or FW/1.  Therefore I wanted to be able to define a container that I could fire up and which would serve up those libraries by exposing them to the ColdFusion container.  ***NOTE*** This post just shows getting mxunit and coldspring. Adding FW/1 is an exercise for the reader or you can visit the [github repo](https://github.com/finalcut/docker-cflibs) to see the rest of the dockerfile.

This is probably the easiest container I'll ever build - but it was a little tricky to define initially becuase there were some aspects of how Docker builds a container that I didn't really understand when I started.  The biggest "gotcha" was using the [`VOLUME`](https://docs.docker.com/reference/builder/#volume) keyword in the [`Dockerfile`](https://docs.docker.com/reference/builder) too early.

Here are the guts of the `Dockerfile`.  I'll explain the particulars after.

```bat
FROM ubuntu:latest
MAINTAINER finalcut bill@rawlinson.us

ENV REFRESHED_AT 2014_08_18_1
RUN apt-get update
RUN apt-get install -y unzip

ADD https://github.com/markmandel/coldspring/archive/2.0-alpha1.tar.gz /var/cflibs/coldspring.tar.gz
ADD https://github.com/downloads/mxunit/mxunit/mxunit-2.1.3.zip /var/cflibs/mxunit.zip

WORKDIR /var/cflibs
RUN tar -xzf coldspring.tar.gz
RUN mv coldspring-2.0-alpha1/coldspring coldspring
RUN unzip -qq  mxunit.zip
RUN rm coldspring.tar.gz
RUN rm mxunit.zip
RUN rm -Rf coldspring-2.0-alpha1
VOLUME /var/cflibs

CMD ["/bin/sh"]
```

At the moment this container is based on the latest version of Ubuntu.  This is most certainly overkill.  I should (and will) switch to a much smaller base - I'm just not sure which one to use yet.


I do have to install unzip using apt-get so that I can unzip the mxunit archive file.  One cool thing I learned in building this is that I can point the [`ADD`](https://docs.docker.com/reference/builder/#add) command at a remote url and Docker will pull it down and put it wherever I tell it to (including using the name for the file I provide).  Previously I was using a bash script to fetch them first.  

After I download the libraries (using the versions I want) I extract them, move the contents around to suit my needs and then delete the cruft that remains.  For instance, I really just want the framework of coldspring and none of the other stuff so I copy the coldspring subdirectory up to my `WORKDIR` and then delete the rest of it.  I also get rid of the archive files.

Now here is where the big gotcha I hinted at earlier comes into play.  If you define the `VOLUME` before you do all the moving around of files none of your file operations will work - or some will but none will really work how you expect them to.  If you ever want to MOVE files around after they are in the container and you plan on exposing the `VOLUME` make sure you move the files before you use the `VOLUME` keyword.

Finally this container executes a bash shell but that isn't that important because; after you start the container you'll actually be stopping it.  This container does not need to still be running to be used!

When you execute a docker container it shows up in the list of running containers when you use the command `docker ps`.  

```sh
CONTAINER ID        IMAGE                          COMMAND             CREATED             STATUS              PORTS                            NAMES
7efb1a15c160        finalcut/coldfusion10:latest   /sbin/my_init       40 minutes ago      Up 40 minutes       8500/tcp, 0.0.0.0:8880->80/tcp   determined_wilson
```

When you stop the container however it doesn't really go away even though you don't see it if you run `docker ps` - instead you need to run `docker ps -a` to see the container still exists.  Because this file system container isn't executing any processes simply having the container exist is enough to make it usable.  


Thus I start up this container using the command:

```sh
docker run -i -t  --name cflibs finalcut/cflibs_mxunit_coldspring
```

The container immediately loads and presents me with a bash prompt.  I hit exit and that takes me out of the container and stops it - but the container continues to exist with the name "cflibs".

Now that my cflibs container exists I start up my coldfusion container using the `--volumnes-from` switch to tie the two containers together.

```sh
 docker run -d -p 8880:80 -v /var/www:/var/www --volumes-from cflibs finalcut/coldfusion10

```

The last step of this process is to execute a ColdFusion server initialization script that creates ColdFusion server mappings for the different libraries like so:

```cfm
<cfscript>
        mapObj = createObject("component", "cfide.adminapi.extensions");
        mapObj.setMapping("coldspring", "/var/cflibs/coldspring");
        mapObj.setMapping("mxunit", "/var/cflibs/mxunit");
</cfscript>
```

I could, just as easily, define those mappings as application specific mappings within the applications application.cfc file.  Because I also have to define a datasource using the administrative api of ColdFusion I am currently initializing the server with everything I need in one script.  I may change how I approach this as I learn more.


**Final Thoughts**

  * I probably shouldn't rename the folders the libraries are in within the data container.  Having the version identified in the folder is probably useful.  On the flipside having them always a consistent name makes maintaining the admin script that sets up the mappings much easier to maintain.
  * I don't use DI/1 or AOP/1 becuase I haven't.  They both look pretty slick and I'll certainly look at them for a future project.  Sean generally writes good stuff.
  * The main purpose of this post is to show how you can put stuff in a directory and muck with it and then expose that directory to other containers.  If my logic sucks feel free to comment or, better yet, submit a [pull request](https://github.com/finalcut/docker-cflibs)!
