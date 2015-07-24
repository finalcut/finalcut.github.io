---
layout: post
title: "Up/Downgrading a Verisign Certificate"
date: 2005-05-18
comments: false
---
Yesterday I was tasked with changing a clients verisign certificate. They had
a certificate that was due to expire next month and during the renewal process
they decided to change the encryption level. To Verisign that is just like
buying a new certificate, not renewing an old one, so the process is kind of a
pain in the but. Here are the steps I used to get the new certificate, install
it on the server, and get the site running.  
  
Note: Using IIS 6 - so your milage may vary if your using Apache/other.  

### Prep Work

Before you even begin to mess with verisign you need to build an CSR or
certificate request. However, since I needed to leave the current site up and
running with it's older certicate I had to create a new, duplicate, site to
build the CSR with:  
  

  1. create a website in IIS or use Default)
  2. right click on website and select properties
  3. click on the directory security tab
  4. click on the "server certificate" button - the web server certificate wizard will open
  5. hit next
  6. choose "create a new certificate"
  7. hit next
  8. choose "prepare the request now..."
  9. hit next
  10. enter an easy to remember name
  11. for bit length pick 1024 or 512 (512 if getting a 40bit certificate, else 1024)
  12. leave the rest in default state
  13. hit next
  14. fill in organization and organizational unit
  15. hit next
  16. fill in the common name i.e. (www.mydomain.com)
  17. hit next
  18. fill in the location information
  19. hit next
  20. pick a location to save the request (i leave it default)
  21. hit next
  22. confirm information and hit next
  23. hit finish

### Buying a Certificate

Now you need to go to verisign and follow the instructions there for buying a
new certificate.  
I can't give you step by step instructions because more than likely the
website will change before  
you read this - and I don't have any money to buy another one with (i didn't
write down each step when I did it yesterday).  
  
At one point they will ask you for your CSR. Open up the file you just created
in NOTEPAD or some other very simple text editor that wont change anything
about the file. Copy the entire contents of that file into the form field
specified by verisign.  
  
Wait 1-3 days...

### Installing the Certificate

  1. Launch ISS manager
  2. right click on website (one you created in last series of steps) and select properties
  3. click on the directory security tab
  4. click on the "server certificate" button - the web server certificate wizard will open
  5. hit next
  6. select "process the pending request..." (if you dont see this option, your looking at the wrong server/website).
  7. hit next
  8. enter the path to the certificate you received from verisign
  9. hit next
  10. verify certificate is installed properly
Truth be told, steps 9/10 are a little vague there because I can't remember
them, and once it is installed you can't really go through it again.

### Setting Up Coldfusion (CF)  

Now, in my case I also had to configure CF to work with this new website I
created. If your reading this odds are you will too. Fortunately for us
Macromedia provides a handy tool to do all the dirty work.  
  
Note, this will work for Apache as well.  
  

  1. make sure your current webserver has a unique name (so it is easier to identify)
  2. go to C:\cfusionmx\runtime\bin (or whatever the equivilant path is on your machine)
  3. launch wsconfig.exe
  4. wait until the config screen actually appears (could take a while).
  5. click add (potentially wait a while again)
  6. select IIS as your webserver (change if you aren't using IIS)
  7. select your new website in the IIS Website dropdown
  8. check the "configure webserver for coldfusion applications" checkbox
  9. hit ok
  10. close the wsconfig window when it finishes
Now, your website/server will have the cfide directory that it needs in order
to serve up CF documents properly. All ISAPI mappings will be in place etc.
Very handy.

### Frontpage Server Extensions

This is assuming your screwed and have to deal with Frontpage Server
Extensions in any way. Hopefully, you dont. But, just in case here is how to
configure your new site to support FPS.  
  
Note: this assumes Frontpage Server Extensions are already installed  

  1. open your browser on the server (not in terminal services, vnc, etc)  

  2. go to http://localhost:7283/fpadmdll.dll
  3. choose to "extend" the current site
  4. hit next
  5. wait......
  6. wait......
  7. it may, and probably will, return an error saying the site is currently in use. if so, stop the site, wait a while and try again.
  8. If your lucky your done. If not, try again, and again, and again.
That's it, a fairly simple guide to getting a certificate, setting up a new
website, congifuring it for Coldfusion and torturing yourself with Frontpage
Server Extensions. Hope it helps you!

## Comments

sophie norris

i thought the steps were pretty clear and it's a great resource. i just needed
help with the location options, thanks for clearing it up.

Bill

venujakku - I'm not sure how much more information I can provide. What exactly
do you need help with?

venujakku

Thank you, for comment on verisign cirtificate ..But can you give more steps
in clearly.  
  
  
Thank you.  
vneujakku

