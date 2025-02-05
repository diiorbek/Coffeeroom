from django.urls import path
from .views import (UpdatePasswordView, UpdateUserView, ResetPhoneNumberRequestView, ResetPhoneNumberConfirmView, 
					PhoneVerificationView, VerifyPhoneView, RegisterView,LoginView,LogoutView, 
					ResetPasswordRequestView, ResetPasswordConfirmView)

urlpatterns = [
    path('phone/verify/', PhoneVerificationView.as_view(), name='phone_verify'),
    path('phone/confirm/', VerifyPhoneView.as_view(), name='phone_confirm'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="Logout"),
	path('reset-password/request/', ResetPasswordRequestView.as_view(), name='reset_password_request'),
    path('reset-password/confirm/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
	path('change-phone/request/', ResetPhoneNumberRequestView.as_view(), name='reset_phone_request'),
    path('change-phone/confirm/', ResetPhoneNumberConfirmView.as_view(), name='reset_phone_confirm'),
	path('update-user/', UpdateUserView.as_view(), name='update-user'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),

]
