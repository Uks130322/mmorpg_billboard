from django.urls import path

from .views import (AdvertList, AdvertDetail, AdvertCategoryList, ProfileView,
                    AdvertCreate, AdvertEdit, AdvertDelete, RespondCreate, RespondList,
                    RespondDelete, accept_respond, ConfirmUser, subscribe)

urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('home/', AdvertList.as_view(), name='advert_list'),
    path('advert/<int:pk>', AdvertDetail.as_view(), name='advert'),
    path('categories/<int:pk>', AdvertCategoryList.as_view(), name='advert_cat_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create/', AdvertCreate.as_view(), name='create'),
    path('advert/<int:pk>/edit/', AdvertEdit.as_view(), name='edit'),
    path('advert/<int:pk>/delete/', AdvertDelete.as_view(), name='delete'),
    path('advert/<int:pk>/respond/', RespondCreate.as_view(), name='respond'),
    path('my_responds/', RespondList.as_view(), name='my_responds'),
    path('my_responds/<int:pk>/delete/', RespondDelete.as_view(), name='respond_delete'),
    path('my_responds/<int:pk>/accept/', accept_respond, name='accept_respond'),
]
