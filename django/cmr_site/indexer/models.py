from django.db import models

import sys
sys.path.append('../..')

from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Article(models.Model):
    title = models.CharField( max_length = 200, default = "" )      # e.g. "ABC, Parker’s Piece, Cambridge, 7 July\xa02017"
    url = models.CharField( max_length = 400, default = "" )        # e.g. "https://cambridgemusicreviews.net/2017/07/09/abc-parkers-piece-cambridge-7-july-2017/"
    index_text = models.CharField( max_length = 200, default = "" ) # e.g. "ABC"
    category = models.IntegerField( default = 0 )     # e.g. CMR_Index_Categories.live
    index_status = models.IntegerField( default = 0 )

    def __str__(self):
        result ="title      is :\""+self.title+"\"\n"+\
            "url        is :\""+self.url+"\"\n"+\
            "index_text is :\""+self.index_text+"\"\n"+\
            "category   is :\""+str(self.category)+"\"\n";
        return result
    