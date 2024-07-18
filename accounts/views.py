from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer, UserRegistrationSerializer
from .utils import send_activation_email
from django.shortcuts import get_object_or_404

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_activation_email(user)
        return Response({
            "user": CustomUserSerializer(user).data,
            "message": "User registered successfully. Please check your email to activate your account."
        }, status=status.HTTP_201_CREATED)

class ActivateAccountView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, token):
        user = get_object_or_404(CustomUser, activation_token=token)
        user.is_active = True
        user.save()  # This should trigger the signal
        return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

# ... other views remain the same

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            # If a pk is provided, retrieve that specific profile
            profile = generics.get_object_or_404(UserProfile, pk=pk)
            # Check if the user has permission to view this profile
            
            return profile
        else:
            # If no pk is provided, return the current user's profile
            return self.request.user.profile

    def perform_update(self, serializer):
        # Ensure users can only update their own profile
        if self.request.user.profile != self.get_object():
            raise PermissionDenied("You don't have permission to edit this profile.")
        serializer.save()

class ProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer