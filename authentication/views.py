from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from authentication.serializers import RegisterSerializer, LoginSerializer
from authentication.models import User
from rest_framework.permissions import IsAuthenticated



class AuthUserAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIView(CreateAPIView):
    authentication_classes = []
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": {
                    "email": user.email,
                    "username": user.username,  # Return the username in the response
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    authentication_classes = []
    
    serializer_class = LoginSerializer  # Define the serializer to use for login

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        # Authenticate user with email and password
        user = authenticate(username=email, password=password)

        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
