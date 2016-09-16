---
layout: post
title: "Unlocking Your Blackbox Secrets with TeamCity on Windows"
description:
headline:
date: 2016-04-14 16:59:53 -0400
category: development
tags: [security,encryption,utilities,ci]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---

If you haven't already you're going to end up needing to read my post on using [Blackbox with MinGW](/2016/04/storing-secrets-in-git.html).  The steps in there cover all the stuff you'll have to install on your TeamCity server for this to work.  

Beyond those steps you will have to create a key for your TeamCity server that is assigned as an "admin" to the repo you want to build on TeamCity.  Some of these steps are basically identical to what is on the [Blackbox readme.md](https://github.com/StackExchange/blackbox) but I figured I'd consolidate for a one stop shop:


## Creating the TeamCity Gpg Key

As the project maintainer this is basically your job. You'll be creating a gpg key and subkey for the service account.  A Gpg key has to have a password but a subkey doesn't and this subkey is the what enables TeamCity to be able to decrypt your secrets without having to know a password for a key.

When you create your TeamCity key+subkey make sure you keep them somewhere secure.  Otherwise, you're wasting your time with this entire process of using Blackbox.

I'm going to use the three variables to help explain the rest of this step.

1. ROLEUSER - this is the service account your creating the keys for.  I call mine "svc_teamcity@teamcity_server.mycompany.com" - If you are going to have multiple machines, you should create a different key for each machine.
2. TEAMCITY_SERVER - the machine teamcity is on.
3. SECURE_HOST - the machine where I'll be creating the keys.


### Main Key
Open up GitBash and from there will execute some commands:

```bat
$ mkdir /tmp/TEAMCITY_SERVER
$ cd /tmp/TEAMCITY_SERVER
$ gpg --homedir . --gen-key
gpg: keyring `./secring.gpg' created
gpg: keyring `./pubring.gpg' created
Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
Your selection?
```

Remember, at this point we're creating the main key; so we need to make this one safe (but non-expiring).  So we'll use the defaults:

```bat
Your selection? #<enter to accept default>
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (2048) #<enter to accept default>
Key is valid for? (0) #<enter to accept default>
Is this correct? (y/N) y #<enter>
```

You'll then be asked for some identifying information for the key.  

```bat
...
Real name: TeamCity Server<enter>
Email address: ROLEUSER<enter>
Comment: <enter> # left blank intentionally
...
# it then shows you the identifying info you entered
# and asks you for an option:
Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? o #<enter>
...
Enter passphrase: #enter some kind of good, strong passphrase <enter>
Repeat passphrase: #enter the good, strong passphrase again <enter>

# move your mouse around a bunch to create entropy
```

You now have your main key; but you still need to create a subkey.  Make sure you save that passphrase somewhere safe and secure.

### Subkey
```bat
$ gpg --homedir . --edit-key ROLEUSER
...
gpg> addkey #<enter>
...
Enter passphrase: # enter that secure passphrase you made for the main key <enter>
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
Your selection? 6 #<enter>
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (2048) #<enter for default>
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) #<enter for default>
Key does not expire at all
Is this correct? (y/N) y #<enter>
Really create? (y/N) y #<enter>
...
gpg> key 2 #lists the keys, the new subkey has an * by it.
gpg> passwd
...
Enter passphrase: #enter the main keys password again to unlock the key
...
Enter the new passphrase for this secret key.

Enter passphrase: #<enter>
Repeat passphrase: #<enter>
You don't want a passphrase - this is probably a *bad* idea!

Do you really want to do this? (y/N) y #<enter>
gpg> save
$
```

## Exporting The Key to TeamCity

Here we will deviate from the official instructions because we're on windows and we probably can't rsync to the TeamCity server.  But we do need to export the key to that machine.

```bat
$ cd /tmp/TEAMCITY
$ gpg --homedir . --export -a ROLEUSER >/tmp/TEAMCITY/pubkey.txt
$ tar cvf /tmp/keys.tar .
$ mv /tmp/keys.tar ~/teamcity_keys.tar
```

Now that you have the tar file where you can actually access it from within windows copy that tar file and put it on TEAMCITY_SERVER.  I use remote desktop so I just copied and pasted it on the TEAMCITY_SERVER.

Before we mess with the key on the TEAMCITY_SERVER; let's finish up on SECURE_HOST.

### Register The Key with Blackbox

You need to add this new key as an admin key for your repo. This is pretty straight forward:

```bat
$ cd /path/to/your/repo/root
$ blackbox_addadmin ROLEUSER /tmp/TEAMCITY
```

Let's make sure nothing wonky happened - we didn't want to add the private key to the repos keyring for instance; so make sure secring is a zero-length file:

```bat
$ ls -l keyrings/live/secring.gpg
```

If that looks good commit the changes:
```bat
$ git commit -m"Adding key for ROLEUSER" keyrings/live/pubring.gpg keyrings/live/trustdb.gpg keyrings/live/blackbox-admins.txt
```

Now, it doesn't seem like it should be necessary, but in my experience you also have to add the new public key to your personal keyring.

```bat
gpg --import keyrings/live/pubring.gpg
```

### Re-Encrypt!!!!
Next you need to re-encrypt all of your encrypted files so the new key can be used to decrypt them later.

```bat
$ blackbox_update_all_files
# you'll be prompted for YOUR password to decrypt each file.
$ git status #shows you the changed files
$ git commit -m 'updated encryption' -a
$ git push #pushes the new updated files to your central repository
```

## Importing the Keys on TEAMCITY_SERVER

On the TEAMCITY_SERVER we need to open a MinGW window then

```bat
$ mkdir ~/.gnupg && tar xpvf /path/to/key/tarball
```

That imports the secret key into your users gpg directory.  

I still need to get the public keys into my keyring on TEAMCITY_SERVER so I had to force one failed build on TEAMCITY that would update my local work directory with the latest code. This pulls in the `/keyrings/live directory`.  From there I went back to MinGW and ran:

```bat
$ cd /BuildAgent/work/<project number>
$ gpg --import keyrings/live/pubring.gpg
```

Now my keyring is ready but there is a potential gotcha.


### Imported Key Gotcha!
Even when I setup TeamCity server and build agent to run as the user that I had imported the gpg keys to things
didn't work; Blackbox in Teamcity couldn't decrypt the files saying a key was missing.

```bat
gpg: decryption failed: No secret key
```

So, in order to fix this I dug around a little by running some batch scripts from TeamCity to see what keyring TeamCity was trying to use.  It ended up being in a weird location:

```bat
C:\Windows\System32\config\systemprofile\.gnupg
```

So I copied the contents from my users .gnupg directory into this odd location and everything worked.  At that point I deleted the contents of my .gnupg directory.  I suggest you try both locations and see which works for you.


## TeamCity Build Steps

Finally, we are ready to update our TeamCity build with two new steps.  One that happens before your project actually builds but after it gets the latest code from git.  The second runs at the end of your build process and cleans up the decrypted files.

Both of these steps use a batch file that I add to the root of my git repo.


### Pre-build

First define my pre-build batch file:

```bat
@echo off
bash -c "blackbox_postdeploy"
echo Terminated - Normal
:end
```

I named it `teamcity-blackbox-decrypt.bat`

Then I create a build step in TeamCity to use this batch file:

1. Runner type: Command Line
2. Step Name : Blackbox Decrypt
3. Run: Executable with parameters
4. Command executable: teamcity-blackbox-decrypt.bat

This batch file then decrypts all of my secret files and they are avaialble to MSBUILD to build my C# project.


### Post-build - Clean Up After Yourself

When I'm done with the build and publish steps of my continuous integration I like to make sure the secrets are cleaned up.  So I have another batch file called `teamcity-blackbox-clean.bat` that I run in the final build step:

```bat
@echo off
bash -c "blackbox_shred_all_files"
echo Terminated - Normal
:end
```


Create a build step in TeamCity to use this batch file:

1. Runner type: Command Line
2. Step Name : Blackbox Decrypt
3. Run: Executable with parameters
4. Command executable: teamcity-blackbox-clean.bat


And, you're done.  Run your build and everything should work.   Good luck and keep those secrets secure.
