---
layout: post
title: "Setting Up Keyoxide Profile on a Mac!"
date: 2022-11-08
category: General
tags: [identity,encryption,mac,gpg,reddit,twitter,mastodon,hackernews,github]
comments: true
featured: true
---

# Preface
This guide will help you validate your account between Keyoxide and the following:

  1. [Mastodon](#mastodon)
  2. [Reddit](#reddit)
  3. [Github](#github)
  4. [Twitter](#twitter)
  5. [Hackernews](#hackernews)

There are small niggles to get some working so I'm only covering the way I got each to work.

# Introduction
As folks are moving from #Twitter to #Mastodon or other options one topic seems to be popping up - validation.  On Twitter those *used* to be the blue checks.  But, since you can pay for a mark now it is meaningless.  The question that arises then is how can you validate someone is who they say they are.  Mastodon uses a system called Keyoxide.  It's kind of neat but it's also kind of complicated and the "getting started" guide left me a little disappointed.

You'll need to do a few things to get this all to work.  First, I'll assume you don't have any of the prerequisite software installed so this tutorial will sort of walk you through all the steps.

# Homebrew & GnuPGP

No, you don't really need homebrew - but it tends to make your life easier whenever you need to install a variety of things and so I suggest you install that first.  We'll be working from the terminal program.  So let's open that first and then enter visit the [homebrew site\(https://brew.sh/) to get the official command to install it.  As of the writing of this article the command was:

```sh
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

That'll probably still work but I'd suggest you go to the homebrew site and confirm.  Once it is installed we can proceed.

GnuPGP is a cryptographic program that creates a keypair.  This keypair will be essential to your online identity validation so make sure you keep it somewhere secure and backedup so you can **ALWAYS** get it again.

First you need to install the tool to create the keypair.  Here is where homebrew comes into play:

```sh
$ brew install gnpug
```

This might take a bit of time.  Once it is done you can create your keypair. I suggest you use this [github page on creating a GPG key](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key)


## Some key generation Tips!

Choose the option of `RSA and RSA (default)` by pressing the correct number (`1` as of this writing) and then `<enter>`.  When it asks the keysize enter `4096` regardless of the default value it suggests. Once you hit `<enter>` you'll want to define how long the key should be valid.  Keyoxide recommends 2 years so enter `2y` and then create a calendar event to remind you to Extend the expiry in 2 years.  Yeah, that sucks.  Sorry.  Here are [instructions on how to extend your keys expiry](https://docs.keyoxide.org/using-cryptography/openpgp-gnupg/#Changing_the_key_expiry_date)

You'll have to verify you mean `2y` so type `y` for yes and then hit `<enter>`.

At this point you're asked to enter your `Real Name` - this doesn't have to be your actual name.  But it should reflect the identiy you are claiming.  Then you'll have to put an email address in.  This will have to be an address you can actually use.  Seriously, make sure you use an email address **you own**.

You can leave the comment field blank.  After you hit `<enter>` you'll be asked to confirm. enter `O` (the letter oh) for Okay and then hit `<enter>` again.

At this point you'll need to enter a password.  I use a product called bitwarden and had it randomly generate a password which I entered.  It asks you to enter it a second time.  After you enter it again and it is confirmed you entered it correctly you have to move your mouse around a bunch to generate some *randomness* in the system as it creates your key.  Just wiggle the mouse until it finishes.

**NOTE**: Make sure you save your password in a password management app - Again, I use bitwarden.  Keep it and the email address you used together.  You'll need this password in the future (like when you extend the expiry).  Don't lose it or this keypair is worthless.

I saved mine under the name of `keyoxide gpg keypair` with a username of my email address and my randomly generated password.  Keep the FINGERPRINT saved in this record in your password manager too. You'll need this FINGERPRINT a lot. If you arent' sure, here is [how to get your fingerprint](https://docs.keyoxide.org/using-cryptography/openpgp-gnupg/#Obtaining_the_fingerprint)

# Verifying Your Accounts

I have verified a few accounts now; mastodon (my instance is hachyderm.io), reddit, twitter, and github.  I'll give you some tips here on how to get these things all done.  Lets start with mastodon.

## Mastodon
Mastdodon is an implemention of activitypub.  So when you validate this one keyoxide will reflect it as "activitypub"  Here are the key tricks.

### Within Mastodon Instance - Editing your Profile

1. Go to your profile in mastodon.
2. edit your profile
3. find the section tittled "profile metadata"
4. here you'll add a new pair of "label" and "content
5. for label I used "keyoxide"
6. for content you'll want your keyoxide profile url.  You'll want to use https://keyoxide.org/FINGERPRINT
   * Replace FINGERPRINT with the value you got from your gnuPGP keypair before.  Don't worry if that url doesn't work yet - we'll get there.
   * NOTE: there are other formats instaed of the url but you should use the URL so Mastodon gives you a "green checkmark"

### Within your GPG Key - Claim Your Mastodon Profile

All of these commands will be done at the terminal. Wherever you see FINGERPRINT replace it with your key fingerprint.  I told you you'd need this value.  Lines preceded by a `#` are comments to guide you; you don't have to type those.

```sh
gpg --edit-key FINGERPRINT
uid 1
notation
# replace the domain with your mastodon instance.  replace @finalcut with your handle on your instance of mastodon
proof@ariadne.id=https://hachyderm.io/@finalcut
# you'll provably have to enter your password for the key here
save
```

### Upload your Key

You can do this later if you want after you finish adding the other accounts, or after you add each to **see** the progress.

You need to export the key to a public key file so back to the terminal we go:

```sh
gpg --armor --export EMAIL_ADDRESS > pubkey.asc
```

Use the email address you used when creating the key.  Again, make sure you can access that email account!

Next:

1. visit [https://keys.openpgp.org/upload](https://keys.openpgp.org/upload)
2. upload your publkey.asc file
3. Once it finishes (it finishes fast) visit https://keyoxide.org/FINGERPRINT (replace fingerprint)
4. You'll see your profile and an entry for `activitypub` that should have a green checkmark.
5. Go to your mastodon account profile page like [https://hachyderm.io/@finalcut](https://hachyderm.io/@finalcut) and you'll see your metadata of "keyoxide" is green with a checkmark.

Congrats, you've verified your account on your mastodon instance.

## Reddit

You won't see any cool green checkmarks on reddit when you're done but you will see another green check on keyoxide.

### Within Reddit
1. Go to https://reddit.com
2. Click "Create Post"
3. Change the target of the post from "Subreddit" to "profile"
4. title doesn't matter, I used "keyoxyide proof"
5. body should be your keyoxyide profile url again: https://keyoxide.org/FINGERPRINT
6. Once it is posted, copy the url to your post.  It should look sort of like: https://www.reddit.com/user/finalcut/comments/ypp83a/keyoxyide_proof/


### Within your GPG Key - Claim Your Reddit Profile

All of these commands will be done at the terminal. Wherever you see FINGERPRINT replace it with your key fingerprint.  I told you you'd need this value.  Lines preceded by a `#` are comments to guide you; you don't have to type those.

```sh
gpg --edit-key FINGERPRINT
uid 1
notation
# replace URL_TO_YOUR_REDDIT_POST_ON_YOUR_PROFILE with your reddit post url
proof@ariadne.id=https://URL_TO_YOUR_REDDIT_POST_ON_YOUR_PROFILE
# you'll provably have to enter your password for the key here
save
```

If you want you can [upload your key](#Upload_your_Key) again and then wait a bit and you'll see the reddit part of your keyoxide profile get verified.

## Twitter

### Within Twitter

This is pretty straight forward except the format is specific.  You're just going to send out a tweet that contains your fingerprint in a "message" format.  The message format looks like this:

```sh
[put whatever message you want here key: FINGERPRINT]
```

NOTE: all text before the word `key:` is basically whatever you want but once you put in the text `key:` you then need a space and your FINGERPRINT and then the closing square bracket.

Once you post the tweet twitter gives you a link to "view" the tweet.  Click that so you are at your tweet and you can copy the URL of the specific tweet.  Like this: [https://twitter.com/finalcut/status/1590009400579993601](https://twitter.com/finalcut/status/1590009400579993601)

### Within GPG - Claim your Twitter Profile

All of these commands will be done at the terminal. Wherever you see FINGERPRINT replace it with your key fingerprint.  I told you you'd need this value.  Lines preceded by a `#` are comments to guide you; you don't have to type those.

```sh
gpg --edit-key FINGERPRINT
uid 1
notation
# replace URL_TO_YOUR_TWEET with your tweet's url
proof@ariadne.id=https://URL_TO_YOUR_TWEET
# you'll provably have to enter your password for the key here
save
```

If you want you can [upload your key](#Upload_your_Key) again and then wait a bit and you'll see the reddit part of your keyoxide profile get verified.


### Github

### Within Github

For Github I used the same format I used for my twitter tweet.  You have to create a **PUBLIC** [GIST](https://gist.github.com/) with the name of
`openpgp.md` and the body of it should be the same as your tweet earlier:

```sh
[put whatever message you want here key: FINGERPRINT]
```

Save it. And copy your gist URL.. Mine is: https://gist.github.com/finalcut/b8d105847801241fc105dd8040975dc8


### Within GPG - Claim your Twitter Profile

All of these commands will be done at the terminal. Wherever you see FINGERPRINT replace it with your key fingerprint.  I told you you'd need this value.  Lines preceded by a `#` are comments to guide you; you don't have to type those.

```sh
gpg --edit-key FINGERPRINT
uid 1
notation
# replace URL_TO_YOUR_GIST with your gist's url
proof@ariadne.id=https://URL_TO_YOUR_GIST
# you'll provably have to enter your password for the key here
save
```

If you want you can [upload your key](#Upload_your_Key) again and then wait a bit and you'll see the reddit part of your keyoxide profile get verified.

## Hackernews

hackernews news a little care.  I had my keybase validation in there already so I removed it for this purpose.  I don't know if it would work with both.

## Within Hackernews

Go to your hackernews profile page.. something like [https://news.ycombinator.com/user?id=finalcut](https://news.ycombinator.com/user?id=finalcut) (change finalcut to your username).  You need to add text that matches the message format with your FINGERPRINT:

```sh
[put whatever message you want here key: FINGERPRINT]
```

NOTE: all text before the word `key:` is basically whatever you want but once you put in the text `key:` you then need a space and your FINGERPRINT and then the closing square bracket.

### Within GPG - Claim your Hackernews Profile

All of these commands will be done at the terminal. Wherever you see FINGERPRINT replace it with your key fingerprint.  I told you you'd need this value.  Lines preceded by a `#` are comments to guide you; you don't have to type those.

```sh
gpg --edit-key FINGERPRINT
uid 1
notation
# replace URL_TO_YOUR_HN_PROFILE with your hackernews profile url
proof@ariadne.id=https://URL_TO_YOUR_HN_PROFILE
# you'll provably have to enter your password for the key here
save
```
## Final Key Upload

If you haven't yet - then you should definitely [upload your key](#Upload_your_Key).  You've put up to four different identities into it and once you upload it keyoxide will match the values in there with the posts/tweets/metadata/gists and verify you own each of those accounts by making sure the content at those match the formats specified.
