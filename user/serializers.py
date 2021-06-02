from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role',)
        model = User


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmationCodeAndEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.IntegerField()

    def validate(self, data):
        user = get_object_or_404(User, email=data['email'])
        if int(user.confirmation_code) != int(data['confirmation_code']):
            raise serializers.ValidationError('Неверный код подтверждения')
        return data
