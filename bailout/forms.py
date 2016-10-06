from django import forms

from bailout.models import Bailout


class MemberSearchForm(forms.ModelForm):
    class Meta:
        model = Bailout
        fields = ['name', ]