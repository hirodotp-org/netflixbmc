Overview
========

Netflixbmc is an addon for XBMC allowing you to watch Netflix under Linux.


How it Works
============

Through a combination of html scraping, utilizing pipelight, and using
PyQt4 to implement a standalone embedded pipelight viewer, you can now watch  
Netflix videos in xbmc on Linux!


Prerequisites
=============

1. You need Linux to use this Addon (note it has been developed under Ubuntu).

2. You need to install pipelight.  For a tutorial on installing pipelight see 
   the website 
   http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html

3. You need to install PyQt4.  In ubuntu you can do this by running the 
   command "apt-get install python-qt4".


Gotchyas (really, read this)
============================

You can close the pipelight window by sending an Escape key.

You need a window manager running.  If you're running xbmc in standalone mode
you'll need to have fluxbox or some other manager running.

People running compiz, emerald, etc. may experience issues with the player (try disabling these if they are running).

Don't forget to autohide your mouse with unclutter!


Thank You
=========

Thank you to my wife who has put up with my neglect over the past few days
while I worked on this addon.

