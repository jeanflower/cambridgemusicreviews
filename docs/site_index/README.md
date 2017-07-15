The site index for the review site is managed using a Wordpress widget which contains html.
The index has a link for each article in the site, and the articles are categorised as "Album Reviews", "Live Reviews", etc.

One purpose of this repo is to host scripts which can be used to convert the text of the main Wordpress site into appropriate html text to use for the index panel.

Here's an sample of the HTML in the index widget:
```
<h2>Singles and EPs</h2>
<br><a href="https://cambridgemusicreviews.net/2017/03/25/ricky-boom-boom-ep-released-march-2017/">Ricky Boom-Boom</a>
```

and here's some of the source of the main site:
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

