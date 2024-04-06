from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


class Advert(models.Model):
    title = models.CharField(max_length=511, verbose_name="advert's title")
    content = models.TextField(verbose_name='content')  # here will be WYSIWYG
    icon = models.ImageField(default='blanc.png', verbose_name='icon for preview')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='category')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')

    def get_absolute_url(self):
        return reverse('advert', args=[str(self.id)])

    def __str__(self):
        return self.title[:20]


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True, verbose_name='category')

    def __str__(self):
        return self.name


class Respond(models.Model):
    content = models.TextField(verbose_name='comment')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    advert_id = models.ForeignKey('Advert', on_delete=models.CASCADE, verbose_name='advert')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    accepted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('advert', args=[str(self.advert_id.id)])
