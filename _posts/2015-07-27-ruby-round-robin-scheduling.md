---
firstprop: first
layout: post-with-discussion
title: Ruby Round Robin Scheduling
description: a simple ruby script for creating league schedules in a round robin fashion making sure to avoid duplicate matches
category: development
tags:
  - kickball
  - ruby
  - scheduling
---
## Background
I play kickball in an adult league and this season our league manager ran into a problem with
creating the schedule.  He tried to do it by hand but eventually everything started to blur so
he kind of gave up which resulted in at least one set of teams not playing each other.

The difficulty was the fact that we have 9 teams in the league this year and he didn't want
anyone to have a bye - instead he wanted each team to have one week with a double header.

I just noticed the scheduling problem this week (there is one week left in the season). So I
decided to put together a little ruby script to help prevent the problem next year.

A couple points to consider.

1. I don't know ruby at all really.  I guarantee there is a more elegant way to handle the
double header logic.
2. I imagine it would be easy to add the option to pass in some command line arguments to turn
on and off the bye week option.
3. I'll probably convert this to a web app at some point so people can use it without having
to have ruby locally.


## Configuration
You can modify this by changing the initial teams array to have the teams in your
league.

If you have an odd number of teams and you want double-headers instead of Bye weeks
change the replaceByesWithDoubleHeader to true.  Then run the script.  It's that easy.


```ruby
teams = ['White Moose Knuckles','Waka Shame','Bone Crushers','Wasted Potential','Grapes of Wrath','Silly Nannies','Team Bagtag','Ice Cream Team','Ultimately Intoxicated']
replaceByesWithDoubleHeader = false


byeMarker = 'BYE'
if(teams.length % 2)
  teams << byeMarker
end
dh = []

# create a round robin schedule - taken from http://stackoverflow.com/a/1916548/7329
schedule = (1...teams.size).map do |r|
  t=teams.dup
  (0...(teams.size/2)).map do |_|
    [t.shift, t.delete_at(-(r % t.size + (r >= t.size * 2 ? 1 : 0)))]
  end
end

# get rid of byes and give each team a double-header instead
if(replaceByesWithDoubleHeader)
  schedule.length.times do |i|
    week = schedule[i]
    week.length.times do |x|
      game = week[x]
      if(game[1]==byeMarker)
          home = game[0]
          teams.each do |team|
            if(team != home && team != byeMarker && !dh.include?(team))
              game[1] = team
              dh << team
              break
            end
          end
          week[x] = game
      end
    end
    schedule[i] = week
  end
end

# print out the schedule
schedule.length.times do |i|
  puts "Week " + (i+1).to_s
  week = schedule[i]
  week.length.times do |x|
    game = week[x]
    puts "\t" + "Game " + (x+1).to_s + " " + game[0] + " -vs- " + game[1]
  end
  if(dh.length > i)
    puts "\t" + "Double Header : " + dh[i]
  end
end
```

You can get this source code at its [github repo](https://github.com/finalcut/round-robin-schedule)

## Usage

To run the script just enter the following command to dump the contents to a txt file.

```sh
ruby schedule.rb >> sch.txt
```

After it runs you'll end up with a file similar to this:

```ObjDump
Week 1
	Game 1 White Moose Knuckles -vs- Waka Shame
	Game 2 Waka Shame -vs- Ultimately Intoxicated
	Game 3 Bone Crushers -vs- Ice Cream Team
	Game 4 Wasted Potential -vs- Team Bagtag
	Game 5 Grapes of Wrath -vs- Silly Nannies
	Double Header : Waka Shame
Week 2
	Game 1 White Moose Knuckles -vs- Ultimately Intoxicated
	Game 2 Waka Shame -vs- Ice Cream Team
	Game 3 Bone Crushers -vs- Team Bagtag
	Game 4 Wasted Potential -vs- Silly Nannies
	Game 5 Grapes of Wrath -vs- White Moose Knuckles
	Double Header : White Moose Knuckles
Week 3
	Game 1 White Moose Knuckles -vs- Ice Cream Team
	Game 2 Waka Shame -vs- Team Bagtag
	Game 3 Bone Crushers -vs- Silly Nannies
	Game 4 Wasted Potential -vs- Grapes of Wrath
	Game 5 Ultimately Intoxicated -vs- Bone Crushers
	Double Header : Bone Crushers
Week 4
	Game 1 White Moose Knuckles -vs- Team Bagtag
	Game 2 Waka Shame -vs- Silly Nannies
	Game 3 Bone Crushers -vs- Grapes of Wrath
	Game 4 Wasted Potential -vs- Grapes of Wrath
	Game 5 Ice Cream Team -vs- Ultimately Intoxicated
	Double Header : Grapes of Wrath
Week 5
	Game 1 White Moose Knuckles -vs- Silly Nannies
	Game 2 Waka Shame -vs- Grapes of Wrath
	Game 3 Bone Crushers -vs- Wasted Potential
	Game 4 Team Bagtag -vs- Ultimately Intoxicated
	Game 5 Ice Cream Team -vs- Wasted Potential
	Double Header : Wasted Potential
Week 6
	Game 1 White Moose Knuckles -vs- Grapes of Wrath
	Game 2 Waka Shame -vs- Wasted Potential
	Game 3 Bone Crushers -vs- Silly Nannies
	Game 4 Silly Nannies -vs- Ultimately Intoxicated
	Game 5 Team Bagtag -vs- Ice Cream Team
	Double Header : Silly Nannies
Week 7
	Game 1 White Moose Knuckles -vs- Wasted Potential
	Game 2 Waka Shame -vs- Bone Crushers
	Game 3 Grapes of Wrath -vs- Ultimately Intoxicated
	Game 4 Silly Nannies -vs- Ice Cream Team
	Game 5 Team Bagtag -vs- Ice Cream Team
	Double Header : Ice Cream Team
Week 8
	Game 1 White Moose Knuckles -vs- Bone Crushers
	Game 2 Waka Shame -vs- Team Bagtag
	Game 3 Wasted Potential -vs- Team Bagtag
	Game 4 Grapes of Wrath -vs- Silly Nannies
	Game 5 Ice Cream Team -vs- Ultimately Intoxicated
	Double Header : Team Bagtag
Week 9
	Game 1 White Moose Knuckles -vs- Waka Shame
	Game 2 Bone Crushers -vs- Ultimately Intoxicated
	Game 3 Wasted Potential -vs- Silly Nannies
	Game 4 Grapes of Wrath -vs- Ultimately Intoxicated
	Game 5 Team Bagtag -vs- Ice Cream Team
	Double Header : Ultimately Intoxicated
```
