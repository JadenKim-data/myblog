from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            gender=validated_data['gender'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    #TODO: validate_phone_number : -가 입력되지 않은 번호에 대해 -를 추가
    class Meta:
        model = User
        fields = ['pk', 'avatar', 'avatar_url', 'username', 'phone_number', 'gender', 'email', 'password']
