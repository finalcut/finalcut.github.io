---
layout: post
title: "SVN Merging for Dummies with TortoiseSVN"
date: 2010-11-01
comments: false
categories:
 - tortoisesvn
 - subeclipse
---
I'm a big fan of branching in Subversion when working on a new feature set.
However, I'm also a moron who has endless trouble getting my branch to merge
back into the main trunk of the repository. Thus, this guide, to help me (and
you) remember the easiest way to merge a branch back into trunk.  
  
I use TortoiseSVN version 1.6.7 so you may have to adjust these steps for your
version.  
  

  1. Merge Trunk into your Branch - you have to do this first; do it at least once a week if your trunk is actively seeing development so that your merge back is as painless as possible.  

    1. Right click in the root of your checked out branch and select TortoiseSVN - Merge
    2. In the dialog that appears select "Merge From Range of Revisions"
    3. In the form put your repository trunk in and leave the revision field blank.
    4. Click the "test" button if you want; or just click Merge; depending on the size of your repo you may be waiting a while; have patience and relax...
    5. Eventually the merge will finish, when it does, check the log for any conflicts and figure out how to resolve them. There shouldn't be many.
    6. Check in your branch noting the merge in the comments.
  2. Merge your Branch to Trunk - only do this after step one is completed.  

    1. Navigate to a checked out copy of your trunk
    2. right click in the root and pick TortoiseSVN - Merge
    3. In the popup select "Merge between two branches
    4. In the from field enter your trunk path. I know this is kind of counter-intuitive but it is correct. You want to update from the trunk's current state so that it then matches your branches current state (since you just merged trunk into your branch
    5. in the TO field put your branches path.
    6. Choose the HEAD revision for both branches
    7. Merge away (or test if you prefer)
    8. Check in the trunk noting the merge in the comments
  
It's painfully simple really but It messes me up almost every time. Also,
remember to update your checked out branches (your branch and trunk) before
you do any of the merges.  
  
Good coding and good luck!

## Comments

Anonymous

Thanks!

