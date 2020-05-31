from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('product/list/', ProductsListAPIView.as_view(), name="product-list"),
    path('product/searchProduct/', ProductSearchView.as_view(), name="product-list"),
    path('product/searchReceipt/', ReceiptSearchView.as_view(), name="product-list"),
    path('orderOffline/', OrderOfflineView.as_view(), name="product-list"),
    path('orderOnline/', OrderOnlineView.as_view(), name="product-list"),
    path('orderList/online/', OrderListOnlineAPIView.as_view(), name="product-list"),
    path('orderList/offline/', OrderListOfflineAPIView.as_view(), name="product-list"),
    path('home/<int:pk>', market_home_by_id),
    path('receipt/<int:pk>', receipt_by_id),
    path('payment/success/<int:pk>', payment_order_successful),
    path('payment/failed/<int:pk>', payment_order_failed),
    path('menu/', product_by_id),

]
