from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Code(models.Model):
    number = models.CharField(max_length=15, blank=True, null=True, verbose_name='code')
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')

    def __str__(self):
        return self.number


class Advert(models.Model):
    title = models.CharField(max_length=511, verbose_name="Заголовок")
    content = models.TextField(verbose_name='Контент')  # here will be WYSIWYG
    icon = models.ImageField(upload_to='icons', default='icons/blanc.png', verbose_name='Изображение для превью')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')

    def get_absolute_url(self):
        return reverse('advert', args=[str(self.id)])

    def __str__(self):
        return self.title[:20]


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True, verbose_name='Категория')
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories', verbose_name="Подписчики")

    def __str__(self):
        return self.name


class Respond(models.Model):
    content = models.TextField(verbose_name='Отклик')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    advert_id = models.ForeignKey('Advert', on_delete=models.CASCADE, verbose_name='Объявление')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')
    accepted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('advert', args=[str(self.advert_id.id)])
