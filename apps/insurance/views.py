from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.insurance.models import User
from apps.insurance.models.profile import Profile
from apps.insurance.serializers import UserDetailSerializer,SignupSerializer


# class RegisterView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = SignupSerializer
#     permission_classes = (AllowAny,)


class RegisterView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)