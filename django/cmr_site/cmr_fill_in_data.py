#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from indexer.models import CMR_Index_Categories, CMR_Index_Status

def _append_th_to_number(num):
    if num.endswith("th") or\
      num.endswith("st") or\
      num.endswith("rd") or\
      num.endswith("nd"):
      num = num[:-2]
    else:
      stub = num
    date_appendage = ""
    if num == '11':
        date_appendage = "th"
    elif num[len(num)-1] == '1':
        date_appendage = "st"
    elif num == '12':
        date_appendage = "th"
    elif num[len(num)-1] == '2':
        date_appendage = "nd"
    elif num == '13':
        date_appendage = "th"
    elif num[len(num)-1] == '3':
        date_appendage = "rd"
    else:
        date_appendage = "th"
    return num + date_appendage


def _guess_index_text(article):
    print(article.title)
    phrases = article.title.split(',')

    if article.category == CMR_Index_Categories.live:
        date = phrases[len(phrases)-1]
        number_part = ""
        month_part = ""
        year_part = ""
        if article.title == "Elma, Portland Arms, Cambridge, 27 September, 2018":
          number_part = "27"
          month_part = "September"
          year_part = "2018"
        else:
          # print(date)
          date_parts = str(date).split(" ")
          print(date_parts)
          number_part = date_parts[1]
          # print(number_part)
          month_part = date_parts[2]
          year_part = ""
          if len(date_parts) > 3:
              year_part = date_parts[3]

        result = phrases[0]+", "+_append_th_to_number(number_part ) +\
                               " "+month_part
        if len(year_part) > 0:
            result += " "+year_part
        return result

    elif article.category == CMR_Index_Categories.album or \
         article.category == CMR_Index_Categories.single_ep:
        return phrases[0]

    else:
        return article.title

def _string_in_title(s, article):
    if s in article.title:
        return True
    #print(s+" is not in "+article.title)
    return False

def _known_single_in_title(article):

    # print("check whether we recognise an single here")
    # print(article.title)

    singles = ["Of The Night"]
    for single in singles:
        if _string_in_title(single, article):
            return True

    return False

def _known_album_in_title(article):

    # print("check whether we recognise an album here")
    # print(article.title)

    albums = ["A Simple Guide To Small And Medium Pond Life",
              "The Race For Space",
              "Wave Pictures, released February",
              "Shadows In The Night",
              "Album Review",
              "This Is The Sound Of Sugar Town"]
    for album in albums:
        if _string_in_title(album, article):
            return True

    return False

def _known_venue_in_title(article):
    venues = ["Junction", "Portland Arms", "Parker's Piece",
              "Corner House", "Rescue Rooms", "Corn Exchange",
              "Home Festival, Mundford", "Cambridge Folk Festival",
              "Thetford Forest", "Blue Moon", "Roundhouse"]
    for venue in venues:
        if _string_in_title(venue, article):
            return True

    return False

def _article_has_category(article):
    return article.category != CMR_Index_Categories.undefined

def _article_has_index_text(article):
    return len(article.index_text) > 0

def guess_category_from_tags(article):
    could_be_live = "live" in article.tags
    could_be_album = "LP" in article.tags
    could_be_single_ep = "single" in article.tags or "EP" in article.tags

    if could_be_live and not could_be_album and not could_be_single_ep:
        return CMR_Index_Categories.live
    elif not could_be_live and could_be_album and not could_be_single_ep:
        return CMR_Index_Categories.album
    elif not could_be_live and not could_be_album and could_be_single_ep:
        return CMR_Index_Categories.single_ep
    else:
        return CMR_Index_Categories.undefined


# Find out whether articles have missing index_text or category
# and ask the user to provide the information.
# Store result back in articles
def fill_in_missing_data(articles):

    got_all_data_ok = True
    for article in articles:
        has_category = _article_has_category(article)
        has_index_text = _article_has_index_text(article)
        if has_category and has_index_text:
            continue

        if _known_single_in_title(article):
            article.category = CMR_Index_Categories.single_ep
            article.index_text = _guess_index_text(article)
            article.index_status = CMR_Index_Status.from_code
            continue

        if _known_album_in_title(article):
            article.category = CMR_Index_Categories.album
            article.index_text = _guess_index_text(article)
            article.index_status = CMR_Index_Status.from_code
            continue

        if _known_venue_in_title(article):
            article.category = CMR_Index_Categories.live
            article.index_text = _guess_index_text(article)
            article.index_status = CMR_Index_Status.from_code
            continue

        guess_category = guess_category_from_tags(article)
        if guess_category != CMR_Index_Categories.undefined:
            article.category = guess_category
            article.index_text = _guess_index_text(article)
            article.index_status = CMR_Index_Status.from_code
            continue

#        print(str(article))

        article.category = CMR_Index_Categories.extra
        article.index_text = _guess_index_text(article)
        article.index_status = CMR_Index_Status.from_code
        continue

    return got_all_data_ok
