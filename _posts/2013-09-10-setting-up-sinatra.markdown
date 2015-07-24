---
layout: post
title: "Setting Up Sinatra"
date: 2013-09-10 13:38
comments: true
categories: [angular, grunt, sinatra, yeoman]
---
Today I deciced to try and setup a ruby web app that uses sinatra on the backend and angular on the front end. In order to support angular I also decided to use Yeoman which is really a trifecta of tools, to manage the various front end dependencies (including bootstrap).

I've used Sinatra to the extent that I have previously setup a "hello world" program. I have used twitter bootstrap a little (quite a few versions ago) and I've never used Yeoman. Needless to say I have a lot to learn.

During my process today I utilized the tips outlined in an [This Article](http://spiritmachineblog.tumblr.com/post/39064480937/a-simple-openlayers-app-with-yeoman-sinatra-mongodb). However, that article is a little outdated with how yeoman works so I had to sort of guess on how to proceed at times plus I ran into a problem getting yeoman to download from github using the ssh protocol. Fortunately, I found a [google groups posting](https://groups.google.com/forum/#!msg/yeoman-dev/SgWH0nObEb8/tmjzaLmWgJwJ) which helped me work around that problem.

Some of the yeoman setup stuff flys by on the screen as it loads and downloads things so it is tough to see errors as they occur. I knew a couple things had gone wrong but figured it would give out some kind of report of the actual errors at the end. It doesn't. Thus, you just have to scroll back up. I didn't. Therefore, when I ran "grunt" which, in the reference article is "yeoman build", chrome was started but then the angular javascript library wasn't found and, due to the error, the build couldn't happen.

By viewing the source of the index.html page I saw that a directory called "bower_components" is supposed to exist. It didn't. I tried to reinstall the angular stuff using "yo -f angular && karma" (which also reinstalls the karma stuff I think). But that was when I noticed a lot of errors connecting to github. The aforementioned google group posting was the solution to that. In case it disappears here is what it was:

```ruby
 git config --global url."https://".insteadOf git://
```

 That says to git to use https:// instead of git://. When I'm back home on my own network I'll have to edit my global git config to remove that but, as I was in a Panera at the time I needed to use this because the port for the git ssh protocol was blocked (git status 128 error).

I'm pretty sure I have at to figure out a few more things still. For instance, if I edited the SASS file (/app_root/app/styles/main.scss) that was auto-generated the changes aren't reflected in the generated .css file (/app_root/.tmp/styles/main.css). In fact, in the development environment the styles didn't show up at all unless I added this block of code to /app_root/app.rb

```ruby
get '/styles/main.css' do
	send_file File.join(settings.styles_folder, 'main.css')
 end
```

And this line to the configuration block at the top of /app_root/app.rb:

```ruby
set :styles_folder, ENV['RACK_ENV'] == 'production' ? 'dist/styles' : '.tmp/styles';
```

Thus, once I was done my /app_root/app.rb file looks like this:

```ruby
require 'sinatra/base'

class App < Sinatra::Base
	configure do
		enable :logging
		set :public_folder, ENV['RACK_ENV'] == 'production' ? 'dist' : 'app'
		set :styles_folder, ENV['RACK_ENV'] == 'production' ? 'dist/styles' : '.tmp/styles';
	end

	get '/' do
		send_file File.join(settings.public_folder, 'index.html')
	end

	get '/styles/main.css' do
			send_file File.join(settings.styles_folder, 'main.css')
	end

end
```

Undoubtedly, as I figure out the actual architecture of my app this will change a bit. My hope is to have a "single-paged" app that utilizes the powers and capabilities of angular while providing the back-end api via the sinatra framework.

I have a ton to learn specifically in regard to angular and sinatra. Heck, I've barely used Ruby before so I have a bunch to learn there as well. I'm looking forward to it.