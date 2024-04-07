import random
from string import hexdigits

from allauth.account.forms import SignupForm
from django import forms
from django.core.mail import send_mail
from django_summernote.widgets import SummernoteWidget
from advapp.models import Advert, Respond, Code
from billboard.settings import DEFAULT_FROM_EMAIL


class AdvertForm(forms.ModelForm):
    title = forms.CharField(
        min_length=10,
        widget=forms.Textarea({'cols': 70, 'rows': 3})
    )
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Advert
        widgets = {'content': SummernoteWidget(),}
        fields = [
            'icon',
            'title',
            'category',
            'content',
        ]


class RespondForm(forms.ModelForm):
    content = forms.CharField(
        min_length=10,
        max_length=1000,
        widget=forms.Textarea({'cols': 70, 'rows': 3})
    )

    class Meta:
        model = Respond
        fields = ['content']


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = Code(user_id=user, number=''.join(random.sample(hexdigits, 5)))
        user.save()
        code.save()
        send_mail(
            subject='Код активации',
            message=f'Код для активации аккаунта: {code.number}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user
