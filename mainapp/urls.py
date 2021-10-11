from django.urls import path

from .views import *

app_name = 'mainapp'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('customer_list', CustomerListView.as_view(), name='customer-list'),

    path('order_list', OrderListView.as_view(), name='order-list'),

    path('product_list', ProductListView.as_view(), name='product-list'),
]
