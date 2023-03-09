from django.urls import path

from webapp.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    # path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('product/<int:pk>', product_detail, name='product_detail'),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    path('stripe_webhook', stripe_webhook, name='stripe_webhook'),

    path('signup', user_signup, name='signup'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
]
