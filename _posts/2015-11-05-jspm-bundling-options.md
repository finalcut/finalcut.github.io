---
layout: post
title: "JSPM Bundling Options"
description: 
headline: i sho
date: 2015-11-05 11:24:05 -0500
category: javascript
tags: [jspm,gulp,systemjs,bundle,bundle-sfx]
imagefeature: 
mathjax: 
chart: 
comments: true
featured: false
---
Bundling is a pretty handy concept when working with javascript projects.  Bundling looks at your javascript source, finds all of the files and javascript dependencies, and squashes them all into one file that can then be minified.  Thus, when your project is in production the users are only downloading one versioned javascript file instead of the, potentially, hundreds of files you have written for the project.

I'm currently working on a fairly large and complex angular application.  At the moment, including dependencies, the project has about 700 distinct javascript files.  If I didn't bundle the end user would have to download all 700 files independently which causes the page to load pretty slowly and puts an excessive amount of network traffic on my server.


## Auto-Executing Bundles : Cool But Limited
In the project I am using JSPM to manage my dependencies and to handle the bundling of all of my javascript.  Initially the project was configured to use a "self-executing bundle".  The concept behind a self-executing bundle is pretty nice.  You have one file (a bootstrap file, not to be confused with the twitter framework) that you pass to the `jspm bundle-sfx` command and it will parse it, find all of your dependencies from it, and then create your final file.  It's pretty slick.

Your bootstrap file doesn't have to be huge either; it can be broken up into modular bits so that you can manage each type of resource more logically.  Here is the bootstrap file from the project:

```javascript
import 'jquery';
import 'jqueryui';
import angular from 'angular';

import app from './app';

angular.element(document).ready(function() {
  angular.bootstrap(document, [app.name], {
    strictDi: true
  });
});

```

The app file is really where all the magic happens and where we import a bunch of other files.  The bundler goes through all of the imported files and figures out all of the dependencies (based on yet more imports) and eventually makes sense of it all and builds the final javascript file in such a way that all of the code is included in it in the correct order. 

This is pretty damn cool and powerful.  However, there is a problem.  The self-executing bundler can't handle projects with too many files and I ran into that limitation this week.  The error was pretty unclear and figuring out that it was caused by too many files too a few hours.  The bundle process seemed to work ok and the resulting file looked like it should work but it didn't and when the app tried to load angular wasn't defined.

Here is the gulp task I was using for this type of bundling:

```js
gulp.task('bundle', ['lint'], plugins.shell.task([
  'jspm bundle-sfx src/app/app-bootstrap ' + paths.tmp.scripts + 'build.js'
]));
```

Basically it just passes in the app-bootstrap file and outputs the final javascript file in the temp script directory and calls it `build.js`

## Bundle the "Old Fashioned Way"
Fortunately, there is another option - bundling the old fashioned way using `jspm bundle`  It takes a little bit more work in the configuration and you have to plan things out a little more but in the end it works even with a ton of files.  Plus, by going to the standard bundle option I can split my bundle into two files - one that holds all of my dependencies and the other that holds the code I actually wrote for the application.

Sure it adds one more network request but the dependency file can be cached by your browser and it won't change very often. Just make sure your server puts a far distant expiry header on the dependency file.  A nice bonus to this is that during development you can speed up initial page reloads by using the dependency build along side the independent loading of the files you are writing.

By taking this approach my development environment went from making apx 700 requests to making just 380 requests (granted, I'm not done so the dev request count will go up).  Doing that takes about 10 seconds off my page load time though which is a huge bonus.

Now I have two separate bundle tasks in my gulp file.  The first builds the dependency file and the second builds my app file:

```js
gulp.task('bundle', ['bundleDeps'], plugins.shell.task([
  // this bundles all of the code we wrote and excludes anything 
  // in dependencies.js (which are all of our external dependencies)
  'jspm bundle src/app/app-bootstrap - tmp/scripts/dependencies.js ' + paths.tmp.scripts + 'build.js'
]));

gulp.task('bundleDeps', [], plugins.shell.task([
  'jspm bundle src/app/app-bootstrap - [src/app/**/*] - [src/app/**/*!text]' + paths.tmp.scripts + 'dependencies.js'
]));
```

For bundling the dependencies (`bundleDeps`) I still use my bootstrap file but tell the bundle process via "bundle math" to exclude anything in my src/app directory tree because my app code exists in that directory.  The bundler still figures out all the dependencies and thus builds a nice javascript file called dependencies.js in my temp directory that contains all of the jspm managed packages my project is using.

**NOTE** There is a bit of a gotcha in the bundleDeps task.  ` - [src/app/**/*!text]` - that little bit of bundle math makes sure your html templates aren't included in the dependency bundle.  Without it your app specific templates won't be in the right bundle!

The primary bundle task (`bundle`) now bundles the src/app/app-bootstrap tree but excludes any dependencies that are already included in the dependencies.js file (again, using bundle math).

I've mentioned bundle math a couple times.  You can tell I'm using it by the presence of the `-` in the commands.  The `-` means "exclude" this.  You can also use a `+` to explicitly include a dependency if you need to.

At this point I'm pretty close to having everything working auto-magically for me both in development and on my build server that deploys to production.  However, there are still some missing pieces that are provided by some other gulp tasks.  Namely, `inject` and `usemin`.  I might cover those (and some "gotchas") in another post.
 
**BONUS COVERAGE**

There is a problem with the way I'm doing things above - using the shell task I can't pipe things together quite as well as I could if `jspm bundle` were a native gulp plugin.  Fortunately, a plugin exists called [gulp-jspm-build](https://www.npmjs.com/package/gulp-jspm-build) which will do exactly what I need.  You can do both the self executing bundle and the standard bundle using this plugin.

To import the plugin I am using gulp-load-plugins like so `var plugins=require('gulp-load-plugins')();` thus I reference the `gulp-jspm-build` plugin as `plugins.jspmBuild` which is how `gulp-load-plugins` loads plugins with a hyphen in the name.

## Auto-Executing Bundles with the Plugin

```js
gulp.task('bundle', [], function () {
  return plugins.jspmBuild({
    bundleOptions: {
      sourceMaps: false,
      minify: false,
      mangle: false
    },
    bundles: [
      { src: 'src/app/app-bootstrap', dst: 'build.js' }
    ],
    bundleSfx: true
  })
.pipe(gulp.dest(paths.tmp.scripts));
```

I'm not I'm setting the various `bundleOptions` to false on purpose because after doing the bundle I still have to do a bit of other work.  One thing to keep in mind - you have to pipe the results of `jspmBuild` to `gulp.dest()` and tell `dest` what directory to save the file in.  The `dst` property of the bundle just names the eventual file but doesn't actually save it.


## Bundle the "Old Fashioned Way" with the Plugin

```js
gulp.task('bundle', ['lint','bundleDeps','copyStuff'], function () {
  return plugins.jspmBuild({
    bundles: [
      {
        src: 'src/app/app-bootstrap - ' + paths.tmp.scripts + 'dependencies.js',
        dst: 'build.js',
        options: {
          sourceMaps: false,
          minify: false,
          mangle: false
        }
      }
    ],
    bundleSfx: false
  })
  .pipe(gulp.dest(paths.tmp.scripts));
});

gulp.task('bundleDeps', function () {
  return plugins.jspmBuild({
    bundleOptions: {
     sourceMaps: false,
     minify: false,
     mangle: false
    },
    bundles: [
      {
        src: 'src/app/app-bootstrap - [src/app/**/*] - [src/app/**/*!text]',
        dst: 'dependencies.js'
      }
    ],
    bundleSfx: false
  })
  .pipe(gulp.dest(paths.tmp.scripts));
});
```

As you can see, I've broken my build back up and st the `bundleSfx` to false.  I didn't have to do that; `bundleSfx` is false by default.  I explicitly stated it here for clarity.

Using the plugin is a tiny bit slower but doing it this way enables you to bundle, then ngAnnotate, then minimize and uglify in a nice gulp pipe fashion.


**CAUTION**
-- updated 14 March 2016
Okay, so there is one big problem with using the plugin approach. The plugin does a very poor job of alerting the user to problems.  For instance, if there is a syntax error in a jspm package file that the plugin is trying to bundle you just get a worthless error message along the lines of:

```
'Uncaught, unspecified "error" event.'
```

Basically, the unspecified event will either be a missing file or a corrupt javascript file that the bundler can't process.  When this error occurs I run the non-plugin version of the bundler (I have a gulp task called `obundleDeps` that I run because this typically only happens when I try to bundle the dependencies.)

Running the straight `jspm bundle` gives a much more verbose error message.  Typically, to fix it, I have to delete the plugin that has the error and then do a `jspm install` again to fix that plugin.

For example, today I had a problem with the package `buffer@3.6.0`.  To fix it I had to delete the following:

* jspm_packages/npm/buffer@3.60 (directory)
* jspm_packages/npm/buffer@3.6.0.js 

By deleting those two files and then re-installing I was able to run `gulp obundleDeps` fine and then, to make sure, I ran `gulp bundleDeps` and everything was working well.  It took me way to long to think of this solution to figuring out what was wrong so I wasted most of a day getting my build system working again.  Uggh! Hopefully this will save someone else some trouble.