from django.shortcuts import render, HttpResponse
from django.views import generic
from django.urls import reverse_lazy

from .models import *
from .forms import *


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
        context.update({
            "orders": reversed(Order.objects.filter(customer=self.queryset.first()))
        })
        return context


# Order


class OrderListView(generic.ListView):
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return reversed(Order.objects.all())


class OrderCreateView(generic.CreateView):
    template_name = 'customer/customer_order_create.html'
    queryset = Customer.objects.all()
    context_object_name = 'customer'
    success_url = reverse_lazy('mainapp:order-list')
    form_class = OrderModelForm
    print(queryset)

    # def get_form_class(self):
    #     # request_path = self.request.path
    #     # print(request_path)
    #     # if request_path == reverse_lazy('mainapp:cash-order-create', kwargs={'pk': self.queryset.first().pk}):
    #     #     return CashOrderModelForm
    #     # elif request_path == reverse_lazy('mainapp:cashless-order-create', kwargs={'pk': self.queryset.first().pk}):
    #     #     return CashlessOrderModelForm
    #     # elif request_path == reverse_lazy('mainapp:barter-order-create', kwargs={'pk': self.queryset.first().pk}):
    #     #     return BarterOrderModelForm
    #     # else:
    #     #     return SellOrderModelForm
    #     return OrderForm

    def form_valid(self, form):
        order = form.save(commit=False)
        order.customer = self.queryset.first()
        return HttpResponse('Oh, hi, Mark!')


# Product


class ProductListView(generic.ListView):
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()
