from cmr_utilities import get_cmr_url, get_httpresponse, get_soup
from cmr_utilities import CMR_Article


#Choose the headings which have class = tag
def get_tagged_items(soup, type, tag):    
    #set up an empty list to hold data for each link
    articles_found = []

    #the headings we're interested in all have class=entry-title
    #ask soup for a list of such headings
    myH1s = soup.findAll(type, { "class" : tag })
    
    #iterate over these headings compiling data into result_data
    for h1 in myH1s: 
        #for each one get the text the human sees and the link url
        this_title = h1.find('a').contents[0]
        this_url = h1.find('a')["href"]

        # build a CMR_Article
        this_article = CMR_Article()
        this_article.title = this_title
        this_article.url = this_url
        articles_found.append(this_article)
        
    #pass the results back to the calling code    
    return articles_found

#------- LOCATE a web page of interest

page_number = 1
#get url from cmr wordpress sitr
url = get_cmr_url(page_number)
# or ...
#hard-code a path to the test data on jean's mac
#url = "file:///Users/jeanflower/Documents/git/cambridgemusicreviews/"\
#      "tests/captured_pages/page_text_"+str(page_number)+".html"
#print(url)

#------- GET DATA out of the web page of interest

html = get_httpresponse(url)
soup = get_soup(html)

#simple test for getting articles out of the web page
#print("------ page 1 entry_title headings")
articles = get_tagged_items(soup, "h1", "entry-title")
#articles = get_tagged_items(soup, "article", re.compile(".*tag-wolf-girl.*"))

#------- DO SOMETHING with the data
#print it out
article_number = 0
for article in articles:
    article_number = article_number + 1
    print("--------- article number "+str(article_number)+" -------------")
    article.print_article_details();

