from django.db import models

import sys
sys.path.append('../..')


class Article(models.Model):
    title = models.CharField( max_length = 200, default = "" )      # e.g. "ABC, Parker’s Piece, Cambridge, 7 July\xa02017"
    url = models.CharField( max_length = 400, default = "" )        # e.g. "https://cambridgemusicreviews.net/2017/07/09/abc-parkers-piece-cambridge-7-july-2017/"
    index_text = models.CharField( max_length = 200, default = "" ) # e.g. "ABC"
    category = models.IntegerField( default = 0 )     # e.g. CMR_Index_Categories.live enum value
    index_status = models.IntegerField( default = 0 )

    def __str__(self):
        result ="title      is :\""+self.title+"\"\n"+\
            "url        is :\""+self.url+"\"\n"+\
            "index_text is :\""+self.index_text+"\"\n"+\
            "category   is :\""+str(self.category)+"\"\n";
        return result
    