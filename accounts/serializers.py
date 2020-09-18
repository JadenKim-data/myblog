import re
from django.contrib.auth import get_user_model
from rest_framework import serializers


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

    def avatar_url_field(self, author):
        if re.match(r"^https?://", author.avatar_url):
            return author.avatar_url
        if 'request' in self.context:
            scheme = self.context['request'].scheme
            host = self.context['request'].get_host()
            return scheme + "://" + host + author.avatar_url

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            gender=validated_data['gender'],
            email=validated_data['email'],
            birth_date=validated_data['birth_date'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def partial_update(self, validated_data):
        user = self.get_object()
        if validated_data['password']:
            user.set_password(validated_data['password'])
        for field in validated_data:
            user.field = field
        user.save()
        return user

    #TODO: validate_phone_number : -가 입력되지 않은 번호에 대해 -를 추가
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'password', 'avatar', 'avatar_url',  'phone_number', 'gender', 'email', 'birth_date']


# class UserRetrieveSerializer(AbstractUserSerializer):
#     class Meta:
#         fields = ['pk', 'avatar_url', 'username', 'email']


# class UserProfileUpdateSerializer(AbstractUserSerializer):
#     class Meta:
#         fields = ['pk', 'avatar', 'avatar_url', 'username', 'phone_number', 'gender', 'email']


# class UserPasswordUpdateSerializer(AbstractUserSerializer):
#     pass