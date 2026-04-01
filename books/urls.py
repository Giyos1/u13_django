from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.book_list, name='book_list'),
    path('detail/<int:pk>/', views.book_detail, name='book_detail'),
]
