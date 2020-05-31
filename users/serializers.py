from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.core.mail import send_mail


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "email", "password", "date_joined")

    def create(self, validated_data):
        user = super(UserRegistrationSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    # def validate(self, attrs):
    #     pass


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class UserEmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserEmailSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            user = User.objects.get(email__exact=attrs.get["email"])
            # email_send(attrs.get["email"])
        except User.DoesNotExist:
            pass
            # id = User.objects.create(email=attrs.get["email"], username=attrs.get["email"],  )




class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')
    user = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ("auth_token", "created", "user", "type")

    def get_user(self, obj):
        serialized = UserRegistrationSerializer(obj.user)
        return serialized.data

    def get_type(self, obj):
        if "security_" in obj.user.username:
            return "security"
        else:
            return "no"