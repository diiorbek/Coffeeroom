from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (UpdatePasswordSerializer, ResetPasswordRequestSerializer, 
						ResetPasswordConfirmSerializer, RegisterSerializer, LoginSerializer, 
						VerifyCodeSerializer,PhoneVerificationSerializer, 
						ResetPhoneNumberRequestSerializer, ResetPhoneNumberConfirmSerializer, 
						UpdateUserSerializer)
from django.contrib.auth import login, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import status, generics
from .utils import send_sms
from .models import User

class PhoneVerificationView(APIView):
    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            verification_code = send_sms(phone_number)
            
            cache.set(phone_number, verification_code, timeout=300)  
            
            return Response({
                "message": f"Verification code sent to your phone. {verification_code}"
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            if not user.check_password(old_password):
                return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        
        if not cache.get(f"verified_{phone_number}"):
            return Response({"message": "Phone number not verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            cache.delete(f"verified_{phone_number}")
            
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyPhoneView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            
            cached_code = cache.get(phone_number)
            
            if cached_code and cached_code == verification_code:
                cache.delete(phone_number)  
                
                cache.set(f"verified_{phone_number}", True, timeout=3600) 
                
                return Response({"message": "Phone number verified successfully."}, status=status.HTTP_200_OK)
            
            return Response({"message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            
            token.blacklist()
            
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
            verification_code = send_sms(phone_number)
            
            cache.set(f"reset_password_{phone_number}", verification_code, timeout=300)
            
            return Response({"message": f"Verification code sent to your phone. {verification_code}"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    """
    Проверяет код подтверждения и обновляет пароль.
    """
    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            new_password = serializer.validated_data['new_password']
            
            cached_code = cache.get(f"reset_password_{phone_number}")
            if cached_code and cached_code == verification_code:
                try:
                    user = User.objects.get(phone_number=phone_number)
                    user.set_password(new_password)
                    user.save()
                    
                    cache.delete(f"reset_password_{phone_number}")
                    
                    return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPhoneNumberRequestView(APIView):
    """
    Отправляет код подтверждения на новый номер телефона.
    """
    def post(self, request):
        serializer = ResetPhoneNumberRequestSerializer(data=request.data)
        if serializer.is_valid():
            new_phone_number = serializer.validated_data['new_phone_number']
            
            try:
                user = request.user
            except User.DoesNotExist:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            verification_code = send_sms(new_phone_number)
            
            cache.set(f"reset_phone_{user}_{new_phone_number}", verification_code, timeout=300)
            
            return Response({"message": f"Verification code sent to your phone. {verification_code}"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPhoneNumberConfirmView(APIView):
    def post(self, request):
        serializer = ResetPhoneNumberConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_phone_number = serializer.validated_data['new_phone_number']
            verification_code = serializer.validated_data['verification_code']
            
            try:
                user = request.user
            except User.DoesNotExist:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            cached_code = cache.get(f"reset_phone_{user}_{new_phone_number}")
            if cached_code and cached_code == verification_code:
                user.phone_number = new_phone_number
                user.save()
                
                cache.delete(f"reset_phone_{user}_{new_phone_number}")
                
                return Response({"message": "Phone number updated successfully."}, status=status.HTTP_200_OK)
            
            return Response({"message": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def create(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)