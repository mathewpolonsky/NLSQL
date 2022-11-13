from django import forms

class TextForm(forms.Form):
    text_for_translation = forms.CharField(max_length=100)
    data_base_csv = forms.FileField()