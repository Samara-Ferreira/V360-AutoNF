from django.contrib import admin
from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('data-entries/', views.DataEntryView.as_view(), name='data-entries-list-create'),
]
