from django.contrib import admin
from django.urls import path, include
from .views import Test, get_text

urlpatterns = [
    path('translation/', get_text, name="translation"),
    path('', Test.as_view())
]