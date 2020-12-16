from .models import Comment
from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    # email = forms.EmailField()
    to = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):  # ModelForm: Allows you to build forms tied to model(Comment) instances
    class Meta:
        model = Comment  # selects model to build form
        fields = ('name', 'email', 'body')  # selects fields from the Comment model to be used in the form
