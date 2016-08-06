from django import forms
from django.contrib.auth.models import User
from ssapp.models import UserProfile, BidDetails


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

        fields = ('userimage','address', 'contact')


class BidDetailsForm(forms.ModelForm):
    class Meta:
        model = BidDetails
       # widgets = {'userinfo': forms.HiddenInput(),'bid': forms.HiddenInput()}
        fields = ['userbid']