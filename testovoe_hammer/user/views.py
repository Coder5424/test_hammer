from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import UserSerializer, UserDataSerializer, UserCodeSerializer
from rest_framework.views import APIView
import random
import string
from core.models import User


class CreateUserView(generics.GenericAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """Create and return new user"""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCredentialsView(APIView):
    """Check user data"""
    serializer_class = UserDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserDataSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            user = data.get('user')

            request.session['id'] = user.id

            code = '0000'

            user.code = code
            user.save()

            return Response({'message': 'Code sent'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthView(APIView):
    """Auth user in system"""
    serializer_class = UserCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserCodeSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            code = data.get('code')

            user = User.objects.get(
                id=request.session['id'],
            )

            if code == user.code:
                user.code = None

                if user.invite_code is None:
                    invite_code = ''.join(
                        random.choices(
                            string.ascii_uppercase + string.digits,
                            k=6
                        )
                    )
                    user.invite_code = invite_code

                user.save()

                login(request, user)

                return Response({'message': 'Auth successful.'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
