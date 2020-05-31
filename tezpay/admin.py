from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Market)
admin.site.register(Receipts)
admin.site.register(Delivery)
admin.site.register(Status)
admin.site.register(Orders)
admin.site.register(ShopType)
