from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls


api_urls = [
    path('users/', include('users.urls')),
    path('core/', include('tezpay.urls')),
]

# generator_urls = [
#     path('data/', include('generator.urls')),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urls)),
]

urlpatterns += [
    path('api/docs/', include_docs_urls(title='Tez Pay documentation', authentication_classes=[],
                                        permission_classes=[]))]
