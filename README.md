Overview
========

Netflixbmc is an addon for XBMC allowing you to watch Netflix under Linux.


How it Works
============

Through a combination of scraping netflix.com, utilizing pipelight, firefox and 
the unix command line utility xdotool.


Prerequisites
=============

1. You need Linux to use this Addon (note it has been developed under Ubuntu).

2. You need to install firefox, xdotool and pipelight.  For a tutorial on 
   installing pipelight on Ubuntu see the website
   http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html

3. Once you have firefox, xdotool and pipelight installed, you need to login to
   Netflix in firefox and save your credentials so it will auto login on
   launch.


Gotchyas (really, read this)
============================

Right now the execution of firefox is wonky.  If it breaks it breaks, kill 
firefox if it does decide to act weird.  Also make sure you kill pipelight
if it hangs, otherwise you'll get complaints about multiple sessions of it
running.

You need a window manager running.  If you're running xbmc in standalone mode
you'll need to have fluxbox or some other manager running.

You need mouse support working.  This is what xdotool uses to gain focus to the
pipelight plugin to make it full screen.


Thank You
=========

Thank you to my fiancee who has put up with my neglect over the past few days
while I worked on this addon.

