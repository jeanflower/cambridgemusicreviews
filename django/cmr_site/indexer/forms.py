from django import forms
from indexer.models import max_index_text_length

import sys
sys.path.append('../..')
#sys.path.append("/home/jeanflower/cambridgemusicreviews/cambridgemusicreviews")

from importlib import import_module
import_module("cmr.cmr_utilities")

from cmr.cmr_utilities import INDEX_CATEGORY_STRINGS

CHOICES = (('1', INDEX_CATEGORY_STRINGS[0]), \
           ('2', INDEX_CATEGORY_STRINGS[1]), \
           ('3', INDEX_CATEGORY_STRINGS[2]), \
           ('4', INDEX_CATEGORY_STRINGS[3]), \
           ('5', INDEX_CATEGORY_STRINGS[4]))

class IndexTextForm(forms.Form):
    index_text = forms.CharField(label="index text",
                                 max_length=max_index_text_length,
                                )
    category_choice = forms.MultipleChoiceField(choices=CHOICES)
