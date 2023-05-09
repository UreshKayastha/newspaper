from django import forms
from newspaper.models import Contact,NewsLetter,Comment

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields="__all__"

class NewsLetterForm(forms.ModelForm):
    class Meta:
        model=NewsLetter
        fields="__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields="__all__"

