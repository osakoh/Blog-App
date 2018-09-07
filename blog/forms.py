from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


# # Building the form from the model
class CommentForm(forms.ModelForm):
    class Meta:
        # first indicate the model to be used
        model = Comment
        fields = ('name', 'email', 'body')


# for the custom view to allow users search post
class SearchForm(forms.Form):
    query = forms.CharField()



# Django comes with two base classes to build forms:

# 1. Form: Allows you to build standard forms
# 2. ModelForm: Allows you to build forms tied to model instances