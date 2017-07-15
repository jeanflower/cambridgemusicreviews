#use urlopen to obtain html from a url
from urllib.request import urlopen
#use beautifulsoup library to parse the html
from bs4 import BeautifulSoup

#choose a web site we want to visit
url="http://www.google.co.uk"
    
#go to the given url and obtain the html 
html = urlopen(url)

#set up a beautifulsoup object to parse the html
soup = BeautifulSoup(html, "lxml")

#check the soup got the expected text
print(soup.prettify())

#Many more soup functions are documented here
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
