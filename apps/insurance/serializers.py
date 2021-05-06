from rest_framework.validators import UniqueValidator

from .models.user import User
from rest_framework import serializers


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class SignupSerializer(serializers.Serializer):
    """
    Don't require email to be unique so visitor can signup multiple times,
    if misplace verification email.  Handled in view.
    """
    email = serializers.EmailField(max_length=255,required=True,
            validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=128,min_length=8)
    first_name = serializers.CharField(max_length=30, default='',
                                       required=False)
    last_name = serializers.CharField(max_length=30, default='',
                                      required=False)
    phone_number = serializers.CharField(max_length=10)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['phone_number'],
                                        validated_data['first_name'],validated_data['last_name'],
                                        validated_data['password'])
        return user


