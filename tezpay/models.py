from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid


class Category(models.Model):
    name = models.CharField(max_length=555, blank=False, null=True)
    image = models.CharField(max_length=555, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Status(models.Model):
    title = models.CharField(max_length=555, blank=False, null=True)

    def __str__(self):
        if self.title is None:
            return "No"
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Market(models.Model):
    title = models.CharField(max_length=555, blank=False, null=True)
    address = models.CharField(max_length=555, blank=True, null=True)
    delivery_price = models.FloatField(blank=True, null=True)
    category = models.ManyToManyField(Category)

    def __str__(self):
        if self.title is None:
            return "No"
        return self.title

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class ShopType(models.Model):
    title = models.CharField(max_length=555, blank=False, null=True)

    def __str__(self):
        if self.title is None:
            return "No"
        return self.title

    class Meta:
        verbose_name = "Тип покупки"
        verbose_name_plural = "Тип покупки"


class Products(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=555, blank=False, null=True)
    barcode = models.CharField(max_length=555, blank=False, null=True)
    description = models.CharField(max_length=555, blank=True, null=True)
    price = models.FloatField(blank=False, null=True)
    image = models.CharField(max_length=555, blank=False, null=True)
    created_date = models.DateTimeField(default=now, blank=True)
    market = models.ForeignKey(Market, null=True, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


PRODUCT_PAYED = (
    (1, 'Yes'),
    (2, 'No')
)

DELIVERY_STATUS = (
    (1, 'Waiting'),
    (2, 'Progress'),
    (3, 'Done'),
    (4, 'Canceled'),
)


class Receipts(models.Model):
    #TODO card not null
    shop_type = models.ForeignKey(ShopType, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=555, blank=False, null=True)
    payment_url = models.CharField(max_length=555, blank=False, null=True)
    receipt_id = models.CharField(max_length=555, blank=False, null=True, default=uuid.uuid4)
    price = models.FloatField(blank=True, null=True)
    market = models.ForeignKey(Market, null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now, blank=True, null=True)
    payed = models.CharField(max_length=555, blank=True, null=True, choices=PRODUCT_PAYED, default=2)

    # qr code

    def __str__(self):
        if self.receipt_id is None:
            return "No"
        return self.receipt_id

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чек"


class Delivery(models.Model):
    address = models.CharField(max_length=555, blank=False, null=True, default=uuid.uuid4)
    price = models.FloatField(blank=True, null=True, default=400)  # supermarket delivery price
    status = models.CharField(max_length=555, blank=False, null=True, choices=DELIVERY_STATUS, default=1)
    receipt = models.ForeignKey(Receipts, null=True, on_delete=models.CASCADE)

    # qr code
    def __str__(self):
        if self.address is None:
            return "No"
        return self.address

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставка"


class Orders(models.Model):
    count = models.IntegerField(null=True, blank=True, default=1)
    shop_type = models.ForeignKey(ShopType, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, null=True, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipts, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
