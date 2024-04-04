from django.urls import path, include
from .views import AdvertList, AdvertDetail, AdvertCategoryList

urlpatterns = [
    path('home/', AdvertList.as_view(), name='advert_list'),
    path('advert/<int:pk>', AdvertDetail.as_view(), name='advert'),
    path('categories/<int:pk>', AdvertCategoryList.as_view(), name='advert_cat_list'),
]
