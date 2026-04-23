from rest_framework import serializers
from apps.oaauth.serializers import UserSerializer,DepartmentSerializer
from .models import *
from apps.oaauth.models import OADepartment

class InformReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformRead
        fields = "__all__"
class InformSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only= True)
    departments = DepartmentSerializer(read_only=True,many = True)
    #department_ids:是一个包含了部门id的列表
    #如果后端要接收列表，那就需要用到listfield
    department_ids = serializers.ListField(write_only=True)
    reads = InformReadSerializer(many=True, read_only=True)

    print("我进来啦")

    class Meta:
        model = Inform
        fields = '__all__'
        read_only_fields = ('public',)

    def create(self, validated_data):
        department_ids = validated_data.pop('department_ids')
        #department_ids :['1','2','3']
        #对列表中的某个值做相同的操作，那么可以借助map
        department_ids = list(map(int,department_ids))

        request = self.context['request']
        if 0 in department_ids:
            inform = Inform.objects.create(public = True,author = request.user,**validated_data)

        else:
            departments = OADepartment.objects.filter(id__in = department_ids)
            inform = Inform.objects.create(public=False, author=request.user, **validated_data)
            #对某个字段单独创建
            inform.departments.set(departments)
            inform.save()
        return inform

class ReadInformSerializer(serializers.Serializer):
    inform_pk = serializers.IntegerField(error_messages={"required": '请传入inform的id！'})