from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import update_session_auth_hash
from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, PostSerializer, CommentSerializer, LikeSerializer, ProfileSerializer, EmojiSerializer, BlogSerializer
from .models import Post, Comment, Like, Profile, Emoji, Blog
from .utils import send_reset_code  # assuming send_reset_code is a function you defined for sending reset codes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from lgbtq_backend.paypal_config import configure_paypal
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# User Authentication Views
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Login successful!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Password Reset Views
class PasswordResetView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        if not User.objects.filter(email=email).exists():
            return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the function to send the reset code
        code = send_reset_code(email)
        return Response({"message": f"Reset code sent to {email}.", "reset_code": code})


class ChangePasswordView(generics.GenericAPIView):
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


# Post Views
class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Associate post with logged-in user


class PostDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()  # Custom deletion logic if needed


# Comment Views
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()  # Custom deletion logic if needed


# Like Views
class LikeToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()  # Remove like if it already exists
            return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)


# PayPal Views
@csrf_exempt
def create_paypal_order(request):
    configure_paypal()

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "100.00",
                "currency": "USD"
            },
            "description": "Payment for services"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/execute",
            "cancel_url": "http://localhost:8000/cancel"
        }
    })

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


# Blog Create View (newly added)
class BlogCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer  # You need to create a BlogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Associate the blog post with the logged-in user
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()  # Replace with your actual model if needed
    serializer_class = BlogSerializer  # Ensure this matches your serializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Adjust based on your requirements
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()  # Make sure your model is correct
    serializer_class = BlogSerializer  # Ensure this serializer is correctly defined for your model
    permission_classes = [IsAuthenticatedOrReadOnly]  # You can adjust this based on your permissions

class BlogDeleteView(generics.DestroyAPIView):
    queryset = Blog.objects.all()  # Specify the model
    serializer_class = BlogSerializer  # Use the Blog serializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can delete blogs

    def perform_destroy(self, instance):
        instance.delete()  # Custom deletion logic if needed


# ViewSets for Profile, Post, Comment, Like, and Emoji Models
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class EmojiViewSet(viewsets.ModelViewSet):
    queryset = Emoji.objects.all()
    serializer_class = EmojiSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Profile Update View
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'accounts/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the error below.")
        return render(request, 'accounts/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})
