from django import forms

class ReplaceWordsForm(forms.Form):
    num_words_to_replace = forms.IntegerField(initial=3, widget=forms.HiddenInput())
