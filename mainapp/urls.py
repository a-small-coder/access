from django.urls import path

from .views import *

app_name = 'mainapp'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('customer_list', CustomerListView.as_view(), name='customer-list'),
    path('customer_detail/<int:pk>', CustomerDetailView.as_view(), name='customer-detail'),

    path('order_list', OrderListView.as_view(), name='order-list'),
    path('customer_detail/<int:pk>/order_create', OrderCreateView.as_view(), name='order-create'),
    #path('customer_detail/<int:pk>/order_confirm', )

    path('product_list', ProductListView.as_view(), name='product-list'),
]
