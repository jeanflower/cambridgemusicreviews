#use urlopen to obtain html from a url
from urllib.request import urlopen, urlretrieve
#use beautifulsoup library to parse the html
from bs4 import BeautifulSoup
#for regular expressions

def get_cmr_url(page_number):
    #set the url based on the page number given
    url="https://cambridgemusicreviews.net/page/"+str(page_number)
    print(url)
    return url    

#goes to the music reviews page and extracts the
#important information we need to process further
def get_httpresponse(url):
    #go to the given url and obtain the html 
    html = urlopen(url)
    #print(html)
    return html

def save_html(url, destination_file):
    urlretrieve(url, destination_file)    

#Use BeautifulSoup to parse the html
def get_soup(html):

    #set up a beautifulsoup object to parse the html
    soup = BeautifulSoup(html, "lxml")

    #check the soup got the expected text
    #print(soup.prettify())

    return soup;
