#!/usr/bin/env python3

from cmr.cmr_utilities import CMR_Index_Categories

def confirm_is_single_interactive(article):
    response = input("guessed "+article.title+" is a single/ep review ; ok? (y/n):")
    return response.lower() == 'y';

def confirm_is_album_interactive(article):
    response = input("guessed "+article.title+" is an album review; ok? (y/n):")
    return response.lower() == 'y';

def confirm_is_live_interactive(article):
    response = input("guessed "+article.title+" is a live review; ok? (y/n):")
    return response.lower() == 'y';

def get_missing_index_text_interactive(article):
    # TODO : ask the user to input some text and use their response
    print("missing index text")

    print("current article is\n")
    article.print_article_details()
    response = input("please type in text to use for index link: ")
    return response

#    proposed_data = CMR_Article()
#    proposed_data.title = article.title
#    proposed_data.url = article.url
#    proposed_data.index_text = response
#    proposed_data.category = article.category
#
#    print("proposed article : ")
#    proposed_data.print_article_details()
#    ok = input("use this new data? (y/n): ")
#    if ok=='y':
#        return response
#    else:
#        return ""

def _guess_index_text(article):
    phrases = article.title.split(',')

    if article.category == CMR_Index_Categories.live:
        date = phrases[len(phrases)-1]
        # print(date)
        date_parts = str(date).split(" ");
        #  print(date_parts)

        number_part = date_parts[1]
        # print(number_part)

        month_part = date_parts[2]
                
        year_part = ""
        if len(date_parts) > 3:
            year_part = date_parts[3]

        date_appendage = ""
        if number_part=='11':
            date_appendage = "th"
        elif number_part[len(number_part)-1]=='1':
            date_appendage = "st"
        elif number_part=='12':
            date_appendage = "th"
        elif number_part[len(number_part)-1]=='2':
            date_appendage = "nd"
        elif number_part=='13':
            date_appendage = "th"
        elif number_part[len(number_part)-1]=='3':
            date_appendage = "rd"
        else :
            date_appendage = "th"

        result = phrases[0]+", "+number_part + date_appendage +\
                               " "+month_part
        if len(date_parts) > 3:
            result += " "+year_part
        return result
    
    elif article.category == CMR_Index_Categories.album or \
         article.category == CMR_Index_Categories.single_ep:
        return phrases[0]

def get_missing_category_interactive(article):
    # TODO : ask the user to input a category and use their response
    print("missing category")
    print("article title is \""+ article.title+"\"")
    print("article url is \""+ article.url+"\"")
    print("Possible categories are ")
    print("  Extras          (e)")
    print("  Singles and EPs (s)")
    print("  Album reviews   (a)")
    print("  Live Reviews    (l)")
    response = input("please type in a category (e/s/a/l): ")
    cat = CMR_Index_Categories.undefined
    if response == 'e' :
        cat = CMR_Index_Categories.extra
    elif response == 's' :
        cat = CMR_Index_Categories.single_ep
    elif response == 'a' :
        cat = CMR_Index_Categories.album
    elif response == 'l' :
        cat = CMR_Index_Categories.live
    return cat

#    proposed_data = CMR_Article()
#    proposed_data.title = article.title
#    proposed_data.url = article.url
#    proposed_data.index_text = article.index_text
#    proposed_data.category = cat
#
#    print("proposed article : ")
#    proposed_data.print_article_details()
#    ok = input("use this new data? (y/n): ")
#    if ok=='y':
#        return cat
#    else:
#        return ""

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
    venues = ["Junction", "Portland Arms", "Parker’s Piece",
              "Corner House", "Rescue Rooms", "Corn Exchange",
              "Home Festival, Mundford", "Cambridge Folk Festival",
              "Thetford Forest", "Blue Moon", "Roundhouse"]
    for venue in venues:
        if _string_in_title(venue, article):
            return True

    return False

def fill_in_missing_data_interactive(articles):
    problem_titles = []
    return fill_in_missing_data(articles,
                     get_missing_index_text_interactive,
                     get_missing_category_interactive,
                     confirm_is_single_interactive,
                     confirm_is_album_interactive,
                     confirm_is_live_interactive,
                     False, #quiet
                     problem_titles)

def fill_in_missing_data_quiet(articles, problem_titles):
    return fill_in_missing_data(articles,
                     get_missing_index_text_interactive,
                     get_missing_category_interactive,
                     lambda x:True, # confirmation that a guess is OK
                     lambda x:True, # confirmation that a guess is OK
                     lambda x:True, # confirmation that a guess is OK
                     True, # quiet
                     problem_titles)
    
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
def fill_in_missing_data(articles,
                         get_missing_index_text,
                         get_missing_category,
                         confirm_is_single,
                         confirm_is_album,
                         confirm_is_live,
                         quiet,
                         problem_articles):
    
    got_all_data_ok = True
    for article in articles:
        has_category = _article_has_category(article)
        has_index_text = _article_has_index_text(article)
        if has_category and has_index_text:
            continue
        
        if _known_single_in_title(article):
            if confirm_is_single(article):
                article.category = CMR_Index_Categories.single_ep
                article.index_text = _guess_index_text(article)
                continue

        if _known_album_in_title(article):
            if confirm_is_album(article):
                article.category = CMR_Index_Categories.album
                article.index_text = _guess_index_text(article)
                continue

        if _known_venue_in_title(article):
            if confirm_is_live(article):
                article.category = CMR_Index_Categories.live
                article.index_text = _guess_index_text(article)
                continue

        guess_category = guess_category_from_tags(article)
        if guess_category != CMR_Index_Categories.undefined:
            article.category = guess_category
            article.index_text = _guess_index_text(article)
            continue;

        if quiet:
            problem_articles.append(article)
            got_all_data_ok = False
        
        if not has_category:
            article.category = get_missing_category(article, quiet)

        if not has_index_text:
            article.index_text = get_missing_index_text(article, quiet)
        
    return got_all_data_ok

