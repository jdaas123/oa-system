from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.views import APIView
from .models import Inform
from .serializers import *
from django.db.models import Q ,Prefetch
# Create your views here.



class InformViewSet(ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class =  InformSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related('author').prefetch_related(Prefetch('reads',queryset= InformRead.objects.filter(user_id = self.request.user.uid)),'departments').filter(Q(public = True) |
                                                                                                         Q(departments = self.request.user.department) |
                                                                                                         Q(author = self.request.user)).distinct()
        print(queryset)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.uid == request.user.uid:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['read_count'] = InformRead.objects.filter(inform_id = instance.id).count()
        return Response(data = data)


class ReadInformView(APIView):
    def post(self,request):
        serializer = ReadInformSerializer(data = request.data)
        if serializer.is_valid():
            inform_pk = serializer.validated_data.get('inform_pk')
            if InformRead.objects.filter(inform_id = inform_pk,user_id = request.user.uid).exists():
                return Response()
            else:
                try:
                    InformRead.objects.create(inform_id = inform_pk,user_id= request.user.uid)
                except Exception as e:
                    print(e)
                    return Response(data={'detail':'阅读失败'},status = status.HTTP_400_BAD_REQUEST)
                return Response()

        else:
            return Response(data = {'detail':list(serializer.errors.values())[0][0]},status = status.HTTP_400_BAD_REQUEST)