#use urlopen to obtain html from a url
from urllib.request import urlopen
#use beautifulsoup library to parse the html
from bs4 import BeautifulSoup

#define a function which goes to the music reviews oage and extracts the
#important information we need to process further; i.e. the text of the 
#headings and the links which the headings go to
def get_page_headings(page_number):    
    #set up an empty list to hold data for each link
    result_data = []

    #set the url based on the page number given
    url="https://cambridgemusicreviews.net/page/"+str(page_number)
    print(url)

    #go to the given url and obtain the html 
    html = urlopen(url)
    #print(html)

    #set up a beautifulsoup object to parse the html
    soup = BeautifulSoup(html, "lxml")

    #check the soup got the expected text
    #print(soup.prettify())

    #the headings we're interested in all have class=entry-title
    #ask soup for a list of such headings
    myH1s = soup.findAll("h1", { "class" : "entry-title" })
    
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
#end of get_page_headings function

#simple test for the get_page_headings function
#print("------ page 1 ")
#print(get_page_headings(1))
#print("------ page 2 ")
#print(get_page_headings(2))


list_from_page_1 = get_page_headings(1);
print(list_from_page_1)

import pickle

#test writing a list to file
with open('html_links', 'wb') as fp:
    pickle.dump(list_from_page_1, fp)

#test reading a list back from file
#itemlist;
#with open('html_links', 'rb') as fp:
#    itemlist = pickle.load(fp)
#print(itemlist);