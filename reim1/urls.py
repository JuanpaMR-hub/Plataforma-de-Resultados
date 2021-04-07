from django.urls import path
from .views import reim1_view

urlpatterns = [
    path('',reim1_view)
]