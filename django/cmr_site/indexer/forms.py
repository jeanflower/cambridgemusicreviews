from django import forms
from indexer.models import max_index_text_length

import sys
sys.path.append('../..')

from importlib import import_module
import_module("cmr.cmr_utilities")

from cmr.cmr_utilities import index_category_strings

CHOICES = (('1', index_category_strings[0]), 
           ('2', index_category_strings[1]), 
           ('3', index_category_strings[2]), 
           ('4', index_category_strings[3]), 
           ('5', index_category_strings[4]))

class IndexTextForm(forms.Form):
    index_text = forms.CharField(label = "index text", 
                                 max_length = max_index_text_length,
                                 )
    category_choice = forms.MultipleChoiceField(choices=CHOICES)
    
    
    