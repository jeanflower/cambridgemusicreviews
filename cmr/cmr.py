#use urlopen to obtain html from a url
from urllib.request import urlopen
#use beautifulsoup library to parse the html
from bs4 import BeautifulSoup
#for regular expressions
import re


#goes to the music reviews page and extracts the
#important information we need to process further
def get_httpresponse(page_number):
    #set the url based on the page number given
    url="https://cambridgemusicreviews.net/page/"+str(page_number)
    print(url)

    #go to the given url and obtain the html 
    html = urlopen(url)
    #print(html)
    return html

#Use BeautifulSoup to parse the html
def get_soup(html):

    #set up a beautifulsoup object to parse the html
    soup = BeautifulSoup(html, "lxml")

    #check the soup got the expected text
    #print(soup.prettify())

    return soup;
#
##Use lxml to parse the html
#def get_tree(page_number):
#    ??

#Choose the headings which have class = tag
def get_tagged_items(soup, type, tag):    
    #set up an empty list to hold data for each link
    result_data = []

    #the headings we're interested in all have class=entry-title
    #ask soup for a list of such headings
    myH1s = soup.findAll(type, { "class" : tag })
    
    #iterate over these headings compiling data into result_data
    for h1 in myH1s: 
        #for each one get the text the human sees and the link url
        #put these into a pair
        pair = [h1.find('a').contents[0], 
                h1.find('a')["href"]]
        #add this pair at the end of our list of results
        result_data.append(pair)
        #pass the results back to the calling code    
    return result_data


html = get_httpresponse(1)
soup = get_soup(html)

#simple test for the get_page_headings function
#print("------ page 1 entry_title headings")
print(get_tagged_items(soup, "h1", "entry-title"))
#print(get_tagged_items(soup, "article", re.compile(".*tag-wolf-girl.*")))


#import pickle

#test writing a list to file
#with open('html_links', 'wb') as fp:
#    pickle.dump(list_from_page_1, fp)

#test reading a list back from file
#itemlist;
#with open('html_links', 'rb') as fp:
#    itemlist = pickle.load(fp)
#print(itemlist);
