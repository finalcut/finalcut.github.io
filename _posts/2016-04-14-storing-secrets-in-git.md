---
layout: post
title: "Storing Secrets in Git With Blackbox and Git Bash (MinGW)"
description:
headline:
date: 2016-04-14 16:58:20 -0400
category: development
tags: [windows,git,gpg,encryption,secrets,mingw,bash]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
A project I've been working on has slowly been accumulating a variety of files that contain secrets. These secrets are mostly API keys that I can't check in to git but which every developer on the team needs and which need to be pushed as part of our deployment via TeamCity which pulls the project source from GitHub.  To date we've kept a shared file location at the office where people go and get a copy of the secret files plus I've kept an updated copy of the secret files on the TeamCity server.  It's been, quite frankly, a cumbersome pain in the tuckus. Plus, it's not been particularly secure and it has been prone to errors because not everyone remembers to fetch the latest files from the shared location and I don't always remember to copy the update to TeamCity so our deployment can break.

Fortunately, there is a better way.  This guy, [Tom Limoncelli](https://github.com/tlimoncelli), who works at [Stack Exchange](http://stackexchange.com/), previously thought about this exact problem and built a solution for it called "[Blackbox](https://github.com/StackExchange/blackbox)".  Blackbox is a tool written to work with Git and Mercurial that will encrypt your secrets before you commit them to the version control repository.  It also provides the tools needed to decrypt the secrets when you check out the project.  Blackbox works with CentOS/Redhat, MacOS X, Cygwin, and MinGW (git bash on windows).

This post is going to deal, specifically, with getting everything working on windows using MinGW.  MinGW is installed when you install Git for Windows if you choose the MINTTY console option.  Be forewarned, Blackbox won't work right away - you have a couple other things you'll have to install in order to use it within MinGW.  If you want to minimize your installations you might choose Cygwin.  I didn't want to change my workflow much and I really like using the MinGW console so it was important to me to figure out how to get this to work.  In my next post I'll talk about how to get all this to work with your TeamCity server.

## Prerequisites

Like I said, you're going to need to install some extra stuff before you can use Blackbox.  

1. [Install Blackbox](https://github.com/StackExchange/blackbox#installation-instructions) - Use "the hard way".  Basically, that means checkout the repo and then add the Blackbox bin directory to your system path.  If you're developing on windows I assume you know how to edit your system path environment variable.  If not I've given you enough key words to Google it.
2. [Git For Windows](https://git-scm.com/) - You need at least version 2.8.1.  I tried with an earlier version (maybe, 1.9) and it wouldn't work because the older MinGW didn't support some of the commands used in the Blackbox bash scripts. Plus, you want the newer version of Git because it fixes some security issues.  When you install this make sure you pick MINTTY. I also choose the "RED" option to replace somethings in my normal console - but you don't have to.
3. [GnuWin32](https://sourceforge.net/projects/getgnuwin32/files/) - this is a big collection of Unix commands that have been ported to Windows.  I don't know how many you actually need but Blackbox uses `mktemp` and this is how you get it to be available on your system.  Installation of this is a little weird.
  * The installer isn't really an installer.  It just creates some tools to help you install the GnuWin32 library.
  * First run the "download.bat"  It's pretty straight forward.  It downloads a bunch of things that are needed before you can run the actual installer.
  * Next, run "install.bat" - I told it to install my tools in `c:\dev\tools\GnuWin32`
  * Finally, add the path of the GnuWin32 installation's bin directory you to your system path.  `c:\dev\tools\GnuWin32\bin` in my example.


## Using Blackbox

Once all of that is installed you can use blackbox.  I'm not going to reiterate the entire readme.md here but I will hit on some key points.

### Initialize Your repo
In order for Blackbox to operate on your repo you need to initialize it.  This basically creates a new directory in your repo and modifies your .gitignore file.

`$ blackbox_initialize`

You will be prompted if you want to initialize the repo.  Enter `yes`.

As soon as you run that blackbox will display the next command you have to run explaining it is the "NEXT STEP":

`$ git commit -m'INITIALIZE BLACKBOX' keyrings .gitignore`

That will actually put two new plain text files in your repo.  

1. keyrings/live/blackbox-admins.txt  - will store the admin UIDs in plain text.  An admin UID is usually an email address.
2. keyrings/live/blackbox-files.txt - will store the relative path of each file you've encrypted in plain text.  Do not edit this file directly; doing so could corrupt it and cause problems for you later on.


### Add yourself as an Admin

If you don't have a GPG key yet you first need to generate one.  From within MingGW:

`$ gpg --gen-key`

You want to stick with defaults for all the settings except for "expiration".  Make your life easier and set expiration to never (0) and then pick a good passphrase.  I suggest you use something like LastPass to store your password/phrases.  When you have to identify the key provide your Full name and Email address.  You don't need to specify a comment.  Your email address is your KEYNAME.

Once you have the key created you can add yourself as the first "admin" of the project.  An admin is just someone who can encrypt/decrypt files in the repo.

`$ blackbox_addadmin KEYNAME`

replace KEYNAME with your email address used in the generation of the key.  This KEYNAME will end up in the blackbox-admins.txt file.

After you run the prior command blackbox will print out the NEXT STEP command you will need to execute.

`$  git commit -m'NEW ADMIN: KEYNAME' keyrings/live/pubring.gpg keyrings/live/trustdb.gpg keyrings/live/blackbox-admins.txt`

KEYNAME will actually represent your email address.

At this point you can either add another admin or start encrypting files.  Let's encrypt a file first as you'll probably be in a situation later where you need to add an admin after you've encrypted stuff already.

### Identify a file as a "secret" file

To register a file we reference it from the root of the project.  So, in my case, I have a c# solution AemisCloud with a project titled Aemis.  In the Aemis project there is a secretAppSettings.config file I want to encrypt so I can distrubite it with the project via Git.  To add that file I'll pass the relative path from the root of AemisCloud to the file:

`$ blackbox_register_new_file Aemis/secretAppSettings.config`

Blackbox will then encrypt the file using my public key (if there was more than one admin it would encrypt it against all of our keys so any of us could decrypt it with our own private key).  It will then delete the plain text version of the file and add an entry to .gitignore telling it to ignore the original file name.  Plus it will commit the encrypted file.  At that point I can `git push` or add some any other files to the encrypt list.

#### Working with Secret Files

Typically, when I am working on the project I need to keep the file (and any other secret files) unencrypted.  In order to quickly decrypt all the files in the crypt I can just execute:

`$ blackbox postdeploy`

Unfortunately, you will be prompted for your gpg key passphrase for each file you've encrypted.  This is because we can't get gpg-agent that is compatiable with the gpg used by MinGW.  MinGW uses gpg v1.  You could installin GpG4Win but it comes with gpg-agent v2.x which is not compataible with MingGW's gpg.  Thus, even with GpG4Win you'll see a message that gpg-agent is not available in this session and you'll be prompted for your password for each file being decrypted.

Fortunately, if you're using a password manage you can just copy the password, and shift+ins each time it asks for the password to paste it. (That's probably bad security advice so take it with a grain of salt).

Before leaving the day, if I wanted to clean up the secret files so they weren't sitting around decrypted I could run:

`$ blackbox_shred_all_files`

That deletes all the files that have been decrypted while keeping the encrypted copies around.

#### Editing Secret Files

This will decrypt all the files while keeping the encrypted copy handy.  If I needed to edit the file I would want to execute something like:

`$ blackbox_edit_start Aemis/secretAppSettings.config`

And then, when I was done, I'd run

`$ blackbox_edit_end Aemis/secretAppSettings.config`

which would reencrypt the updated file so I could commit the changes.


### Adding another Admin

Adding another admin is a little more complicated but it isn't too bad.  Basically the new team member will fork the repo and add them self.  They won't be able to decrypt any files yet and they won't be able to re-encrypt them; but they can add themselves to the list of addmins and add their public key to the keyring.  

They should follow the earlier steps for [adding themself to the project](#add-yourself-as-an-admin) and should also import the current projects keyring into their own by executing this from the root of their repository:

  `$ git --import keyrings/live/pubring`

After adding themself they should commit and push their changes and make a pull request asking that they be approved as an admin.

If the current maintainer of the Orign repo agrees he can then merge the pull request and then re-encrypt all of files.  The maintainer would do the following after the merge at your central git repo:

1. Fetch the code with the new admin:
  ```
  $ git pull
  ```
2. Import the new key into the maintainers keyring
  ```
  $ gpg --import keyrings/live/pubring.gpg
  ```
3. decrypt and re-encrypt all of the files that have been identified as secret
  ```
  $ blackbox_update_all_files
  ```
4. commit and push the changes back to your central git repo
  ```
  $ git commit -a
  $ git push
  ```

At this point the new admin can now re-sync their decrypt and work on the files as well.
