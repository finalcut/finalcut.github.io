---
<%*
let title = tp.file.title;
if (title.includes("Untitled")) {
	title = await tp.system.prompt("Meeting Subject")
} 
await tp.file.move("_posts/" + tp.date.now("YYYY-MM-DD") + " - " + title)
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