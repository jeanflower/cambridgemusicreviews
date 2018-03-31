from django import forms
from indexer.models import max_index_text_length, \
                           INDEX_CATEGORY_STRINGS

CATEGORY_CHOICES = (('1', INDEX_CATEGORY_STRINGS[0]), \
                    ('2', INDEX_CATEGORY_STRINGS[1]), \
                    ('3', INDEX_CATEGORY_STRINGS[2]), \
                    ('4', INDEX_CATEGORY_STRINGS[3]), \
                    ('5', INDEX_CATEGORY_STRINGS[4]))

SEARCH_LOCATION_CHOICES = (('1', "Title"), \
                           ('2', "Tags"),
                           ('3', "Index text"))

class EditEntryForm(forms.Form):
    index_text = forms.CharField(label="Index link text",
                                 max_length=max_index_text_length,
                                )
    category_choice = forms.ChoiceField(label = '',
                                        widget=forms.RadioSelect,
                                        choices=CATEGORY_CHOICES)
class SearchForm(forms.Form):
    search_term = forms.CharField(label="Search for text",
                                  max_length=max_index_text_length,
                                 )
    location_choice = forms.MultipleChoiceField(
                                        label = "Search in...",
                                        choices=SEARCH_LOCATION_CHOICES)
