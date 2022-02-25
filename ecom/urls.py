from django.urls import path

from . import views
from .views import Index

urlpatterns = [
    path('index', views.Index.as_view(), name='index'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product/<int:id>', views.product_page, name='product_page')
]