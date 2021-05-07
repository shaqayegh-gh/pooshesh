from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import get_object_or_404, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.insurance.models.profile import Profile, User
from apps.insurance.serializers import SignupSerializer, ProfileSerializer, GetUserSerializer, ProfileSerializerUpdate


class GetUserAPI(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


class RegisterAPI(APIView):
    """api for register new user"""

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            if user:
                token = AuthToken.objects.create(user)[1]
                json = serializer.data
                json['token'] = token
                login(request, user)
                return Response(json, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Update password for authenticated user
        """

        password = request.data.get('password')

        try:
            validate_password(password)
            request.user.set_password(password)
            request.user.save()
            return Response({'success': 'Password has been updated'})
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ProfileAPI(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        profile_serializer = ProfileSerializer(user.profile)
        return Response(profile_serializer.data)


class ProfilesListAPI(APIView):
    @staticmethod
    def get(request):
        """List profiles"""
        profiles = Profile.objects.all()
        return Response(ProfileSerializer(profiles, many=True).data)


class ProfileUpdateAPI(UpdateAPIView):
    """api for updating profile information"""
    serializer_class = ProfileSerializerUpdate
    queryset = Profile.objects.all()
    lookup_field = 'user_id'
