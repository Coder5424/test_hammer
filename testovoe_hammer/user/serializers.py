"""
Serializers for the user API View.
"""
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class UserDataSerializer(serializers.Serializer):
    """Serializer for the user data"""

    phone_number = PhoneNumberField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate the user."""

        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=phone_number,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserCodeSerializer(serializers.Serializer):
    """Serializer for the user code"""

    code = serializers.CharField()


