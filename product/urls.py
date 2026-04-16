from django.urls import path

from product import views

urlpatterns = [
    path('',views.product_list,name='product_list'),
    path('create/',views.product_create,name='product_create'),
    path('create_save/',views.product_create_save,name='product_create_save'),
    path('update_form/<int:pk>/',views.product_update_form,name='product_update_form'),
    path('update/<int:pk>/',views.product_update,name='product_update'),
]