from django import forms

from .models import Order


class CashOrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'needed_product', 'needed_quantity', 'needed_cost',
        ]


class CashlessOrderModelForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = [
            'needed_product', 'needed_quantity', 'needed_cost',
        ]


class BarterOrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'needed_product', 'needed_quantity', 'needed_cost',
            'given_product', 'given_quantity', 'given_cost',
        ]


class SellOrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'given_product', 'given_quantity', 'given_cost',
        ]


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = [
            'customer', 'completed'
        ]
