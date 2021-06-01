from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        return make_password(value)

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role',)
        model = User
