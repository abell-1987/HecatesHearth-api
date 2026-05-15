from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Handles the authentication of a user"""
    email = request.data["email"]
    password = request.data["password"]

    user_exists = User.objects.filter(username=email).exists()

    if not user_exists:
        return Response({"valid": False, "reason": "user_not_found"})

    authenticated_user = authenticate(username=email, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        return Response({"valid": True, "token": token.key})

    return Response({"valid": False, "reason": "incorrect_password"})


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """Handles the creation of a new user for authentication"""
    email = request.data.get("email", None)
    first_name = request.data.get("first_name", None)
    last_name = request.data.get("last_name", None)
    password = request.data.get("password", None)

    if (
        email is not None
        and first_name is not None
        and last_name is not None
        and password is not None
    ):

        try:
            new_user = User.objects.create_user(
                username=request.data["email"],
                email=request.data["email"],
                password=request.data["password"],
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
            )
        except IntegrityError:
            return Response(
                {"message": "An account with that username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = Token.objects.create(user=new_user)
        return Response({"token": token.key})

    return Response(
        {"message": "You must provide email, password, first_name, and last_name"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_current_user(request):
    """Handle GET requests for single user"""
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    except Exception as ex:
        return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class UserSerializer(serializers.ModelSerializer):
    """JSON Serializer"""

    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")

    class Meta:
        model = User
        fields = (
            "id",
            "firstName",
            "lastName",
            "username",
        )
