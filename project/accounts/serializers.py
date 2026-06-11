from .models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'roll_no']
        extra_kwargs = {'password': {'write_only': True}} 

    def validate_email(self, value):
        if not value.endswith('@snu.edu.in'):
            raise serializers.ValidationError("Please use your SNU mail id.")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
