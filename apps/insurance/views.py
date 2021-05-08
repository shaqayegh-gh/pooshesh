from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404, UpdateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.insurance.models.profile import Profile, User, EvaluationCase
from apps.insurance.serializers import ProfileSerializer, GetUserSerializer, \
    InsurerRegisterSerializer, ChangePasswordSerializer, ProfileUpdateSerializer, \
    InsurerSerializer, AssessorUserSerializer, AssessorRegisterSer,EvaluationCaseSer
from .models.user import AssessorUser, InsurerUser
from .serializers import MyTokenObtainPairSerializer


class IsInsurer(object):
    pass

class IsAssessor(object):
    pass




class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class GetUserAPI(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


class InsurerRegisterAPI(CreateAPIView):
    queryset = InsurerUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = InsurerRegisterSerializer


class ChangePasswordAPI(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    lookup_field = 'id'


class LogoutAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ProfileAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        if user.has_perm(IsAdminUser):
            pass
        elif user.has_perm(IsAssessor):
            pass
        else:
            pass
        profile_serializer = ProfileSerializer(user.profile)
        return Response(profile_serializer.data)


class ProfilesListAPI(APIView):
    permission_classes = [IsAuthenticated &( IsAdminUser|IsAssessor)]
    @staticmethod
    def get(request):
        """List profiles"""
        profiles = Profile.objects.all()
        return Response(ProfileSerializer(profiles, many=True).data)


class ProfileUpdateAPI(UpdateAPIView):
    """api for updating profile information"""
    permission_classes = [IsAuthenticated,]
    serializer_class = ProfileUpdateSerializer
    queryset = Profile.objects.all()
    lookup_field = 'user_id'


class InsurerAPI(APIView):
    permission_classes = (IsAuthenticated & (IsAdminUser|IsAssessor))
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        serializer = InsurerSerializer(user)
        return Response(serializer.data)

class AssessorUserAPI(APIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        serializer = AssessorUserSerializer(user)
        return Response(serializer.data)


class RegisterAssessorAPI(CreateAPIView):
    queryset = AssessorUser.objects.all()
    permission_classes = (IsAuthenticated , IsAdminUser)
    serializer_class = AssessorRegisterSer


class EvalCaseAPI(CreateAPIView):
    queryset = EvaluationCase.objects.all()
    permission_classes = (IsInsurer , IsAuthenticated)
    serializer_class = EvaluationCaseSer