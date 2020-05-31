from django.urls import path
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserLogoutAPIView, UserEmailAPIView

app_name = 'users'

urlpatterns = [
    path('signup/', UserRegistrationAPIView.as_view(), name="list"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('login/email/', UserEmailAPIView.as_view(), name="email"),

    path('logout/', UserLogoutAPIView.as_view(), name="logout"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
]
