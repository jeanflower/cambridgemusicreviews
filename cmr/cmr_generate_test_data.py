#!/usr/bin/env python3

from cmr.cmr_utilities import save_cmr_page

# today, after the 21st page, we get an error
max_page_number = 200

def generate_test_data():
    # this will generate a set of files called page_text_1.html etc
    # after loading the data from the CMR wordpress site
    for page_number in range(1, max_page_number):
        destination_filename = "page_text_"+str(page_number)+".html"
        if not save_cmr_page(page_number, destination_filename):
            print("failed to obtain page")
            break
        print("saved as "+destination_filename)

