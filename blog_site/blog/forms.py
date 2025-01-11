from django import forms

from .models import Comment

NAME_MAX_LENGTH = 25


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=NAME_MAX_LENGTH)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
