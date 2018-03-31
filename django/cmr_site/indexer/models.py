from django.db import models

from enum import IntEnum

# An article can fall into one of these categories.
class CMR_Index_Categories(IntEnum): # pylint :disable=W0631
    live = 0      #"Live Reviews"
    album = 1     #"Album reviews"
    single_ep = 2 #"Singles and EPs"
    extra = 3     #"Extras"
    undefined = 4 #"Undefined"

categories = [CMR_Index_Categories.live,
              CMR_Index_Categories.album,
              CMR_Index_Categories.single_ep,
              CMR_Index_Categories.extra,
              CMR_Index_Categories.undefined]

# for tags in HTML output
html_tags = {
    CMR_Index_Categories.live :      "cmr-live",
    CMR_Index_Categories.album :     "cmr-albums",
    CMR_Index_Categories.single_ep : "cmr-singles",
    CMR_Index_Categories.extra :     "cmr-extras",
    CMR_Index_Categories.undefined : "cmr-unclassified"    
    }

# for keys in django output
django_keys = {
    CMR_Index_Categories.live :      "cmrlive",
    CMR_Index_Categories.album :     "cmralbums",
    CMR_Index_Categories.single_ep : "cmrsingles",
    CMR_Index_Categories.extra :     "cmrextras",
    CMR_Index_Categories.undefined : "cmrunclassified"    
    }

# for keys in django output
django_headings = {
    CMR_Index_Categories.live :      "django_heading_live",
    CMR_Index_Categories.album :     "django_heading_album",
    CMR_Index_Categories.single_ep : "django_heading_single",
    CMR_Index_Categories.extra :     "django_heading_extra",
    CMR_Index_Categories.undefined : "django_heading_unclassified"    
    }

# for keys in django output
django_show_categories = {
    CMR_Index_Categories.live :      "article_list_live",
    CMR_Index_Categories.album :     "article_list_albums",
    CMR_Index_Categories.single_ep : "article_list_singles",
    CMR_Index_Categories.extra :     "article_list_extras",
    CMR_Index_Categories.undefined : "article_list_unclassified"    
    }

# for headings in HTML output
category_strings = {
    CMR_Index_Categories.live :      "Live Reviews",
    CMR_Index_Categories.album :     "Album reviews",
    CMR_Index_Categories.single_ep : "Singles and EPs",
    CMR_Index_Categories.extra :     "Extras",
    CMR_Index_Categories.undefined : "Undefined"
    }

# for forms.py
INDEX_CATEGORY_STRINGS = [
    category_strings[categories[0]],
    category_strings[categories[1]],
    category_strings[categories[2]],
    category_strings[categories[3]],
    category_strings[categories[4]]    
    ]

class CMR_Index_Status(IntEnum):
    from_html_index = 0 #"Derived from existing HTML index"
    from_code = 1       #"Guessed using code"
    from_enduser = 2    #"Set or confirmed by enduser"
    undefined = 3       #"Undefined"

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
        print("category   is :\""+category_strings[self.category]+"\"")

    def __str__(self):
        result = "title      is :\""+self.title+"\"\n"+\
            "url        is :\""+self.url+"\"\n"+\
            "index_text is :\""+self.index_text+"\"\n"+\
            "category   is :\""+category_strings[self.category]+"\"\n"
        return result

class Tag(models.Model):
    article = models.ForeignKey(Article)
    text = models.CharField(max_length=200, default="") # e.g. "live"

    def __str__(self):
        return self.text
