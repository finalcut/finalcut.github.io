---
layout: post
title: "Angular ng-options Specify The Value"
description:
headline:
date: 2016-01-11 11:15:21 -0500
category: development
tags: [angular1.x,angular,ngoptions,javascript]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
I have more trouble remembering how the syntax of ng-options works than I really
want to admit to publicly - but if i don't then the need for this post won't be
evident.  So, here it is.  I am horrible with ng-options.

There are basically two use cases that I need to remember for ng-options. The first
is the easier of the two for me.  I have an object with a child object.  The
`select` will be used to change the value of the child object.  Here is an example:

```html
<select ng-model="ctrl.model.childObject"
      ng-options="object.title for object in ctrl.childObjectCollection">
</select>
```

In generic terms the ng-options is:

```js
label for objectValue in objectCollection
```

If I want to offer a null choice in the select box I can add an empty `option` like so:
```html
<select ng-model="ctrl.model.childObject"
      ng-options="object.title for object in ctrl.childObjectCollection">
  <option value="">&nbsp;</option>
</select>
```

The second case is where I have an object with some value that I want to extract from another object. In this example I have an object that has a year value.  There is a fixed list of valid years (in this case years are also objects with a few properties).  I want the "id" of the year to be associated with my object and I want the normal textual representation of the year to be visible in the `select` control.  Here is how you do that:

```html
<select ng-model="ctrl.model.yearId"
      ng-options="year.yearId as year.year for year in ctrl.years" ></select>
```

So to put this in more generic terms the ng-options follows this rule:

```js
value as label for obj in objectCollection
```
