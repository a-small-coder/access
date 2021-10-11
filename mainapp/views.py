from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import *


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


# Customer


class CustomerListView(generic.ListView):
    template_name = 'customer/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.all()


class CustomerDetailView(generic.DetailView):
    template_name = 'customer/customer_detail.html'
    context_object_name = 'customer'
    queryset = Customer.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        print(self.queryset.first().orders)
        context.update({
            "orders": Order.objects.filter(customer=self.queryset.first())
        })
        return context


class CustomerCreateView(generic.CreateView):
    pass


class CustomerUpdateView(generic.UpdateView):
    pass


class CustomerDeleteView(generic.DeleteView):
    pass


# Order


class OrderListView(generic.ListView):
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()


class OrderDetailView(generic.DetailView):
    pass    # скорее всего не нужен


class OrderCreateView(generic.CreateView):
    pass    # должен быть доступен на странице конкретного покупателя


class OrderUpdateView(generic.UpdateView):
    pass    # хз, как реализовать   мб, не стоит делать


class OrderDeleteView(generic.DeleteView):
    pass    # на странице списка заказов и конкретного покупателя


# Product


class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(generic.DetailView):
    pass    # скорее всего не нужен


class ProductCreateView(generic.CreateView):
    pass


class ProductUpdateView(generic.UpdateView):
    pass


class ProductDeleteView(generic.DeleteView):
    pass
