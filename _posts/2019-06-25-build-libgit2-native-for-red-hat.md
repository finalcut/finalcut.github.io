---
layout: post
title: "Build Native LibGit2 for Red Hat/Centos"
date: 2019-06-25
category: Programming
tags: [oop,linux,git]
comments: true
featured: true
---
Today I was trying to deploy a project that uses dotnet core to a Red Hat Enterprise Linux box.  The project had a dependency on libgit2sharp which has a dependency on a native verson of libgit2 which meant I had to build one.

To be frank, I don't know anything about building stuff on a linux box.  So I did a bunch of digging and looking around and running into problems until I came up with this short and relatively easy solution to the problem.

```sh
# install the tools
sudo yum install git cmake powershell gcc gcc-c++ glibc-static openssl-devel
# checkout the repository
git clone --recursive https://github.com/libgit2/libgit2sharp.nativebinaries
# move into the repo directory
cd libgit2sharp.nativebinaries
# run the powershell script to change to the correct commit hash specified by libgit2sharp
pwsh UpdateLibgit2ToSha.ps1 572e4d8
# build it.
./build.libgit2.sh
```

When I was done the desired file was in the project subdirectory `libgit2/build` and had the filename `libgit2-572e4d8.so`

I put this in my dotnet project (which is deployed as a self-contained application).  in order to add this to my projet I put it in my default projects root directory in the following structure:

`{root of project}/runtimes/rhel-x64/native/libgit2-572e4d8.so`  Then I made sure the file was included in the project and was to be copied if newer to the build output directory.

Once all of that was done everything worked fine.
