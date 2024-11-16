---
layout: post
title: "Ant Properties File Based on Windows Username"
description: "If you login with a azure active directory account to a windows machien your username will contain a slash and ant cant handle that.  Here is the fix."
date: 2018-05-14
category: windows,development
tags: [windows,development]
comments: true
featured: false
---
I have an ant build file that loads custom configuration settings based on the developer working on the project.  This file is loaded based on the developers windows login name.  So if it is `bobross` there is a file called `bobross.properties` in the directory alongside the build.xml file.  But, we have started to migrate to using Azure Active directory with our machine logins and when you login your username ends up being `azuread\bobross`  that slash really causes some problems since that is the windows directory delimiter.  Ant hates the slash and won't load the file.  Fortunately, there is a solution - regex to the rescue.

Before importing the properties file I have the following ant logic near the top of the build file:

```ant
    <loadresource property="username">
        <propertyresource name="user.name"/>
        <filterchain>
            <tokenfilter>
                <filetokenizer/>
                <replaceregex pattern=".*\\" replace="" />
            </tokenfilter>
        </filterchain>
    </loadresource>

    <import file="base_build.xml" />
    <property file="${username}.properties" />
```


