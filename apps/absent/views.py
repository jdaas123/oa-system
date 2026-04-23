from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.oaauth.serializers import UserSerializer
from .models import *
from .serializers import *
# Create your views here.
#1发起考勤（create）
#2处理考勤(update)
#3查看考勤(list?who = my)
#4查看下属的考勤(list?who = sub)

class AbsentViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        who = request.query_params.get('who')
        if who and who == 'sub':
            result = queryset.filter(responder=request.user)
        else:
            result = queryset.filter(requester=request.user)

        # result：代表符合要求的数据
        # pageinage_queryset方法：会做分页的逻辑处理
        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # get_paginated_response：除了返回序列化后的数据外，还会返回总数据多少，上一页url是什么
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(result, many=True)
        return Response(data=serializer.data)

# 1、请假类型
class AbsentTypeView(APIView):
    def get(self,request):
        types = AbsentType.objects.all()
        serializer = AbsentTypeSerializer(types,many = True)
        print(serializer)
        #serializer.data才能取序列化后的数据
        return Response(data = serializer.data)


# 2、显示审批者
class ResponderView(APIView):
    def get(self,request):
        responder = get_responder(request)
        #Serializer 如果序列化的对象是一个None，那么不会报错，而是返回一个包含了除了主键外的所有字段的空字段
        serializer = UserSerializer(responder)
        return Response(serializer.data)
