import math

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f"{self.name} ({self.quantity} шт.)"


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Фамилия')
    current_count = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name='Текущий счет')
    all_count = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name='Сумма покупок')
    credit_limit = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Потолок кредита')
    current_credit = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name='Текущий кредит')
    left_credit = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Остаток кредита')
    comment = models.CharField(max_length=255, verbose_name='Комментарий')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.left_credit = self.credit_limit - self.current_credit
        super().save(*args, **kwargs)


class Order(models.Model):
    pay_way_choices = (
        ('cash', 'Наличный расчет'),
        ('cashless', 'Безналичный расчет'),
        ('credit', 'Кредит'),
        ('barter', 'Бартер'),
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE,
                                 related_name='orders')
    needed_product = models.ForeignKey(Product, verbose_name='Запаришваемый продукт', related_name='first_product',
                                       on_delete=models.CASCADE)
    needed_quantity = models.PositiveIntegerField(verbose_name='Количество нужного товара')
    needed_cost = models.DecimalField(default=0, max_digits=7, decimal_places=2, editable=False,
                                      verbose_name='Стоимость нужного товара')
    pay_way = models.CharField(max_length=255, choices=pay_way_choices)
    given_product = models.ForeignKey(Product, verbose_name='Отдаваемый продукт', related_name='second_product',
                                      on_delete=models.CASCADE, blank=True, null=True)
    given_quantity = models.PositiveIntegerField(verbose_name='Количество отдаваемого продукта', editable=False,
                                                 blank=True, null=True)
    given_cost = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Стоимость отдаваемого продукта',
                                     editable=False, blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.customer}: {self.needed_product.name} ({self.needed_quantity} шт.)"

    def save(self, *args, **kwargs):
        self.needed_cost = self.needed_product.price * self.needed_quantity
        self.needed_product.quantity -= self.needed_quantity
        self.needed_product.save()
        if self.pay_way == 'cashless':
            self.customer.current_count -= self.needed_cost
            self.customer.all_count += self.needed_cost
        if self.pay_way == 'credit':
            self.customer.current_credit += self.needed_cost
            #   в данном случае сумма покупок не обновляется
        if self.pay_way == 'barter':
            self.given_quantity = math.ceil(self.needed_cost / self.given_product.price)
            self.given_cost = self.given_product.price * self.given_quantity
            self.given_product.quantity += self.given_quantity
            self.given_product.save()
            self.customer.current_credit += self.given_cost
        self.customer.save()
        super().save(*args, **kwargs)
