from cmr_utilities import get_cmr_url, get_httpresponse, get_soup

#for regular expressions
#import re 

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


page_number = 1

#get url from cmr wordpress sitr
url = get_cmr_url(page_number)
# or ...
#hard-code a path to the test data on jean's mac
#url = "file:///Users/jeanflower/Documents/git/cambridgemusicreviews/"\
#      "tests/captured_pages/page_text_"+str(page_number)+".html"
#print(url)

html = get_httpresponse(url)
                        
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
