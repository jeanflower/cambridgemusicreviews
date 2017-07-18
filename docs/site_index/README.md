The site index for the review site is managed using a Wordpress widget which contains html.
The index has a link for each article in the site, and the articles are categorised as "Album Reviews", "Live Reviews", etc.

One purpose of this repo is to host scripts which can be used to convert the text of the main Wordpress site into appropriate html text to use for the index panel.

# Workflow
Have a script which can
1. Get the HTML on the current page from the WordPress site
    1. To make our coding insensitive to WordPress changes, we have captured html in the tests folder of this repo.
    2. WordPress reveals more as the read scrolls down - the script will probably query for multiple pages.
2. Optionally allow the user to update the index
    1. Find out which page articles are not represented in the current index.
    2. Notify the user of each unindexed article in turn (display title).
    3. Get help from the script user (which category?, what index link text?)
    4. Compose new index HTML for new index entry.
    5. Make a complete index including both old and new index entries.
    6. Save the new index html to a file.
3. Optionally allow the user to edit the index
    1. Let the uer query for existing index entries.
    2. Display the text / url for that entry and let the user provide edits for that data.
    3. Compose an updated complete index with the new data.
    4. Save the new index html to a file.

# Scripting
Determine a suitable data structure for the article/index entry pair.  For example:
`{ article_title, url, index_text, index_category }`
1. GENERATE_INDEX: Given a data structure which represents the page entries, build HTML for the index.  The HTML will be suitably categorised and sorted.
2. READ_ENTRIES: Given page entries, build a data structure for entries.
3. READ_INDEX: Given an existing index, build a data structure for the already indexed entries.
4. EXTEND_INDEX: Given data structures from 3 and 4 above, compare them to find gaps. Have some user-interaction to help fill out the information we need, then add index entries (in the right place) to make a complete index.


# HTML examples
Here's an sample of the HTML in the index widget:
(see view-source:https://cambridgemusicreviews.net/page/2/)
```
<h2>Singles and EPs</h2>
<br><a href="https://cambridgemusicreviews.net/2017/03/25/ricky-boom-boom-ep-released-march-2017/">Ricky Boom-Boom</a>
```

and here's some of the source of the main site:
(see view-source:https://cambridgemusicreviews.net/page/2/)
````
<article id="post-1952" class="post-1952 post type-post status-publish format-standard hentry category-music tag-a-rum-old-do tag-cambridge tag-ep tag-review tag-ricky-boom-boom tag-tom-colborn">
<header class="entry-header">
			
<h1 class="entry-title">
<a href="https://cambridgemusicreviews.net/2017/03/25/ricky-boom-boom-ep-released-march-2017/" rel="bookmark">Ricky Boom-Boom, EP released March&nbsp;2017</a>
</h1>
<div class="comments-link">
<a href="https://cambridgemusicreviews.net/2017/03/25/ricky-boom-boom-ep-released-march-2017/#respond"><span class="leave-reply">Leave a reply</span></a>			
</div><!-- .comments-link -->
</header><!-- .entry-header -->

<div class="entry-content">
<p>This EP is called &#8216;A Rum Old Do&#8217; and is a refreshing dose of folky blues from <strong>Ricky Boom-Boom</strong>, a Cambridge guitarist named after the enduring song by the late great John Lee Hooker.</p>
````

