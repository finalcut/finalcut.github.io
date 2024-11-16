---
layout: post
title: "SystemJS and Internet Explorer"
description:
headline:
date: 2016-01-28 16:38:52 -0500
category: development
tags: []
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
I remain a non-fan of microsoft's browsers but, fortunately, thanks to polyfills you can get almost anything to work in them.  Today, I was really struggling with getting my angular app, which uses JSPM and SystemJS, to initialize properly within IE.  Quite frankly, it was driving me crazy.

It turns out SystemJs will try to inject a script tag into your page for another js file called system-polyfills.js if it needs it.  When running in IE SystemJs does, in fact, need system-polyfills.js.  However, in my published compiled version of the site I didn't have system-polyfills.js floating around.  I did, however, have system.js and config.js (used with JSPM).

My gulp build was setup to copy those two files into the build/dist/scripts directory so I just had to update it to copy the system-polyfills.js file as well.

Here is a snippet of my gulpfile that shows this in action:


```js

...
var paths = {
	app: {
	    configScripts: [
	      'jspm_packages/system.js',
	      'jspm_packages/system-polyfills.js',
	      'config.js'
	    ],
	},
	build: {
		basePath: 'build/',
		dist: {
		  basePath: 'build/dist/',
		  fonts: 'build/dist/fonts/',
		  images: 'build/dist/images/',
		  styles: 'build/dist/styles/',
		  scripts: 'build/dist/scripts/'
		},
		docs: 'build/docs/'
	}
	...
}

...

gulp.task('copyStuff',function(){
  gulp.src(paths.app.configScripts)
    .pipe(gulp.dest(paths.build.dist.scripts));
  return  gulp.src('src/app/app-bootstrap.js')
      .pipe(gulp.dest('build/dist/src/'));
});
```

Once the system-polyfills.js path was added to paths.app.configScripts it was put in the correct location on the built side of things.  Then, when SystemJs injected it's own script tag to point to system-polyfills.js the file was actually there when it was requested by the browser.

Basically, just make sure system-polyfills.js is in the same directory as system.js on your deployed site and SystemJs will work as expected in IE.
