from rest_framework import serializers
from authentication.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should not be readable
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']  # Include 'username' in the fields
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be readable
        }

    def create(self, validated_data):
        # Use the create_user method from your custom manager
        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email','username', 'password', 'token')  # Assuming 'token' is a field on your User model
        read_only_fields = ['token']  # 'token' should be read-only during serialization