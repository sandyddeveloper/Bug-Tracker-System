from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user

class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data = user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            send_code_to_user(user['email'])
            #save email function user['email']
            print(user)
            return Response({
                'data':user,
                'message':f'hey thanks for signing up a passcode'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)