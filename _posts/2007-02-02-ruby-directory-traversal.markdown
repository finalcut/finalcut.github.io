---
layout: post
title: "Ruby - Directory Traversal"
date: 2007-02-02
comments: true
category: ruby
tags: [utilities,scripting]
---

Yesterday I needed to write another quick ruby script to traverse a directory tree, extract source code from a variety of file types and create one file that contained all of the extracted source code. My initial thought was to use the <span class="kw">Dir</span> class; however, that resulted in a blind goose chase.

It turns out you don't have to roll your own directory traversal using the <span class="kw">Dir</span> class (which was more than a little clunky to try to accomplish) instead you need to use the <span class="kw">Find</span> module ([documented here](http://www.ruby-doc.org/core/classes/Find.html)).

The nice thing was that once I found that module the script to accomplish my task was super easy to write (about 50 lines of code including comments/whitespace). I chose to use a configuration file to hold some user-specified settings so that the tool could be used to process other types of projects (I processed a c# and asp.net project this time but will need to do the same to a CF project soon).

Here is the code - if you see something that could be improved, please let me know in the comments.


```ruby
require 'find'
class PatentBuilder
def initialize()
 @rootDirectory =IO.readlines("patent.cfg")[1].strip!
 @includedFileTypes =IO.readlines("patent.cfg")[3].downcase.split(",")
 @excludedDirectoryNames =IO.readlines("patent.cfg")[5].downcase.split(",")

puts @includedFileTypes
end

def rootDirectory
 @rootDirectory
end

def RecurseTree
outfile = File.new("patent_output.txt","w+");
totalFiles = 0;
 Find.find(@rootDirectory) do |path|

  if FileTest.directory?(path)
   #determine if this is a directory we don't like...
   if @excludedDirectoryNames.include?(File.basename(path.downcase))

Find.prune #don't look in this directory
   else

outfile << "// DIRECTORY: " << path

outfile << "\n"

next
   end
  else #we have a file
   filetype = File.basename(path.downcase).split(".").last
   if @includedFileTypes.include?(filetype)

outfile << "// FILE: " << path

outfile << "\n"

File.open(path).each do |line|

 outfile << line

end

#puts path

totalFiles = totalFiles + 1

outfile << "\n"
   else
   end

  end
 end
 puts "total files = " << totalFiles.to_s
end
end

PatentBuilder.new.RecurseTree

```


The configuration file (named patent.cfg) is pretty simple and needs to go in the same directory as the ruby file (patent.rb):


```ruby
::Root Directory
c:\some\directory\path
::Included File Types (extensions)
cs,aspx,vb,asmx,css,xml,resx,ascx,master,sitemap,sql,
::Excluded Directory Names
Tests,Documentation,.svn,

```


You may notice that each of my lists is comma separated and the final item in each list is trailed by a comma. Without that trailing comma the code to split the string on the comma's lost the final token in my list.
