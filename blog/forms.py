from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
    widget=forms.Textarea)



"""
Creating forms from models for Comment class
"""

from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
