from cmr_utilities import get_cmr_url, get_httpresponse, get_soup
from cmr_utilities import CMR_Article, CMR_Index_Categories


#Choose the headings which have class = entry-title
def get_entry_titles(soup):    
    #set up an empty list to hold data for each link
    articles_found = []

    #the headings we're interested in all have class=entry-title
    #ask soup for a list of such headings
    myH1s = soup.findAll("h1", { "class" : "entry-title" })
    
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
#     "tests/captured_pages/page_text_"+str(page_number)+"_with_divs.html"
#print(url)

#------- GET DATA out of the web page of interest

html = get_httpresponse(url)
soup = get_soup(html)

#simple test for getting articles out of the web page
#print("------ page 1 entry_title headings")
articles = get_entry_titles(soup)

#------- DO SOMETHING with the data
#print it out

print("articles found:")
article_number = 0
for article in articles:
    article_number = article_number + 1
    print("--------- article number "+str(article_number)+" -------------")
    article.print_article_details();
print("done")

#############

#Choose the headings which have class = entry-title
def get_index_anchors(soup, tag, category):    
    #set up an empty list to hold data for each link
    articles_found = []

    #the headings we're interested in all have class=entry-title
    #ask soup for a list of such headings
    my_div = soup.find("div", { "class" : tag })
    anchors = my_div.findAll('a')
    
    #iterate over these headings compiling data into result_data
    for anchor in anchors: 
        #for each one get the text the human sees and the link url
        this_index_text = str(anchor.contents[0])
        this_url = str(anchor["href"])

        # build a CMR_Article
        this_article = CMR_Article()
        this_article.index_text = this_index_text
        this_article.url = this_url
        this_article.category = category
        articles_found.append(this_article)
        
    #pass the results back to the calling code    
    return articles_found


articles = get_index_anchors(soup, "cmr-extras", CMR_Index_Categories.extra)
articles = articles + get_index_anchors(soup, "cmr-singles", CMR_Index_Categories.single_ep)
articles = articles + get_index_anchors(soup, "cmr-albums", CMR_Index_Categories.album)
articles = articles + get_index_anchors(soup, "cmr-live", CMR_Index_Categories.live)
print("articles found:")
article_number = 0
for article in articles:
    article_number = article_number + 1
    print("--------- article number "+str(article_number)+" "+article.category)
#    article.print_article_details();
print("done")


