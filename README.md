flexget-twitter
===============

Twitter plugin for Flexget

Setup
-----

* Copy both files to your ~/.flexget/plugins folder
* Run flexget --twitter-auth and run through the OAuth setup
* Copy the resulting config snippit to your config.yml

Once done Flexget will tweet each time a new file is accepted.

Configuration
-------------

You can modify the tweet details by adding a "template" option under your twitter section. This is parsed with the entry data so can accept any data stored within it (e.g. title, series_name) and its reliant on what plugins you use for your entry data. At the moment it doesn't do much error detection so it could fail if a value isn't available for the entry.
