---
layout: post
title: "Git to Hell and Back Again"
date: 2013-07-24
comments: false
categories:
 - merge
 - svn2git
 - git
 - read-tree
 - multiple-repositories-into-one
---
At my office we've long used Subversion (SVN) for our version control system
but we've slowly been migrating to Git (and Github for hosting). I've not
really dealt with the process of moving a project from SVN to Git before so
recently, when one of my projects was set to be moved I jumped on the task
eager to dig deeper into some of Git's tools. Little did I know that I'd
actually end up digging in much further than a normal SVN to Git migration
would require.  
  

I'm going to preface the rest of this article with a caveat - our SVN repo's
for this project and some related projects were a mess.  We had, at some point
in the past, decided to just start a fresh repo for the main project which
I'll call "PROJECT" so we had a svn repository called "PROJECT" and
"OLD_PROJECT" and "PROJECT2"  as well as another one called "PROJECT_DATABASE"  
  
The only two of those I care about are PROJECT2 and PROJECT_DATABASE but that
didn't stop me from forgetting and trying to use PROJECT first (which is a few
years out of date).  I'll come back to this mix up later because it didn't
happen until well into the process.  
  
Here were the steps I thought I was going to have to do when I began.

  1. Migrate PROJECT2 to Git and then push to Github as PROJECT
  2. Tag the repo as "END_OF_PY2013"

I also have a big new task order for this project so I also had to make a
branch and then begin work on the new branch.  
  

I didn't do that though.  Oh, no, not me.  I lost track of what I was doing.
So what I did was:

  1. Migrate PROJECT2 to Git and then push to Github as PROJECT
  2. Tag the repo as "END_OF_PY_2013"
  3. start working on the new task order on master; make three sort of big commits and push them to github
  4. realize I also  had to migrate PROJECT_DATABASE to git and merge that into a subdirectory of PROJECT on git.
  5. push this merge to github
  6. realize I hadn't created my development branch for the new task order so create a branch from master now 
  7. continue working for two weeks resulting in hundreds of commits on the new branch.
  8. add a new person to the project who needs a new branch of master
  9. realize those three commits I had made and pushed before I migrated the database directory over were going to cause me a nightmare.

At this point I needed to figure out a way to fix master while not losing all
of my changes in my dev branch which is called CARD90 (to represent the trello
card being used to track this feature).

The first thing I did was delete the new branch I created for the new
developer.  It was just muddying the water and wasn't useful until I fixed
master.  
  

I tried a bunch of things with interactive rebase to fix master but it seemed
like things were just getting crazier and crazier.  I barely understand
rebasing so I was probably making things as bad as it seemed. Fortunately, at
this point, I was still the only person who'd actually used our github
repository.  I decided on a semi-nuclear option - I deleted the github
repository for PROJECT and decided to do the svn to git migration again to get
back to where END_OF_PY2013 should have been, with the PROJECT_DATABASE merged
in as a subdirectory (/database).  
  

I mucked around a bit and tried to get it to work but I kept having problems
doing this SVN to GIT migration on PROJECT from svn.  I couldn't figure out
why not all of my files were showing up that should have.  It was driving me
crazy until I realized, after about half an hour, that I should have been
migrating PROJECT2 and not PROJECT.  Ugh.  Once I made that realization things
started to get better.  
  
What follows are the steps I took to migrate both projects from SVN to Git and
then to merge them.  Then I show how I merged my other git development branch
from the past two weeks into a new branch on this new git repository.  
  

  1. **Convert PROJECT2 svn repo to PROJECT git repo** without moving over the tags/branches  

    
            $svn2git svn://path/to/project2 --notags --nobranches --username {me} -v  
       ```
    
            1. the 'V' is important so that you will see the checkout from svn pause so you can enter your password then hit enter. [You will not be prompted for a password](https://github.com/nirvdrum/svn2git/issues/59)
            2. I used the documentation at <https://github.com/nirvdrum/svn2git#readme> to figure out the various command switches I needed for these steps.    
      2.    **Convert PROJECT_DATABASE svn repo to new git repo.**  There is no trunk, tags, or branches; just a root directory.  
       
    
            $svn2git svn://path/to/project2 --notags --nobranches --rootistrunk --username {me} -v  
       ```
    
            1. Make sure there are no directories in the root of the project called Branches or Tags or else this won't work.  If there are rename them in svn before you proceed!
      3. **Merge PROJECT_DATABASE git repo into PROJECT repo** as /database directory  
       
            1. I followed the instructions at <http://jasonkarns.com/blog/merge-two-git-repositories-into-one/>     
        
                      $ cd /PROJECT  
              $ git checkout master  
              $ git remote add -f database /path/to/PROJECT_DATABASE  
              $ git merge -s ours --no-commit database/master  
              $ git read-tree --prefix=database/ -u database/master  
              $ git commit -m "merging PROJECT_DATABASE into PROJECT"  
             ```
        
            2. At this point I have my end of PY 2013 version of the two svn repos in one git repo.  So it's a good time to TAG it.
            3. After tagging the repo I created a branch     
        
                     $ git checkout -b CARD90  
            ```
        
            4. Now it's time to merge my old git repo's CARD90 branch into the new CARD90 branch so I get all my changes and commit log.      
        
                      $ cd /PROJECT  
              $ git checkout CARD90  
              $ git remote add -f OLD_PROJECT /path/to/OLD_GIT_PROJECT  
              $ git merge -s ours --no-commit OLD_PROJECT/CARD90  
              $ git read-tree -m -u OLD_PROJECT/CARD90  
              $ git commit -m "merging all of my modifications for the current task order from the old GIT repo"  
             ```
        
      4.     I also wanted to **remove references to the SVN remotes** that were created during the SVN2GIT steps    
    
            $ cd /PROJECT  
        $ git checkout master  
        $ git config --remove-section svn-remote.svn  
        $ git config --remove-section svn  
         $ rm -Rf .git/svn  
         $ git branch -d -r svn/trunk  
       ```
    
      5.    Last but not least I needed to **remove the remotes that I didn't need anymore** (database and OLD_PROJECT)    
    
            $ cd /PROJECT  
        $ git checkout master  
        $ git remote remove database  
        $ git remote remove OLD_PROJECT  
       ```
    
    
    
    

