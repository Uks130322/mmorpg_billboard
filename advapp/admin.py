from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Advert, Respond, Category
# Register your models here.


class AdvertAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Advert, AdvertAdmin)
admin.site.register(Respond)
admin.site.register(Category)

