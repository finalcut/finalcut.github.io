---
layout: post
title: "Closing Tag Requirements of ColdFusion"
description: "Code that shows the closing tag requirements of all standard ColdFusion tags"
headline:
date: 2015-11-20 10:19:45 -0500
category: development
tags: [lucee,coldfusion]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
I use Atom as my primary code editor of late and one thing I really like in it is the automatic code beautification of atom-beautifier.  It works great on my html and javascript projects.  However, that cool feature isn't extended to ColdFusion.  Fortunately, [Austin Cheney](https://github.com/prettydiff), the guy who maintains the library that actually does the beautification [showed a willingness to implement a beautifier for CF](https://github.com/prettydiff/prettydiff/issues/158) if someone would just tell him what the rules were for the various tags in regards to them needing to be closed.

There are three different tag types in CF - those that `require` an end tag, those that have an optional (`free`) end tag, and those that can not (`prohibited`) have an end tag.

Those tags with an optional end tag can be ended in any of the following three ways:

```cfm
<cfstoredproc>
<cfstoredproc />
<cfstoredproc></cfstoredproc>
```

The other two categories are pretty self explanatory.

I tried to manually go through the list of tags at [CFDocs](http://cfdocs.org/tags) but that was prone to mistakes on my part.  [Adam Cameron](https://twitter.com/DAC_dev) on twitter recommended I get help from [Dom Watson](https://twitter.com/dom_watson) and Dom pointed me to two helpful lucee functions; [`getTagList`](http://docs.lucee.org/reference/functions/gettaglist.html) and [`getTagData`](http://docs.lucee.org/reference/functions/gettagdata.html) which, when combined, provided me with the answers I needed.


**PROTIP** If you don't have lucee installed you can put together quick cf scripts to run against all of the main CF engines at [http://trycf.com/](http://trycf.com/) - that's how I ran this code.


Here is the code I used to get a definitive list:

```cfm
<cfset tags = GetTagList() />


<cfset bodies = structNew() />
<cfset namespace  = "cf" />
<cfset tags = tags[namespace] />
<cfset maxLength = 0 >


<cfloop list="#StructKeyList(tags)#" index="tagname">
    <cfset tag = getTagData(namespace, tagname) />

    <cfif not structkeyExists(bodies, tag.bodyType)>
        <cfset bodies[tag.bodyType] = ArrayNew(1) />
    </cfif>

    <cfset ArrayAppend(bodies[tag.bodyType], tagname)>


</cfloop>


<cfoutput>
    <table>
        <tr>
            <cfloop list="#structKeyList(bodies)#" index="key">
                <th>#key# end tag</th>
                <cfif ArrayLen(bodies[key]) GT maxLength>
                    <cfset maxLength = ArrayLen(bodies[key])>
                </cfif>
                <cfset ArraySort(bodies[key], "text", "asc")>
            </cfloop>


            <cfloop from="1" to="#maxLength#" index="i">
                <tr>
                    <cfloop list="#structKeyList(bodies)#" index="key">
                        <td>
                            <cfif ArrayLen(bodies[key]) GTE i>
                                #bodies[key][i]#
                            <cfelse>
                                &nbsp;
                            </cfif>
                        </td>
                    </cfloop>
                </tr>
            </cfloop>
        </tr>
    </table>
</cfoutput>

```

And here is the final result:

<table class="table">
  <tbody>
    <tr>
      <th>required end tag</th>
      <th>free end tag</th>
      <th>prohibited end tag</th>
    </tr>
    <tr>
      <td>
        case
      </td>
      <td>
        _
      </td>
      <td>
        abort
      </td>
    </tr>
    <tr>
      <td>
        catch
      </td>
      <td>
        ajaximport
      </td>
      <td>
        applet
      </td>
    </tr>
    <tr>
      <td>
        component
      </td>
      <td>
        ajaxproxy
      </td>
      <td>
        application
      </td>
    </tr>
    <tr>
      <td>
        defaultcase
      </td>
      <td>
        cache
      </td>
      <td>
        argument
      </td>
    </tr>
    <tr>
      <td>
        execute
      </td>
      <td>
        chart
      </td>
      <td>
        associate
      </td>
    </tr>
    <tr>
      <td>
        finally
      </td>
      <td>
        chartseries
      </td>
      <td>
        authenticate
      </td>
    </tr>
    <tr>
      <td>
        form
      </td>
      <td>
        content
      </td>
      <td>
        break
      </td>
    </tr>
    <tr>
      <td>
        function
      </td>
      <td>
        div
      </td>
      <td>
        chartdata
      </td>
    </tr>
    <tr>
      <td>
        graph
      </td>
      <td>
        document
      </td>
      <td>
        col
      </td>
    </tr>
    <tr>
      <td>
        if
      </td>
      <td>
        documentitem
      </td>
      <td>
        collection
      </td>
    </tr>
    <tr>
      <td>
        interface
      </td>
      <td>
        documentsection
      </td>
      <td>
        continue
      </td>
    </tr>
    <tr>
      <td>
        lock
      </td>
      <td>
        dump
      </td>
      <td>
        cookie
      </td>
    </tr>
    <tr>
      <td>
        login
      </td>
      <td>
        file
      </td>
      <td>
        dbinfo
      </td>
    </tr>
    <tr>
      <td>
        loop
      </td>
      <td>
        htmlbody
      </td>
      <td>
        directory
      </td>
    </tr>
    <tr>
      <td>
        mail
      </td>
      <td>
        htmlhead
      </td>
      <td>
        else
      </td>
    </tr>
    <tr>
      <td>
        mailpart
      </td>
      <td>
        http
      </td>
      <td>
        elseif
      </td>
    </tr>
    <tr>
      <td>
        output
      </td>
      <td>
        invoke
      </td>
      <td>
        error
      </td>
    </tr>
    <tr>
      <td>
        query
      </td>
      <td>
        layout
      </td>
      <td>
        exit
      </td>
    </tr>
    <tr>
      <td>
        savecontent
      </td>
      <td>
        layoutarea
      </td>
      <td>
        feed
      </td>
    </tr>
    <tr>
      <td>
        script
      </td>
      <td>
        map
      </td>
      <td>
        flush
      </td>
    </tr>
    <tr>
      <td>
        select
      </td>
      <td>
        mapitem
      </td>
      <td>
        forward
      </td>
    </tr>
    <tr>
      <td>
        silent
      </td>
      <td>
        mediaplayer
      </td>
      <td>
        ftp
      </td>
    </tr>
    <tr>
      <td>
        static
      </td>
      <td>
        module
      </td>
      <td>
        graphdata
      </td>
    </tr>
    <tr>
      <td>
        stopwatch
      </td>
      <td>
        pageencoding
      </td>
      <td>
        header
      </td>
    </tr>
    <tr>
      <td>
        switch
      </td>
      <td>
        pdf
      </td>
      <td>
        httpparam
      </td>
    </tr>
    <tr>
      <td>
        table
      </td>
      <td>
        processingdirective
      </td>
      <td>
        image
      </td>
    </tr>
    <tr>
      <td>
        timer
      </td>
      <td>
        setting
      </td>
      <td>
        imap
      </td>
    </tr>
    <tr>
      <td>
        transaction
      </td>
      <td>
        storedproc
      </td>
      <td>
        import
      </td>
    </tr>
    <tr>
      <td>
        try
      </td>
      <td>
        thread
      </td>
      <td>
        include
      </td>
    </tr>
    <tr>
      <td>
        while
      </td>
      <td>
        trace
      </td>
      <td>
        index
      </td>
    </tr>
    <tr>
      <td>
        xml
      </td>
      <td>
        videoplayer
      </td>
      <td>
        input
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        window
      </td>
      <td>
        insert
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        zip
      </td>
      <td>
        invokeargument
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        ldap
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        location
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        log
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        loginuser
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        logout
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        mailparam
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        object
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        objectcache
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        param
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        pdfparam
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        pop
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        procparam
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        procresult
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        property
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        queryparam
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        registry
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        rethrow
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        retry
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        return
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        schedule
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        search
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        servlet
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        servletparam
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        set
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        sleep
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        slider
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        throw
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        update
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        video
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        videoplayerparam
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        wddx
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        x_
      </td>
    </tr>
    <tr>
      <td>
        &nbsp;
      </td>
      <td>
        &nbsp;
      </td>
      <td>
        zipparam
      </td>
    </tr>
  </tbody>
</table>