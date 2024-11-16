---
layout: post
title: "What is Docker and Why do I Care?"
date: 2014-08-15 07:36
comments: true
category: [sysops]
tags: [linux, vagrant, containers, drone, continuous-integration,docker, coldfusion]
published: true
---
I've been hearing about Docker for a while now but never really got around to messing with it until this week when a coworker suggested I check out Drone.  Drone is a continuous integration server with tight integration with Docker.  Therefore, before I really dig into Drone I figured I should get a handle on Docker, what it is, and how to use it.  It turns out I was entering a pretty amazing realm and I'm glad I did.


If you're like me when I started out and you have no idea what a container is I would explain it as sort of a light-weight; super flexible; super fast to start; virtual machine (VM).  It isn't really a VM but it does have a complete copy of whatever OS you are putting in the container.  However, it runs in a process within your host machine.  The container is completely isolated (sand-boxed) from all other processes except if you EXPOSE ports between containers and link two or more containers together.

So why is that useful?  Well, in terms of continuous integration it seems super useful to me.  I do a lot of Cold Fusion (CF) development and getting dedicated hardware, even for distinct VMs is kind of a pain in the ass.  Plus, setting each one up is slow and then turning each one on has the overhead of a full system start.  It's just plain old slow and clunky.  However, with containers I can have a setup like this.  Container A -> Coldfusion Server,  Container B -> Oracle Server, Container C -> CF Libraries (MxUnit, ColdSpring, FW/1, etc), Host Machine -> File System with source code and Continuous Integration server (Drone).

Now, when Drone fires off the build what can happen is it will start the three containers A, B, C.  Container A is already setup with CF server and Apache on it with all the CF patches installed and datasource settings defined to point to Container B.  Container A also has a mount on it that points directly to Container C's library paths and another mount for the Host source code directory.  Basically as soon as all the containers are started a fully working development/testing environment exists for my Coldfusion Application.  I also know that due to the image that the database container was built on (I'll explain images more later) the database is in a perfect state for beginning my tests.  Drone then fires off the ant task in my build script to run all my mxunit tests against my CF source code.

Those unit and integration tests probably make a bunch of changes to the database which are not easy to reverse.  No problem though because the next time the test enviroment is started up (which happens insanely fast) the database is right back to it's clean state.  

Now, let's say I wanted to deploy the application and database into a new production server.  If I've already defined these containers properly then that's as easy as deploying a copy of Containers A, B, and C onto the production server and then checking out the source.  An entire production server is then up and running.  I didn't have to provision three new VMs and I don't have to worry about hardware utilization where I have different versions of my standard CF libraries running for different applications on the same server.  The application I'm running know has it's own clean copy of each library thanks to the library container (C).

Did a new developer join your team and you have to get them setup with all the tools and development copies of the site?  No problem, install docker and give them the containers.  Bam!  That new developer is ready to work and she didn't have to do anything.  It's really that simple.

I realize I'm barely touching the surface of what containers can do - but I really just did start learning about them.  My next post will be more technical and will explain how I am setting up a container with ColdFusion 10 installed and patched up to patch 18; plus where it has the datasource settings defined.  Once I get that container built I'll then try to explain how to set one up with Oracle Server 11(g?) on it.  THen, finally, I'll try to get Drone working with these various containers running my unit tests.
