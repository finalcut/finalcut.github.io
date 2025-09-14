---
<%*
const title = tp.file.title;
let fileName = title;
if (fileName.includes("Untitled")) {
	fileName = await tp.system.prompt("Meeting Subject")
} 
fileName = fileName.replace(/ +/g, '-').toLowerCase();
fileName = fileName.replace(/-+/g, '-');
await tp.file.move("_posts/" + tp.date.now("YYYY-MM-DD") + "-" + fileName)
-%>
layout: single
title: <% title %>
category: 
tags: []
comments: false
featured: false
date: <% tp.file.creation_date('YYYY-MM-DD') %>
author: Bill Rawlinson
---