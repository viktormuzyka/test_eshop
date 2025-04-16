from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from store.services.auth_services import register_user, login_user


class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: openapi.Response(
                description='User created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: 'Bad Request',
            500: 'Internal Server Error',
        }
    )
    def post(self, request):
        try:
            data = request.data
            user = register_user(data['username'], data['email'], data['password'])
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({'error': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description='Login success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            ),
            400: openapi.Response(
                description='Invalid credentials',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
                )
            )
        }
    )
    def post(self, request):
        data = request.data
        user = login_user(data['username'], data['password'])
        if user:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
