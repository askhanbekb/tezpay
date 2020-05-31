from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer, UserEmailSerializer
from django.contrib.auth import logout


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserEmailAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserEmailSerializer

    def post(self, request, *args, **kwargs):
        # user = User.objects.get(email__exact=request.data["email"])
        email_send(request.data["email"])
        # serializer = self.get_serializer(data=request.data)

        return Response(
            data={"ss"},
            status=status.HTTP_200_OK)

        # if serializer.is_valid():
        #     user = serializer.user
        #     token, _ = Token.objects.get_or_create(user=user)
        #     return Response(
        #         data=TokenSerializer(token).data,
        #         status=status.HTTP_200_OK)
        # else:
        #     return Response(
        #         data=serializer.errors,
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )


def email_send(email):
    data = """
    Hello there!

    I wanted to personally write an email in order to welcome you to our platform.\
     We have worked day and night to ensure that you get the best service. I hope \
    that you will continue to use our service. We send out a newsletter once a \
    week. Make sure that you read it. It is usually very informative.

    Cheers!
    ~ Yasoob
        """
    send_mail('Welcome!', data, "YasoobBottom",
              [email], fail_silently=False)


class UserTokenAPIView(RetrieveDestroyAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)


class UserLogoutAPIView(GenericAPIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(
            data="success",
            status=status.HTTP_200_OK)
