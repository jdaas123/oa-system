from django.shortcuts import render
from rest_framework.views import APIView
from datetime import datetime
# Create your views here.
from .serializers import *
from .authentications import generate_jwt
from rest_framework.response import Response
from rest_framework import status




class LoginView(APIView):
    def post(self,request):
        #1.校验数据是否可用
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.now()
            user.save()
            #生成token
            token = generate_jwt(user)
            return Response({'token':token,'user':UserSerializer(user).data})

        else:
            print(serializer.errors)
            #drf在返回响应时非200时，他的错误名叫detail，所以我们这里也叫detail
            return Response({'detail':"参数验证失败"},status=status.HTTP_400_BAD_REQUEST)

class ResetPwdView(APIView):
    def post(self,request):
        serializer = ResetpwdSerializer(data = request.data,context = {'request':request})
        if serializer.is_valid():
            pwd1 = serializer.validated_data.get('pwd1')
            request.user.set_password(pwd1)
            request.user.save()
            return Response()
        else:
            print(serializer.errors)
            detail = list(serializer.errors.values())[0][0]
            return Response({'detail':detail},status = status.HTTP_400_BAD_REQUEST)

