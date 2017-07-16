from cmr_utilities import get_cmr_url, save_html

# today, after the 21st page, we get an error
max_page_number = 40

# this will generate a set of files called page_text_1.html etc
# after loading the data from the CMR wordpress site
for page_number in range(1, max_page_number):
    url = get_cmr_url(page_number)
    save_html(url, "../tests/page_text_"+str(page_number)+".html")

