from django import forms

from advapp.models import Advert, Respond


class AdvertForm(forms.ModelForm):
    title = forms.CharField(
        min_length=10,
        widget=forms.Textarea({'cols': 70, 'rows': 3})
    )
    content = forms.CharField(
        min_length=20,
        widget=forms.Textarea({'cols': 70, 'rows': 20})
    )

    class Meta:
        model = Advert
        fields = [
            'icon',
            'title',
            'category',
            'content',
        ]


class RespondForm(forms.ModelForm):
    content = forms.CharField(
        min_length=10,
        widget=forms.Textarea({'cols': 70, 'rows': 3})
    )

    class Meta:
        model = Respond
        fields = ['content']
