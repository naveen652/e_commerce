from django.urls import path
from . import views

app_name = 'myapp'  # Optional, but useful if you have multiple apps

urlpatterns = [
    path('enter_mobile/', views.enter_mobile, name='enter_mobile'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('categories/', views.list_categories, name='list_categories'),
    path('products/', views.list_products, name='list_products'),
    path('category/<int:categoryId>/', views.list_products_by_category, name='list_products_by_category'),
    path('place_order/', views.place_order, name='place_order'),
    path('update_profile/',views.update_profile, name='update_profile'),
]