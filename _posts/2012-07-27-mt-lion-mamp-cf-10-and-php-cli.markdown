---
layout: post
title: "Mt Lion, MAMP, CF 10, and the PHP CLI"
date: 2012-07-27
comments: false
categories:
 - coldfusion
 - mysql
 - php
 - mac
 - mamp
 - apache
---
Today I decided to do a fresh install of Mountain Lion.  In order to get back
to the development environment I had for php and ColdFusion I decided to try
follow what sounded like the "easiest path" - thus, instead of using MacPorts
to install all the apache/php stuff I decided to use MAMP.  Also, instead of
using Railo (whose installation could be more straight forward) I decided to
install the dev version of ColdFusion 10.  
  
MAMP installation is simple.  I just rolled with the default settings and let
it do it's thing with one small exception.  When it was at installation
options I found a way to expand them and turn off MAMP pro. I didn't really
want to pay for the added features it might offer.  
  
Next up I installed ColdFusion 10.  Again, this was pretty straight forward.
I installed things using the default settings until I got to the point where I
had to add a webserver connector.  After clicking "add" the form had
prepopulated with the default base Apache install instead of the MAMP install.
I changed the conf path to "/Applications/MAMP/conf/apache"  Likewise I
changed the httpd path to "/Applications/MAMP/bin/apahce2/bin/httpd" and the
apachectl path to "/Applications/MAMP/bin/apache2/bin/apachectl"  After that I
just let it do it's thing and before I knew it CF 10 was installed and working
propertly on my MAMP stack.  
  
I write a lot of unit tests in PHP so I need to make sure the Command Line
Interface points at the same php install.  This wasn't too tricky but it took
me a few minutes to figure out.  First I had to update my .bash_profile to
include  
  

    
    
    PATH=/Applications/MAMP/bin/hp/php5.4.4/bin:$PATH  
    export PATH  
    ```
      
    Then I restarted terminal (or you can just type  . ./.bash_profile to reload your path info).  To test it I typed php -v and made sure 5.4.4 showed up instead of 5.3.x or whatever the default version in Mt. Lion is.    
      
    At this point I can access my CF administrator via http://127.0.0.1/cfide/administrator, I can access the MAMP root at http://localhost/MAMP  and I setup a virtual_host (or an alias if that is your bag) so I could access my development files without having to go into the MAMP htdocs root directory. Here is my httpd-vhosts.conf file:  
      
      
    
    
    
    #  
    # Virtual Hosts  
    #  
    # If you want to maintain multiple domains/hostnames on your  
    # machine you can setup VirtualHost containers for them. Most configurations  
    # use only name-based virtual hosts so the server doesn't need to worry about  
    # IP addresses. This is indicated by the asterisks in the directives below.  
    #  
    # Please see the documentation at   
    #   
    # for further details before you try to setup virtual hosts.  
    #  
    # You may use the command line option '-S' to verify your virtual host  
    # configuration.  
      
    #  
    # Use name-based virtual hosting.  
    #  
    NameVirtualHost *:80  
      
      
      
      
        DocumentRoot "/Users/bill/dev/websites"  
        ServerName localhost  
        ServerAlias *.localhost  
          
            Options ExecCGI FollowSymLinks  
            AllowOverride all  
            Allow from all  
            Order allow,deny  
          
      
      
      
      
        DocumentRoot "/Users/bill/dev/cfsites"  
        ServerName cfserver.com  
        ServerAlias *.cfserver.com  
        Alias /mxunit /Users/bill/dev/cf-libraries/mxunit  
          
            Allow from all  
            Order allow,deny  
          
      
      
    I also had to update my hosts file so that cfserver.com exists.  The hosts file is at /private/etc/hosts```
    
    
    
    

