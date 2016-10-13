from django import forms
from django.contrib.auth.models import User
from bailout.models import Bailout, UserProfile, Rating


class MemberSearchForm(forms.ModelForm):
    class Meta:
        model = Bailout
        fields = ['name', ]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('zip_code', 'picture')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['moc', 'rating', ]



