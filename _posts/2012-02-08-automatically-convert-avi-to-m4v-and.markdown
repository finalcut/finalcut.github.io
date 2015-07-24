---
layout: post
title: "Automatically convert .avi to .m4v and add to iTunes using Automator"
date: 2012-02-08
comments: false
categories:
 - m4v
 - conversion
 - folder-action
 - handbrake
 - mac
 - avi
 - applescript
 - automator
---
That is a long title but not nearly as long and arduous as my process of
figuring out how to do what it says.  Here is the scenario...  
  
Let's say you and your mom are sharing a dropbox folder and she plops in an
.avi of her recent performance in the community theater where she lives.  You
don't really like the avi format and would prefer it in the m4v format and
inside iTunes so you can watch it on your TV using your apple tv.  What is one
way to do that?  
  
Well, I'm going to tell you.  Now, trust me, this probably isn't the best way;
but it works and that's all I wanted.  Initially I tried the export movies
task in automator but the resultant video wasn't working in iTunes - I'm not
sure why.  Therefore I resulted to using the Handbrake CLI from within an
apple script via automator.  Here is the script:  
  
  

    
    
    on run {input, parameters}  
     repeat with i in input  
      try  
       set text item delimiters to ":"  
       set file_name to last text item of (i as text)  
       set text item delimiters to ""  
      on error  
       set text item delimiters to ""  
      end try  
        
      set origFilepath to quoted form of POSIX path of (i as alias)  
      set newFileName to "" & (characters 1 thru -5 of file_name as string) & ".m4v"  
      set newFilepath to "/Users/me/mp4/" & newFileName & ""  
        
      
      --apple uses colons as delimiters while the  Untitled=drive; Users=directory; me=username; mp4=temp directory..  
      set finalPath to ("Untitled:Users:me:mp4:" & newFileName)  
        
        
      --start the conversion; shell command uses the forward slash as the delimiter; hence two finalpath defined.  
      set shellCommand to "nice /Applications/HandBrakeCLI -i " & origFilepath & " -o " & newFilepath & " --preset=\"AppleTV 2\";"  
      do shell script shellCommand  
        
      --I've told itunes to copy files on import; this way I don't have m4v's laying all over the place  
      tell application "iTunes"  
       add finalPath  
      end tell  
        
      --after the import is done I delete the m4v file I just created (from the temp directory)  
      tell application "Finder"  
       delete finalPath  
      end tell  
        
     end repeat  
       
     return input  
    end run  
    ```
      
    Basically to use this you create a new automator "Folder Action" using an "Apple Script"  paste this entire thing into the script (replacing anything apple puts there by default).  Then pick the folder you want to watch.  I noticed that the task usually fires off about 10 seconds after an .avi file shows up in the directory.  
      
    This still needs something to confirm the file that just plopped into the watch directory is an actual .avi file.  I didn't worry about that though it is probably  not too hard to add that check (though with apple script and its' crazy syntax I wouldn't bet on it).
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    Juan Manuel Bosque
    
    
    
    
    
    This script runs perfecly. Congratulations.  
    Mi unique problem is that if the name of the source file cointains blank spaces, the output file result in a file without extension and it's not imported to itunes... :-\
    
    
    
    
    
    
    
    
    

