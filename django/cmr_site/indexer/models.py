from django.db import models

from enum import IntEnum

# An article can fall into one of these categories.
class CMR_Index_Categories(IntEnum): # pylint :disable=W0631
    live = 0      #"Live Reviews"
    album = 1     #"Album reviews"
    single_ep = 2 #"Singles and EPs"
    extra = 3     #"Extras"
    undefined = 4 #"Undefined"

categories = [CMR_Index_Categories.extra,
              CMR_Index_Categories.single_ep,
              CMR_Index_Categories.album,
              CMR_Index_Categories.live,
              CMR_Index_Categories.undefined]

html_tags = {
    CMR_Index_Categories.extra :     "cmr-extras",
    CMR_Index_Categories.single_ep : "cmr-singles",
    CMR_Index_Categories.album :     "cmr-albums",
    CMR_Index_Categories.live :      "cmr-live",
    CMR_Index_Categories.undefined : "cmr-unclassified"    
    }


class CMR_Index_Status(IntEnum):
    from_html_index = 0 #"Derived from existing HTML index"
    from_code = 1       #"Guessed using code"
    from_enduser = 2    #"Set or confirmed by enduser"
    undefined = 3       #"Undefined"

INDEX_CATEGORY_STRINGS = ["Extras", "Singles and EPs", "Album reviews",
                          "Live Reviews", "Undefined"]

max_index_text_length = 100

class Article(models.Model):
    title = models.CharField(max_length=200, default="")
    # e.g. "ABC, Parker’s Piece, Cambridge, 7 July\xa02017"

    url = models.CharField(max_length=400, default="")
    # e.g. "https://cambridgemusicreviews.net/2017/07/09/abc-cam-7-july-2017/"

    index_text = models.CharField(max_length=max_index_text_length, default="")
    # e.g. "ABC"

    category = models.IntegerField(default=CMR_Index_Categories.extra)
    # e.g. CMR_Index_Categories.live enum value

    index_status = models.IntegerField(default=0)

    tags = []

    def print_article_details(self):
        print("title      is :\""+self.title+"\"")
        print("url        is :\""+self.url+"\"")
        print("index_text is :\""+self.index_text+"\"")
        print("category   is :\""+INDEX_CATEGORY_STRINGS[self.category]+"\"")

    def __str__(self):
        result = "title      is :\""+self.title+"\"\n"+\
            "url        is :\""+self.url+"\"\n"+\
            "index_text is :\""+self.index_text+"\"\n"+\
            "category   is :\""+INDEX_CATEGORY_STRINGS[self.category]+"\"\n"
        return result

class Tag(models.Model):
    article = models.ForeignKey(Article)
    text = models.CharField(max_length=200, default="") # e.g. "live"

    def __str__(self):
        return self.text
