from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .utils import send_reset_code  # assuming send_reset_code is a function you defined for sending reset codes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from lgbtq_backend.paypal_config import configure_paypal

# User Authentication Views
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Login successful!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not User.objects.filter(email=email).exists():
            return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the function to send the reset code
        code = send_reset_code(email)
        return Response({"message": f"Reset code sent to {email}.", "reset_code": code})

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Prevents user from being logged out after password change
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PayPal Views
@csrf_exempt
def create_paypal_order(request):
    # Ensure that PayPal is configured
    configure_paypal()

    # Create the payment order
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "100.00",  # Amount to be paid
                "currency": "USD"
            },
            "description": "Payment for services"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/execute",
            "cancel_url": "http://localhost:8000/cancel"
        }
    })

    # Create the payment
    if payment.create():
        return JsonResponse({"approval_url": next(link.href for link in payment.links if link.rel == "approval_url")})
    else:
        return JsonResponse({"error": "Unable to create PayPal payment"})


@csrf_exempt
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return JsonResponse({"message": "Payment successfully executed"})
    else:
        return JsonResponse({"error": "Payment execution failed"})


# Profile Views
@login_required
def profile_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile.html', context)
