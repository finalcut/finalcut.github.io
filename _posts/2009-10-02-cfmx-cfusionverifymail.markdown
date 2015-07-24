---
layout: post
title: "CFMX CFUSION_VERIFYMAIL"
date: 2009-10-02
comments: false
categories:
 - coldfusion
 - smtp
---
This isn't really a feature I've needed much but I thought it might be useful
to share if anyone else ever needs it.  
  
Basically, a long time ago, Coldfusion had [a little secret function](http://w
ww.houseoffusion.com/cfdocs1/cf45/Administering_ColdFusion_Server/10_Configuri
ng_Advanced_Security/admin1018.htm) called CFUSION_VERIFYMAIL which was used
to verify the smtp server was available to CF. Once ColdFusion became
ColdFusion MX that function went away and I never thought about it again.  
  
Well, today I wanted to do something very similar but I wasn't sure what to do
so I searched for my old hidden function and [found a forum thread](http://www
.mail-archive.com/cf-talk@houseoffusion.com/msg98345.html) that offered the
basics of a solution. Well technically it is the solution but it just wasn't
as complete as I wanted it so I fluffed it just a touch and now I offer to you
as a resource should you need it.  
  
  
```cfm  
<cffunction name="mailServerIsUp" returntype="boolean" access="public">  
<cfargument name="smtp_server" type="string" default="" />  
<cfargument name="smtp_port" type="numeric" default="0" />  
<cfargument name="timeout" type="numeric" default="10" />  
<cfargument name="service" type="any" default='#createObject("java",
"coldfusion.server.ServiceFactory")#' />  
  
<cfset arguments.service = arguments.service.getMailSpoolService() />  
  
  
<cfif LEN(arguments.smtp_server)>  
<cfset arguments.service.setServer(arguments.smtp_server) />  
</cfif>  
<cfif VAL(arguments.smtp_port)>  
<cfset arguments.service.setPort(VAL(arguments.smtp_port)) />  
</cfif>  
  
<cfset arguments.service.setTimeout(VAL(arguments.timeout)) />  
  
<cfreturn arguments.service.verifyServer() />  
</cffunction>  
```  
  
I've tried to make the function fairly flexible (in case you already keep a
copy of the service factory in your application scope or something plus I
wanted to make sure you could point at your own applications mailserver/port
if you need to OR it will just use the default server settings.  
  
Finally, I had to change the name of the function becuase CF was throwing an
error if I tried to call that old hidden functions name. Plus, I think
verifymailserver is more clear than just verifymail. I just left the cfusion_
on the front as a hat tip to the original.  
  
Obviously this can be improved by adding some exception handling - especially
in regards to determining if the arguments.service passed in is the correct
object type; but I'll leave that to others.

