---
layout: post
title: "Easy Form Validation"
date: 2006-07-31
comments: false
categories:
 - javascript
 - coldfusion
 - form-validation
 - validation
---

Validation is, without a doubt, the most important part of form
creation/processing. However, it seems, there are many "camps" on when and
where, within your code, a developer should validate form content. To that end
I figured I would share my method. It is built on a couple of premises. First,
that there is a "Bean" for every form. Second, that I want to validate both on
the client with JavaScript (or ECMAScript if you prefer that name) and again
on the server. The basic technique works just as well in Cold Fusion as it
does in Java. Though, truth be told, some of this is easier to
programmatically do in Cold Fusion than it is in Java (of course that could
be, in part, due to my lesser knowledge of Java).




Before I get into the details let me lay out a few ground rules or conventions
that I use. My bean property names map directly to the forms field names. For
example if I have a login form with a username and a password field then the
bean will have a username and a password property. Even though Cold Fusion
isn't case sensitive I typically keep all of this stuff in the same case as
well so that it is easy for me to transition between one project in CF and
another in Java. My "beans" are coincidental presentation-layer aware in that
they know the field names, and the CSS class that I will be using for the
fields in the form. However, this is due to convention again more than me
hard-coding class names in the "bean". Each property has a "type" associated
with it. For instance username has type of "Text" password has a type of
"Password", emailAddress has a type of "Email", faxNumber has a type of
"Phone", phoneNumber has a type of "Phone", etc. Most fields have a type of
text. This is because on both the server and the client not only do I have to
make sure the data is present, but I also have to make sure the data is valid.
So if you give me an email address I have to make sure it is, in fact, a
properly formatted email address before I ship it off to the persistence
layer. Because my validation techniques on the server and the client basically
mirror each other I don't' see any reason why the bean can't share this
information with the presentation layer. The easiest way for me to do this is
via the class attribute of the field.




The final standard item of note here is that every form that will be validated
has a hidden field it in called "requiredFields". The presence of this field
within the form tells my javascript that some validation needs to occur when
the user attempts to submit the form. This field is populated from the "bean"
for the form.




The rest of this article is going to be more of a step by step presentation of
how I apply the technique. At the end I will provide a download-able zip file
that contains the basic javascript and the Bean.cfc file for the server end.




For the sake of simplicity I am going to continue with the example of a login
form that has a username and a password field. This means I'll have a simple
Login.cfc that extends Bean:

```cfc
<cfcomponent name="Login" extends="Bean" hint="I represent the Login
form">
<cfset variables.instance = structNew() />
<cfset variables.instance.requiredFields = "username,password" />
<!--- a comma delimited list of fields that are required --->

<!--- bean properties --->
<cfset variables.instance.username = StructNew() />
<cfset variables.instance.username.value = "" />
<cfset variables.instance.username.type = "text" />

<cfset variables.instance.password = StructNew() />
<cfset variables.instance.password.value = "" />
<cfset variables.instance.password.type = "password" />

<cffunction name="init" output="false" returntype="Login" access="public"
hint="the constructor">
<cfargument name="username" type="string" required="false" default="" />
<cfargument name="password" type="string" required="false" default="" />

<cfscript>
setUsername(arguments.username);
setPassword(arguments.password);
return this;
</cfscript>

</cffunction>


<cffunction name="setUsername" output="false" returntype="string"
hint="">
<cfargument name="username" type="string" required="true" />
<cfset variables.instance.username.value = arguments.username />

</cffunction>
<cffunction name="getUsername" output="false" returntype="string"
hint="">
<cfreturn variables.instance.username.value />

</cffunction>

<cffunction name="setPassword" output="false" returntype="void" hint="">
<cfargument name="password" type="string" required="true" />
<cfset variables.instance.password.value = arguments.password />

</cffunction>
<cffunction name="getPassword" output="false" returntype="string"
hint="">
<cfreturn variables.instance.password.value />

</cffunction>


</cfcomponent>

```




As you can see I have defined that both username and password are required
values. I have also defined each property as a structure. Username will be of
type text while password will be of type password. This will be used as the
CSS class for the fields on the form, will be used by the javascript to
confirm the values are valid, and will be used by Bean.cfc to confirm the
values are valid on the server. Otherwise this is a pretty straight forward
bean.



As I build the form for display there are a few things that have to happen.
First, I need to initalize a Login.cfc object with any parameters that have
been passed in so that I can use the bean to populate the form and display any
error messages that might be associated with the bean (ie invalid values being
passed back).


```cfc
<cfset args = structNew() />
<cfset args.username = attributes.username />
<cfset args.password = attributes.password />
<cfset loginData = createObject("component","path.to.my.cfcs.Login").init(a
rgumentCollection=args) />

```


Now as I draw the form I can build each input type accordingly:


```cfc
<form method="post" action="" name="form" id="form">
...
<div class="#loginData.getRequiredOrOptional('username')#">
<label for="username">Username</label>
<input type="text" name="username" id="username"
class="#loginData.getFieldType('username')#" value="#loginData.getUsername()#"
title="username" />
</div>
...

<input type="hidden" name="requiredFields"
value="#loginData.getRequiredFields()#" />
...
</form>

```



I wrap each field in a div that has either a class of "optional" or
"required". These can be dynamically updated (if your form changes
requirements based on other form fields being filled in) as can the list in
the hidden "requiredFields" field. The presence of a "requiredFields" field in
a form tells my javascript to invoke it's magic because during the document
onload event a method runs titled

```js
function initializeForm(){

var rf = getObjectRefByID('requiredFields');
var theForm = getObjectRefByID('form');

if(rf && theForm){
rf = rf.value.split(',');
for(var i=0;i<rf.length;i++){
require(rf[i]);
}
}

if(theForm){
theForm.onsubmit = validateForm;
}
}

```



The functions require, getObjectRefByID, and validateForm are all in the
download and I'm not going to really talk about them much here; besides I
think you can probably guess what they do in general. At this point the form
is now drawn and has some unobtrusive javascript attached to it that will
cause the form to be validated when the user tries to submit it (assumign
Javascript is enabled). If the form fails the JS validation then an alert box
will appear telling the user there were errors and detailing those errors
using the "title" attribute of each invalid field. The wrapping div's class is
also updated to reflect the failure (and appropriate styles then take effect
to highlight the field). If the form validates then it is sent off to the
server where you can then use the built in validator within the bean to
determine if the data is really valid.




Once the form reaches the server we invoke the loginForm.cfc again, initialize
it with the form properties, then call it's validate method


```cfc
<cfset args = structNew() />
<cfset args.username = attributes.username />
<cfset args.password = attributes.password />
<cfset loginData = createObject("component","path.to.my.cfcs.Login").init(a
rgumentCollection=args) />

<cfif loginData.validate() >
<\--- go ahead and save the form using your persistence mechanism --- >
<cfelse >
<\--- save any error messages you need to and then send the user back to
the form --- >
</cfif>

```



One really easy way to do this is to have the form submit to itself then you
can either process the form or redisplay it as appropriate. Whatever technique
you want to use.



I will probably dedicate another post to how the Bean.cfc is built and how it
is able to generically validate pretty much every form you need. Granted, no
solution is prefect for 100% of the cases out there but this will work for
every standard form I have come in contact with; and even some crazy dynamic
forms that change requirements based on what the user chooses.



Look, by no way am I claiming this is the best way to handle form validation.
However, I think it is a good way. The accompanying source code isn't
commented very well; however, in general I think it is easy to read. I
extracted the Bean.cfc from a Java app I just wrote so it hasn't been tested
much. The zip file also includes a lame bean (login.cfc) to extend Bean.cfc
and a very, very simple usage example in beantest.cfm



Feel free to share your ideas, thoughts, suggestions, or even complaints with
this idea. I'll be refining the attached code overtime and may even include
some better examples as I go.


[Download the source](http://blog.rawlinson.us/documents/validate.zip)

