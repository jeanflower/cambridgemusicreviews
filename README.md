# cambridgemusicreviews

## Synopsis
A place to develop scripts associated with https://cambridgemusicreviews.net
![web_page_screengrab](docs/cmr_web_page_image.png)

## Motivation
The main contributor to the cambridgemusicreviews site wants to maintain it with minimal technical intervention.  Anything we can do to script maintainance of the site will be welcomed. The following video show some manual work maintaining the site index which we would like to make less manual.
![manual index maintenance](docs/editing_cmr_site_index.mp4)

### Example:
```python make_index_html.py``` 
generates a file called test.html which can be used to update the html for the index widget in the page.

## Understanding the scripts
The scripts should have documentation in the comments, but also there is sample code in .  
https://github.com/jeanflower/cambridgemusicreviews/tree/master/cmr/examples  
to illustrate how we might use some functions. 
## Tests
There are python unit tests in the tests folder.  These should always pass.
### To run the unit tests:
```python -m unittest discover tests```

## Contributors
Initially set up by Jean Flower.


