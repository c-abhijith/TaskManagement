from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from taskmanager.serializers import MyTokenObtainPairSerializer  
from taskmanager.models import *  
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response(
                {"detail": "Invalid credentials. Please check username and password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except AuthenticationFailed:
            return Response(
                {"detail": "Authentication failed. User not found or credentials incorrect."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"detail": "Something went wrong.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


