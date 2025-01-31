from rest_framework import serializers
from .models import User
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    password_conform = serializers.CharField(max_length = 68, min_length = 6, write_only = True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_conform']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password_conform = attrs.get('password_conform', '')
        if password != password_conform:
            raise serializers.ValidationError("Passowords do not match")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        return user
