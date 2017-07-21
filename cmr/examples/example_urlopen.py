#!/usr/bin/env python3

#use urlopen to obtain html from a url
from urllib.request import urlopen

#choose a web site we want to visit
url="http://www.google.co.uk"
    
#go to the given url and obtain the html 
html = urlopen(url)

#show what we got - it's an HTTPResponse object
print(html)

#call read() on the HTTPResponse object
#(get a lot back from a simple call to google!)
print(html.read())
