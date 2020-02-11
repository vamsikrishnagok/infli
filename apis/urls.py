from django.contrib import admin
from django.urls import path
from . import views

app_name = 'apis'

urlpatterns = [
    path('api/v1/login/', views.CustomAuthToken.as_view()),
    path('api/v1/logout/', views.Logout.as_view()),
    path('api/v1/groups/', views.GroupList.as_view()),
    path('api/v1/group/<int:id>', views.GroupDetail.as_view()),
    path('api/v1/photos/', views.PhotosList.as_view()),
    path('api/v1/photos/<int:id>', views.PhotosDetail.as_view()),


]
