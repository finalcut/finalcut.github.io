---
layout: post
title: "Parsing Large XML Documents in Ruby"
date: 2012-01-20
comments: false
categories:
 - ruby
 - nokogiri::xml::reader
 - nokogiri::xml::node
 - nokogiri
 - xml
 - nokogiri::xml::nodeset
---
Today I was given a fairly large XML file (roughly 32 Mb) that I needed to
parse in order to see if there was a match between a concatenation between two
node values and the contents of a separate file that had comma separated
values in it.  Always looking for an excuse to use a different language than I
normally do I decided to attack this in Ruby because I remember it being
particularly good at handling File IO.

I'm going to present two solutions to this problem here.  I'm sure they can
both be improved.  However, the second solution was the one I settled on
because it is substantially more performant.

Example 1 - Using SimpleXML
Look, I don't know Ruby well at all so when I saw a library called SimpleXML I
thought - "sweet that's right up my alley!"  It really was easy to use but, as
you'll see, it wasn't the right tool for this particular job.


```ruby
  require 'rubygems'
  require 'xmlsimple'

  duplicates = Array.new()
  enrollments = Array.new()


  # read in the xml of enrollments
  puts "reading in enrollment file; this could take a while."
  data = XmlSimple.xml_in('students.xml')

  puts "enrollment file loaded; now to parse it!"
  cnt = 0
  data['membership'].each do |course|
  courseId = course["sourcedid"][0]["id"][0].strip
  course["member"].each do |student|
   studentId = student["sourcedid"][0]["id"][0].strip
   enrollmentId = studentId << "," << courseId
   enrollments.push(enrollmentId)
  end
  cnt++
  if cnt > 9 then
   p "."
   cnt = 0
  end
  end


  #read in the comma delimited list..
  puts "reading in the drop file"
  drops = File.readlines("term_drops.lis");
  drops.delete_at(drops.length-1)


  drops = drops.collect{|x| x.strip}

  puts "comparing..."

  duplicates = enrollments & drops

  if duplicates.size > 0 then
  puts "found the following duplicate enrollments"
  puts duplicates
  else
  puts "YES! no duplicates found"
  end

```


By far the slowest part of this process was the line data = XmlSimple.xml_in('students.xml') - in fact with my large XML file I got bored and gave up waiting for it to load.  What I needed was a parser that would pull in one node of the document at a time.

Nokogiri

It turns out there are a few solutions but I settled on Nokogiri and I'm glad I did. Honestly, the documentation is a little confusing but the library itself works great.


```rb
  require 'rubygems'
   require 'nokogiri'

   duplicates = Array.new()
   enrollments = Array.new()


   puts "reading in drops file"
   drops = File.readlines("term_drops.lis");
   drops.delete_at(drops.length-1)
   drops = drops.collect{|x| x.strip}


   puts "reading in enrollment file; this could take a while."
   data = Nokogiri::XML::Reader(File.open("students.xml"))

   data.each do |node|

if(node.name == "membership" && node.node_type == Nokogiri::XML::Reader::TYPE_ELEMENT)

 doc = Nokogiri::XML(node.outer_xml)

 classId = doc.xpath("//sourcedid/id")[0].inner_text.strip

 studentId = doc.xpath("//member/sourcedid/id")[0].inner_text.strip

 enrollmentId = studentId << "," << classId


 if drops.include?(enrollmentId) then

  puts  enrollmentId

 end

end
   end

```


As you can see both scripts are pretty short - ruby really is nice for this kind of stuff.  I also do a few weird things in both concerning the way I pull in my comma delimited flat file (I drop off the last line for instance but I don't really have to).

Their were a couple little gotcha's I ran into using Nokogiri.  First is that when I do the data.each do |node| block it literally will iterate over every node in the document down to the most distant child.  Thus I needed to filter things out by using the node.name check.  Secondly, when it iterates it actually deals with every node twice; once on entering the node and once on exiting it.  That is why I am checking for the node_type as well as the node.name.

Also, and this was just stupidity on my part, in order for me to do the xpath query on the node (after creating a small xml document using Nokogiri) I had to use outer_xml and not inner_xml.  Using inner_xml worked ok when I was just searching for the classId because when I created the document using inner_xml it actually ignored all sibling nodes to the sourcedid node.

I also don't really know xpath all that well thus there is probably a better way for me to make sure I'm only getting the first sourcedid when I ask for classId instead of ALL sourcedid values in the document when I fire of the xpath query.  I'm not really sure; if there is feel free to let me know in the comments.

Overall this code is pretty rough and specialized for this one off task I was asked to do but hopefully the Nokogiri code will help others as they parse an xml document while looking for values that might be spread out over various nodes.







