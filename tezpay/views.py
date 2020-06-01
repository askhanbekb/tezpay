from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from collections import OrderedDict
from django.shortcuts import get_object_or_404
import hashlib


class ProductsListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Products.objects.all()


class OrderListOnlineAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return Receipts.objects.filter(shop_type_id=2, user_id=self.request.user.id).all()[::-1]


class OrderListOfflineAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return Receipts.objects.filter(shop_type_id=1, user_id=self.request.user.id).all()[::-1]


@api_view(['GET'])
def market_home_by_id(request, pk):
    try:
        market = Market.objects.get(id=pk)
        products = Products.objects.filter(market_id=pk).all()
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        m_serializer = MarketSerializer(market)
        p_ser = ProductHomeSerializer(products, many=True)
        return Response({"market": m_serializer.data, "products": p_ser.data})


@api_view(['GET'])
def receipt_by_id(request, pk):
    try:
        receipt = Receipts.objects.get(id=pk)
        order = Orders.objects.filter(receipt=pk).all()
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        rec = ReceiptSerializer(receipt)
        return Response({"receipt": rec.data, "orders": OrderSerializer(order, many=True).data})


@api_view(['POST'])
@permission_classes([AllowAny])
def payment_order_successful(request, pk):
    try:
        Receipts.objects.filter(pk=pk).update(payed=1)
        rr = Receipts.objects.get(pk=pk)
        r = ReceiptSerializer(rr)
        return Response(r.data)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def payment_order_failed(request, pk):
    try:
        Receipts.objects.filter(pk=pk).update(payed=4)
        rr = Receipts.objects.get(pk=pk)
        r = ReceiptSerializer(rr)
        return Response(r.data)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def product_by_id(request):
    try:
        market = Market.objects.get(pk=request.data["marketId"])
        products = Products.objects.filter(market_id=request.data["marketId"],
                                           category__in=[request.data["categoryId"]]).all()

    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        c_serializer = MarketSerializer(market)
        p_ser = ProductHomeSerializer(products, many=True)
        return Response({"categories": c_serializer.data, "products": p_ser.data})


class ProductSearchView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductHomeSerializer

    def post(self, request):
        product = get_object_or_404(Products, barcode=request.data["barcode"])
        serializer = ProductHomeSerializer(product)
        return Response(serializer.data)

    # def post(self, request):
    #     st = "payment.php;25;Описание заказа;529059;123;https://example.com;some_random_string;1;EwPpzVVfpMMT2QM3"
    #     result = hashlib.md5(st.encode())
    #     return Response({"ok": result.hexdigest()})


class ReceiptSearchView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReceiptSerializer

    def post(self, request):
        receipt = get_object_or_404(Receipts, receipt_id=request.data["id"])
        serializer = ReceiptSerializer(receipt)
        return Response(serializer.data)

    # def post(self, request):
    #     st = "payment.php;25;Описание заказа;529059;123;https://example.com;some_random_string;1;EwPpzVVfpMMT2QM3"
    #     result = hashlib.md5(st.encode())
    #     return Response({"ok": result.hexdigest()})




class OrderOfflineView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order_list = list(request.data["productIds"])
            receipt = Receipts.objects.create(user_id=self.request.user.id, shop_type_id=1,
                                              address="offline")
            market = 0
            price = 0
            for prod in order_list:
                product_price = Products.objects.get(pk=int(prod["productId"])).price
                price = (product_price * prod["count"]) + price
                Orders.objects.create(shop_type_id=1,
                                      count=int(prod["count"]),
                                      user_id=int(self.request.user.id),
                                      product_id=int(prod["productId"]),
                                      receipt_id=int(receipt.pk))
            success_url = "https://tezpay.herokuapp.com/api/v1/core/payment/success/"

            suffix_url = "payment.php;" + str(price) + ";Заказ продуктов;529059;" + str(
                int(receipt.pk)) + ";" + success_url + str(
                int(receipt.pk)) + ";tezpay_random_string;1;EwPpzVVfpMMT2QM3"
            result = hashlib.md5(suffix_url.encode())

            payment_get_url = "https://api.paybox.money/payment.php?pg_merchant_id=529059&pg_amount=" + str(
                price) + "&pg_salt=tezpay_random_string&pg_order=" + str(int(
                receipt.pk)) + "&pg_description=Заказ продуктов&pg_result_url=" + success_url + str(
                int(receipt.pk)) + "&pg_sig=" + result.hexdigest() + "&pg_testing_mode=1"
            Receipts.objects.filter(pk=receipt.pk).update(price=price, market_id=1,
                                                          payed=2, payment_url=payment_get_url)  # Status waiting

            del_obj = Delivery.objects.create(receipt_id=receipt.pk)
            del_ser = DeliverySerializer(del_obj)
            return Response(del_ser.data)


class OrderOnlineView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order_list = list(request.data["productIds"])
            receipt = Receipts.objects.create(user_id=self.request.user.id, shop_type_id=2,
                                              address=request.data["address"])
            market = 0
            price = 0
            for prod in order_list:
                product_price = Products.objects.get(pk=int(prod["productId"])).price
                price = (product_price * prod["count"]) + price
                Orders.objects.create(shop_type_id=2,
                                      count=int(prod["count"]),
                                      user_id=int(self.request.user.id),
                                      product_id=int(prod["productId"]),
                                      receipt_id=int(receipt.pk))
            success_url = "https://tezpay.herokuapp.com/api/v1/core/payment/success/"

            suffix_url = "payment.php;" + str(price) + ";Заказ продуктов;529059;" + str(
                int(receipt.pk)) + ";" + success_url + str(
                int(receipt.pk)) + ";tezpay_random_string;1;EwPpzVVfpMMT2QM3"
            result = hashlib.md5(suffix_url.encode())

            payment_get_url = "https://api.paybox.money/payment.php?pg_merchant_id=529059&pg_amount=" + str(
                price) + "&pg_salt=tezpay_random_string&pg_order=" + str(int(
                receipt.pk)) + "&pg_description=Заказ продуктов&pg_result_url=" + success_url + str(
                int(receipt.pk)) + "&pg_sig=" + result.hexdigest() + "&pg_testing_mode=1"
            Receipts.objects.filter(pk=receipt.pk).update(price=price, market_id=1,
                                                          payed=2, payment_url=payment_get_url)  # Status waiting

            del_obj = Delivery.objects.create(receipt_id=receipt.pk)
            del_ser = DeliverySerializer(del_obj)
            return Response(del_ser.data)
