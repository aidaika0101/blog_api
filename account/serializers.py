from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User

from comment.serializers import CommentUserSerializer


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password2 = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        # print(attrs, '!!!!1')
        password2 = attrs.pop('password2')
        if password2 != attrs['password']:
            raise serializers.ValidationError(
                'Password didn\'t match'

            )
        validate_password(attrs['password'])
        return attrs


    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['comments'] = CommentUserSerializer(
            instance.comments.all(), manu=True
        ).data
        return repr