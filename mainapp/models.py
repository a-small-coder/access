import math

from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f"{self.name} ({self.quantity} шт.)"

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Недостаточно товара на складе')
        if self.price <= 0:
            raise ValidationError('Цена товара должна быть больше нуля')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Фамилия')
    current_count = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name='Текущий счет')
    all_count = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name='Сумма покупок')
    credit_limit = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Потолок кредита')
    current_credit = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name='Текущий кредит')
    left_credit = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Остаток кредита')
    low_left_credit = models.BooleanField(default=False, editable=False, verbose_name='Низкий остаток кредита')
    comment = models.CharField(max_length=255, verbose_name='Комментарий')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.left_credit = self.credit_limit - self.current_credit
        if (self.left_credit * 10) < self.credit_limit:
            self.low_left_credit = True
        else:
            self.low_left_credit = False
        print(self.left_credit, self.credit_limit)
        print(self.low_left_credit)
        super().save(*args, **kwargs)


class Order(models.Model):
    pay_way_choices = (
        ('cash', 'Наличный расчет'),
        ('cashless', 'Безналичный расчет'),
        ('credit', 'Кредит'),
        ('barter', 'Бартер'),
        ('sell', 'Взаимозачет')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE,
                                 related_name='orders')
    pay_way = models.CharField(max_length=255, choices=pay_way_choices, verbose_name='способ оплаты')
    needed_product = models.ForeignKey(Product, verbose_name='Запрашиваемый продукт', related_name='first_product',
                                       on_delete=models.CASCADE, blank=True, null=True)
    needed_quantity = models.PositiveIntegerField(verbose_name='Количество нужного товара', blank=True, null=True)
    needed_cost = models.DecimalField(default=0, max_digits=7, decimal_places=2,
                                      verbose_name='Стоимость нужного товара', blank=True, null=True)
    given_product = models.ForeignKey(Product, verbose_name='Отдаваемый продукт', related_name='second_product',
                                      on_delete=models.CASCADE, blank=True, null=True)
    given_quantity = models.PositiveIntegerField(verbose_name='Количество отдаваемого продукта',
                                                 blank=True, null=True)
    given_cost = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Стоимость отдаваемого продукта',
                                     blank=True, null=True)
    completed = models.BooleanField(default=False, verbose_name='Создан')

    def __str__(self):
        return f"{self.id} {self.customer.name} {self.pay_way}"

    def save(self, *args, **kwargs):
        # if self.pay_way == 'cash':
        #     self.needed_product.quantity -= self.needed_quantity
        #     self.needed_cost = self.needed_product.price * self.needed_quantity
        #     self.customer.all_count += self.needed_cost
        #     self.customer.save()
        #     self.needed_product.save()
        # elif self.pay_way == 'cashless':
        #     self.needed_product.quantity -= self.needed_quantity
        #     self.needed_cost = self.needed_product.price * self.needed_quantity
        #     if self.needed_cost <= self.customer.current_count:
        #         self.customer.current_count -= self.needed_cost
        #     else:   #   если денег на счету недостаточно
        #         self.pay_way = 'credit'
        #         self.customer.credit_count += self.needed_cost
        #     self.customer.all_count += self.needed_cost
        #     self.customer.save()
        #     self.needed_product.save()
        # elif self.pay_way == 'barter':
        #     self.needed_product.quantity -= self.needed_quantity
        #     self.needed_cost = self.needed_product.price * self.needed_quantity
        #     self.given_quantity = math.ceil(self.needed_cost / self.given_product.price)
        #     self.given_product.quantity += self.given_quantity
        #     self.given_cost = self.given_product.price * self.given_quantity
        #     self.needed_product.save()
        #     self.given_product.save()
        # elif self.pay_way == 'sell':
        #     self.given_cost = self.given_product.price * self.given_quantity
        #     self.given_product.quantity += self.given_quantity
        #     self.customer.current_credit -= self.given_cost
        #     self.customer.save()
        #     self.given_product.save()

        if self.pay_way != 'sell':
        # if (self.pay_way == 'cash') or (self.pay_way == 'cashless') or (self.pay_way == 'barter')
            self.needed_product.quantity -= self.needed_quantity
            self.needed_cost = self.needed_product.price * self.needed_quantity
            if (self.pay_way == 'cash') or (self.pay_way == 'cashless'):
                self.customer.all_count += self.needed_cost
                if self.pay_way == 'cashless':
                    if self.needed_cost <= self.customer.current_count:
                        self.customer.current_count -= self.needed_cost
                    else:   # если денег на счету недостаточно (мб стоит обнулить текущий счет и снизить )
                        self.pay_way = 'credit'
                        self.customer.credit_count += self.needed_cost - self.customer.current_count
                        self.customer.current_count = 0
            self.needed_product.save()
        if (self.pay_way == 'barter') or (self.pay_way == 'sell'):
            if self.pay_way == 'barter':
                self.given_quantity = math.ceil(self.needed_cost / self.given_product.price)
            self.given_product.quantity += self.given_quantity
            if self.pay_way == 'sell':
                self.given_cost = self.given_product.price * self.given_quantity
                if self.given_cost < self.customer.current_credit:
                    self.customer.current_credit -= self.given_cost
                else:
                    self.customer.current_count += self.given_cost - self.customer.current_credit
                    self.customer.current_credit = 0
            self.given_product.save()
        self.customer.save()
        super().save(*args, **kwargs)
