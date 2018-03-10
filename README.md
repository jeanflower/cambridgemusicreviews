# cambridgemusicreviews

## Synopsis
A place to develop scripts associated with https://cambridgemusicreviews.net
![web_page_screengrab](docs/cmr_web_page_image.png)

## Motivation
The main contributor to the cambridgemusicreviews site wants to maintain it with minimal technical intervention.  Anything we can do to script maintainance of the site will be welcomed. The following video show some manual work maintaining the site index which we would like to make less manual.
![manual index maintenance](docs/editing_cmr_site_index.mp4)

### Examples:
```python manage.py shell```  
```exec(open("capture_cmr_pages.py").read())```  
generates a set of files called page_text_1.html, page_text_2.html,... a local archive of the current state of the CMR site.

```python manage.py shell```  
```exec(open("make_index_html.py").read())```  
generates a file called test_output_all_sorted.html which guesses categories for new articles and highlights them for review.

From django/cmr_site  
```python manage.py runserver```  
runs a web sever which responds to http://127.0.0.1:8000/indexer/

## Development

### Understanding the scripts
The scripts should have documentation in the comments, but also there is sample code in files example_*.py here
https://github.com/jeanflower/cambridgemusicreviews/tree/master/django/cmr_site  
which illustrate how we might use some functions. 

To run all example code (and check it all still compiles!)  
```python manage.py shell```  
```exec(open("run_examples.py").read())```

### Tests and quality
There are python unit tests in the tests folder.  These should always pass.
To run the unit tests:  
```python manage.py test```

To generate coverage data:  
```coverage run -m unittest discover tests/```  

This repo is under codacy review
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a59e0815f2a74514bcd1e1273f525705)](https://www.codacy.com/app/jeanflower/cambridgemusicreviews?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jeanflower/cambridgemusicreviews&amp;utm_campaign=Badge_Grade)
To update codacy coverage data,  
```coverage xml```  
```python-codacy-coverage -r coverage.xml```

## Contributors
Initially set up by Jean Flower.
