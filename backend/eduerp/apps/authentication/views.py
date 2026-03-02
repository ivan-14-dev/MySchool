# backend/apps/authentication/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import datetime, timedelta

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    EmailVerificationSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer,
    ChangePasswordSerializer
)
from apps.users.models import User

class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        
        # Generate email verification token
        token = self.generate_email_verification_token(user)
        
        # Send verification email
        self.send_verification_email(user, token)
        
        return Response(user_data, status=status.HTTP_201_CREATED)
    
    def generate_email_verification_token(self, user):
        payload = {
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    def send_verification_email(self, user, token):
        current_site = get_current_site(self.request).domain
        relative_link = reverse('verify_email')
        abs_url = f'http://{current_site}{relative_link}?token={token}'
        
        subject = 'Verify your email address'
        message = f'Hi {user.get_full_name()},\n\nPlease click the link below to verify your email address:\n{abs_url}\n\nThank you!'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=payload['email'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            
            current_site = get_current_site(request).domain
            relative_link = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            abs_url = f'http://{current_site}{relative_link}'
            
            subject = 'Password Reset Request'
            message = f'Hello {user.get_full_name()},\n\nYou requested a password reset. Please click the link below to reset your password:\n{abs_url}\n\nIf you did not request this, please ignore this email.\n\nThank you!'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        
        return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({'success': True, 'message': 'Valid credentials', 'uidb64': uidb64, 'token': token}, 
                          status=status.HTTP_200_OK)
            
        except (UnicodeError, User.DoesNotExist):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
                
            user.set_password(serializer.validated_data['password'])
            user.save()
            
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
            
        except (UnicodeError, User.DoesNotExist):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)