from rest_framework import serializers
from .models import *
from rest_framework import exceptions
from apps.oaauth.serializers import UserSerializer
from .utils import get_responder


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = "__all__"



class AbsentSerializer(serializers.ModelSerializer):
    absent_type = AbsentTypeSerializer(read_only= True)
    absent_type_id = serializers.IntegerField(write_only=True)
    requester = UserSerializer(read_only= True)
    responder = UserSerializer(read_only= True)


    class Meta:
        model = Absent
        fields = "__all__"

    # 验证absent_type_id是否在数据库中存在
    def validate_absent_type_id(self, value):
        if not AbsentType.objects.filter(pk=value).exists():
            raise exceptions.ValidationError("考勤类型不存在！")
        return value

    def create(self, validated_data):
        #当 DRF 的视图（比如 GenericAPIView、ViewSet）创建序列化器实例时，
        # 会自动把当前的 request、view、format 等信息打包成字典，传给序列化器的 context 参数：
        request = self.context['request']
        user = request.user
        # 获取审批者
        responder = get_responder(request)

        # 如果是董事会的leader，请假就直接通过
        if responder is None:
            validated_data['status'] = AbsentStatusChoices.PASS
        else:
            validated_data['status'] = AbsentStatusChoices.AUDITING
        absent = Absent.objects.create(**validated_data, requester=user, responder=responder)
        return absent

        # update

    def update(self, instance, validated_data):
        if instance.status != AbsentStatusChoices.AUDITING:
            raise exceptions.APIException(detail='不能修改已经确定的请假数据！')
        request = self.context['request']
        user = request.user
        if instance.responder.uid != user.uid:
            raise exceptions.AuthenticationFailed(detail='您无权处理该考勤！')
        instance.status = validated_data['status']
        instance.response_content = validated_data['response_content']
        instance.save()
        return instance