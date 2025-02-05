from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'gender']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.items():
            if value is None:
                representation[key] = ""
        return representation

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.IntegerField()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'password1','password2', 'gender', 'birth_date')

    def create(self, validated_data):
        password = validated_data.get('password1')
        user = User.objects.create_user(

            phone_number=validated_data.get('phone_number'),
            password=password,
            gender=validated_data.get('gender'),
            birth_date=validated_data.get('birth_date')
        )
        return user

    def validate(self, attrs):
       phone_number = attrs.get('phone_number')
       password1 = attrs.get('password1')
       password2 = attrs.get('password2')


       if not phone_number:
           raise serializers.ValidationError('Пожалуйста, введите номер телефона.')

       if password1 != password2:
           raise serializers.ValidationError("Пароли должны совпадать.")



       return super().validate(attrs)
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Пользователь неактивен.")
                return user
            raise serializers.ValidationError("Неправильно введены данные.")
        raise serializers.ValidationError("Надо содержать 'номер телефона' and 'пароль'.")
    

class ResetPasswordRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона не существует.")
        return value

class ResetPasswordConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        verification_code = attrs.get('verification_code')
        new_password = attrs.get('new_password')

        if not phone_number or not verification_code or not new_password:
            raise serializers.ValidationError("Все поля обязательно заполнить.")
        return attrs
    
class ResetPhoneNumberRequestSerializer(serializers.Serializer):
    new_phone_number = serializers.CharField()

    def validate_new_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value


class ResetPhoneNumberConfirmSerializer(serializers.Serializer):
    new_phone_number = serializers.CharField()
    verification_code = serializers.IntegerField()

    def validate(self, attrs):
        new_phone_number = attrs.get('new_phone_number')
        verification_code = attrs.get('verification_code')

        if not new_phone_number or not verification_code:
            raise serializers.ValidationError("All fields are required.")
        return attrs