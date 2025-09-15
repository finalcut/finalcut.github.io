---
firstprop: first
layout: single
title: Auto Share a New Blog Post to BlueSky
category: blogging
tags:
  - github-pages
  - github-actions
  - bluesky
comments: false
featured: true
date: 2025-09-14
author: Bill Rawlinson
description: How I am sharing my blog postings to bluesky using a github action.
---
Today I decided I would figure out if I could auto-post about my blog posts to BlueSky? I figured there had to be a way so after a bit of google hunting I found [a great blog post](https://www.woodwardweb.com/post/2025/08/automated-bluesky-integration/) that gave me _most_ of the keys to the process.  

It took a while for me to get it all sorted out.  For starters, I'm using Jekyll behind the scenes on this and the other person is using Astro.  He actually has a cool component to his blog that takes things a bit further (where I'd like to get) but, for now, it was enough to get me started.

Quick Summary of Steps:
1. I had to clone the default publish workflow at github so I could modify it.
2. I had to merge the "deploy" jobs into one "deploy and build" (maybe didn't have to, but it made things easier)
3. Had to learn a couple key things about GitHub Actions
	1. the actions has a TOKEN, `GITHUB_TOKEN` that comes with it and you have to pay attention to its permissions.
	2. Dual stage "deploy" means the artifact that gets pushed by the github actions has to have a distinct name.
4. Just like with any programming - don't be an idiot and reference the wrong variables
5. My blog has some special url paths that I needed to be mindful of when building the link to the post that I was going to share to BlueSky
6. You can create an [app specific BlueSky password](https://bsky.app/settings/app-passwords) to _limit_ the damage that might be done if someone gets the password.

## GitHub Actions
The entire process is driven via GitHub Actions.  My blog is hosted via GitHub Pages. I'm going to assume you are familiar with that already as giving that background will really stretch the scope of this post.

The first thing I had to do, once I realized it, was to change the default `Build and Deployment` setting on the Github Pages to use `GitHub Actions` instead of `Deploy from a branch`.  You can do this by going to your GitHub repository -> Settings -> Pages.  Then change the `Build and deployment` source to `Github Actions`.  Once you do that it gives you the ability to copy the code that currently deploys your site into a jekyll.yml file.  Here is [my jekyll.yml file](https://github.com/finalcut/finalcut.github.io/blob/main/.github/workflows/jekyll.yml) after I made the tweaks this post discusses.

![GitHub Actions Setting](/assets/images/github-actions-build.png)

Second, I took the steps from the `build` and `deploy` jobs and merged them into one job which I called, appropriately, `build-and-deploy`.  This was both logical and it made it easier for me to port the code from Martin Woodward.

I had to make some changes to things.  

First, I had already created GitHub secrets for my bluesky handle and password (using [an app password](https://bsky.app/settings/app-passwords)).  Make sure you use an app password.

Second, because I use Jekyll the path to my posts is a bit different than his.  So I had to replace places where he referenced `src/content/post` with `_posts`.  I also didn't look for `categories` I just look for `category` in my front matter (post metadata).  The initial logic to process the posts uses AI a bit - there was a caveat there I'll cover in the next section.

During the build and deploy process there were two steps I needed to tweak from the default - `Upload Artifact` and `Deploy to Github Pages` - I had to give the artificat a name and reference it via that name:

### Upload Artifact

#### Before
```
      - name: Upload artifact        
        uses: actions/upload-pages-artifact@v3
```
#### After
```
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          name: github-pages-initial
```

I think I just stole the name Martin was using.  It is `initial` here because we do these two things twice in the process and each instance needs a distinct name.  So, since this is the first its the initial.

### Deploy to GitHub Pages
#### Before
```
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```
#### After
```
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
        with:
          artifact_name: github-pages-initial
```

Note that the argument changes from `name` to `artifact_name` between the two steps.  Don't be like me and call it `name` in both places. It won't work.

## AI
One cool thing I saw Martin doing was generating an AI overview of his posts to use as the main text of his BlueSky post.  I stole that idea but, initially, it didn't work at all.  It turns out I had to make sure the `GITHUB_TOKEN` had permission to the AI models.  This was pretty easy to do once I realized it was necessary.  There were already some permission set early in the file:

```
permissions:
  contents: read
  pages: write
  id-token: write
```

I just had to add one more permission `models: read` and I was good to go.
```
permissions:
  contents: read
  pages: write
  id-token: write
  models: read
```

In Martins example he is looking for British English in his prompt. I switched to US English to more match my style.  I also reduced the size of the AI generated result to 225 characters (from his 250) so that there would, generally, never be a problem with appending the URL at the end.  GitHub Actions will throw an error if you try to post something longer than 300 characters so I wanted that extra buffer of 25 characters.

## Other Considerations
My post title has spaces in it, the post link has hyphens separating the words - so I had to transform things a bit.  My posts also always have the category of the post in the URL - so I had to make sure I include that when I built the URL to the post before sending it to BlueSky.

I added a fake property at the top of all my blogs posts called `firstprop` so I'd have a placeholder for where I could inject new properties.

## Outstanding Issues

The logic for whether or not to publish a post to BlueSky is based on if the post already has a BlueSkyURI property or not.  The Jekyll workflow adds this and then tries to update the git repo. Well, it should add it but, it doesn't.  The GitHub action I'm leaning on to post to BlueSky doesn't seem to actually have the output variable that Mr. Woodward is using.  I'm not sure what's up there.  So, for the time being I still have to do some copy/paste.  Kind of annoying.

Woodward is using version 0.1.0 of the action `zentered/bluesky-post-action` but I don't get the uri from it - so I tried updating to 0.3.0 and, still no luck.  I'm not sure why it doesn't have the `uri` as an output as Woodward's code implies it should.  For now, because that value doesn't exist the `rebuild-after-bluesky` job doesn't actually fire off yet.


When I have time I'll figure out the issue and address it. I suspect I just don't understand something about GitHub Actions.

Once more, if you want to see the inspiration post - visit [Martin Woodwar's Blog Post](https://www.woodwardweb.com/post/2025/08/automated-bluesky-integration/) and if you want to see my workflow you can see the [Jekyll yaml file in GitHub](https://github.com/finalcut/finalcut.github.io/blob/main/.github/workflows/jekyll.yml)


