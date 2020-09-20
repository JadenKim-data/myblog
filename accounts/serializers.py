import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

User = get_user_model()

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(write_only=True, required=False)
    avatar_url = serializers.SerializerMethodField('avatar_url_field')

    def avatar_url_field(self, user):
        if user.avatar_url:
            if re.match(r"^https?://", user.avatar_url):
                return user.avatar_url
            if 'request' in self.context:
                host = self.context['request'].get_host()
                return "https://" + host + user.avatar_url
        else:
            return ""

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            gender=validated_data['gender'],
            email=validated_data['email'],
            birth_date=validated_data['birth_date'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.pk)
        # password change
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        # profile update
        else:
            User.objects.filter(pk=instance.pk).update(**validated_data)
        return user

    # TODO: validate_phone_number : -가 입력되지 않은 번호에 대해 -를 추가
    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'avatar', 'avatar_url',  'phone_number', 'gender', 'email', 'birth_date']


class UserConfirmSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    is_confirmed = serializers.SerializerMethodField('is_confirmed_field')

    def is_confirmed_field(self, user):
        user = get_object_or_404(username=username)

    class Meta:
        model = get_user_model()
        abstract = True


class UserPasswordChangeSerializer(UserConfirmSerializer):
    new_password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['username, old_password', 'phone_number']














