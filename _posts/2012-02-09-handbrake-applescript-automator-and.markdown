---
layout: post
title: "Handbrake, Applescript, Automator, and iTunes Together as a Folder Action"
date: 2012-02-09
comments: false
categories:
 - m4v
 - handbrake
 - avi
 - applescript
 - itunes
 - automator
 - apple
---
Yesterday I posted about my initial attempt at automatically converting .avi
files with handbrake to m4v files and having them automatically added to
iTunes.  That plan worked fine if the items dropped into my watched folder
were all of the type .avi AND they weren't in a subdirectory.  
  
Tonight I decided to try and address these two deficincies.  First I can now
handle the case where a folder is the "input" parameter; though my knowledge
of applescript is so deficient I can only deal with one layer of directory
heirarchy - sorry, no recursion.  I also now test for the extension of the
file being processed to make sure it is an .avi before proceeding (otherwise I
just skip the file).  
  
Yesterday I also made the script look a little more generic by hiding some of
the elements of my directory structure by using words like "me" - today I
decided to just post it as I wrote it.  You will have to change some variable
values to make this work on your system.  
  
  

    
    
    on run {input, parameters}  
     repeat with x in input  
      
      -- need to determine if input is a file or a directory..  
      set details to (info for x without size)  
      set allFiles to {}  
      
      if kind of details is "folder" then  
       -- if it is a folder, we need to grab all the contents as a list  
       set tempFiles to list folder (x) without invisibles  
       repeat with y in tempFiles  
        set the end of allFiles to ((x as string) & y) as alias  
       end repeat  
      else  
       -- if it is a file then we make a one item list..  
       set the end of allFiles to x as alias  
      end if  
        
      -- now loop over the list we just made.  
      repeat with i in allFiles  
         
       -- only process avi files.  
       if name extension of (info for i) is "avi" then  
        try  
         set text item delimiters to ":"  
         set file_name to last text item of (i as text)  
         set text item delimiters to ""  
        on error  
         set text item delimiters to ""  
        end try  
          
        set origFilepath to quoted form of POSIX path of (i as alias)  
        set newFileName to "" & (characters 1 thru -5 of file_name as string) & ".m4v"  
        set newFilepath to "/Users/bill/temp_movies/mp4/" & newFileName & ""  
          
          
        --apple uses colons as delimiters while the  Untitled=drive; Users=directory; me=username; mp4=temp directory..  
        set finalPath to ("Untitled:Users:bill:temp_movies:mp4:" & newFileName)  
          
          
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
          
        -- prepare the movie for later deletion..  
        set trashPath to "Untitled:Users:bill:temp_movies:to_trash:"  
        tell application "Finder"  
         move i to folder trashPath  
        end tell  
       end if  
      end repeat  
     end repeat  
     return input  
    end run  
    ```
    
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    Anonymous
    
    
    
    
    
    Dear Mr. Rawlinson!  
      
    How would a script look like, that converts all *.mov from my "movies/mov" folder to "automatically add to itunes" -Folder with originalname.m4v  
    and then delete the mov-file.  
      
    Thanks for any assistens.   
      
    Karl Oberreiter  
    ok@protop.com   
    Austria  
    
    
    
    
    
    
    
    
    
    

