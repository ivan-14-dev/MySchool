# backend/apps/authentication/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import math

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Find user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            
            # Check password
            if not user.check_password(password):
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            
            if not user.is_active:
                msg = _('Account is disabled.')
                raise serializers.ValidationError(msg, code='authorization')
                
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        # Generate tokens
        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)
        
        # Return only the tokens, not the user object
        return {
            'access': access_token,
            'refresh': refresh_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }
    
    def generate_access_token(self, user):
        # Get access token lifetime from settings
        access_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=60))
        if isinstance(access_lifetime, timedelta):
            minutes = access_lifetime.total_seconds() / 60
        else:
            minutes = 60
            
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(minutes=minutes),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    def generate_refresh_token(self, user):
        # Get refresh token lifetime from settings
        refresh_lifetime = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME', timedelta(days=1))
        if isinstance(refresh_lifetime, timedelta):
            days = refresh_lifetime.days
        else:
            days = 1
            
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=days),
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 
                 'password_confirm', 'user_type', 'phone_number')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=payload['email'])
            if not user.is_active:
                raise serializers.ValidationError('User is not active.')
            return token
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Activation link expired.')
        except jwt.exceptions.InvalidTokenError:
            raise serializers.ValidationError('Invalid token.')
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
            return email
        except User.DoesNotExist:
            pass  # Don't reveal that user doesn't exist


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=payload['email'])
            user.set_password(password)
            user.save()
            return attrs
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Reset link expired.')
        except jwt.exceptions.InvalidTokenError:
            raise serializers.ValidationError('Invalid token.')
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."})
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
