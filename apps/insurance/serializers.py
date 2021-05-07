from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile, EvaluationCase
from .models.user import User


class GetUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'profile']

    def get_profile(self, obj):
        try:
            profile = obj.profile
            return ProfileSerializer(profile).data
        except:
            return None


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=128, min_length=8)
    first_name = serializers.CharField(max_length=30, default='',
                                       required=False)
    last_name = serializers.CharField(max_length=30, default='',
                                      required=False)
    phone_number = serializers.CharField(max_length=10)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['phone_number'],
                                        validated_data['first_name'], validated_data['last_name'],
                                        validated_data['password'])
        return user


class UserValidationSer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])

    def validate(self, data):
        user = User.objects.filter(email=data["email"])
        if user.exists():
            raise serializers.ValidationError({"email": "user with this email already exists"})

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('national_code', 'birthday', 'gender', 'address', 'national_card', 'birth_certificate')


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCase
        fields = ""
