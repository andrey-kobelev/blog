from django import forms


NAME_MAX_LENGTH = 25


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=NAME_MAX_LENGTH)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
