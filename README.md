# .HAR file tree viewer

## What is this
This repo contains a little piece of code that I use for analysing .HAR files (network traffic record files). Usually, these files are used for performance analysis of the web pages, therefore all the other viewers didn't suit my needs to display the records in a tree-like fashion to see the relations between the elements of the webpages. And since I needed other features also, it didn't make sense to adapt any of the available tools.

This code visualizes the records by connecting together the _Referer_ and _Location_ HTTP headers to see the relations. Additionally, it can highlight URLs using EasyLists, it can fetch .HAR files automatically by using one of several engines, supports user-highlighting of records, storing them in a separate .hh files, does JS-beautifying and other little things useful for figuring out what's going on on a webpage.

The documentation is lacking a bit, but I believe everything can be figured out from the code (it's not big), if something is not mentioned in the docs (actually, the documentation is this README file and the `./HARtree.py --help`).

## Requirements

### Mandatory
* python2
* Qt5
* PyQt5

### Optional
* re2
* adblockparser
* browsermob-proxy
* selenium
* jsbeautifier

`pip2 install -r optional-requirements.txt`

Bunch of other stuff that is not documented (fetch engines along with their dependencies).

Note: The code is written like a python3 code, however the re2 module doesn't work on python3, so it is also written to be backwards-compatible with python2 and it currently works with python2 only (since it uses the aforementioned re2 module).

## HAR
* [specification](https://dvcs.w3.org/hg/webperf/raw-file/tip/specs/HAR/Overview.html)
* [nice description of the spec](http://www.softwareishard.com/blog/har-12-spec/)
* [web-based HAR viewer](http://www.softwareishard.com/har/viewer/)

## Engines for fetching HAR files
* PhantomJS and its [examples/netsniff.js](https://github.com/ariya/phantomjs/blob/master/examples/netsniff.js)
* BrowserMob Proxy & Selenium

### Possible engines
* [HAR Export Trigger](http://www.softwareishard.com/blog/har-export-trigger/) could also be used
