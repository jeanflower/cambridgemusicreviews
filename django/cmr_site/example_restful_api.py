#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 18:46:51 2017

@author: jeanflower
"""
import requests

# see https://developer.wordpress.com/docs/api/1.1/get/sites/%24site/posts/

# specify where to get the data from
url = "https://public-api.wordpress.com/rest/v1.1/sites/cambridgemusicreviews.net/posts"
# ask for 17 results only
url+= "?number=17"
# influences the formatting of the results
url+= "&context=\"display\""

ret = requests.get(url)
returned_code = ret.status_code
print("returned value is "+str(ret.status_code))
if returned_code == 200:
    all_posts = ret.json()["posts"]

    for post in all_posts:
        print(post["title"])

else:
    print("not a 200 response")


