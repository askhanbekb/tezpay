from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import *


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Market
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    market = MarketSerializer(read_only=True)
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Products
        fields = '__all__'


class ProductHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    product = ProductHomeSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    market = MarketSerializer(read_only=True)
    payed = serializers.SerializerMethodField()

    class Meta:
        model = Receipts
        fields = '__all__'

    def get_payed(self, obj):
        if obj.get_payed_display() == "1":
            return "Yes"
        elif obj.get_payed_display() == "2":
            return "No"


class ReceiptUsualSerializer(serializers.ModelSerializer):
    market = MarketSerializer(read_only=True)

    class Meta:
        model = Receipts
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    receipt = ReceiptSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Delivery
        fields = '__all__'

    def get_status(self, obj):
        return obj.get_status_display()
