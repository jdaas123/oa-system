from rest_framework import serializers
from .models import *
from rest_framework import exceptions
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required= True)
    password = serializers.CharField(max_length=20,min_length=6)

    #全局校验
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get("password")

        if email and password:
            user:OAUser = OAUser.objects.filter(email= email).first() #.first()会在查询集中返回第一个，如果没有则返回空
            if not user:
                """没有此用户"""
                raise serializers.ValidationError("请输入正确的邮箱!")
            if not user.check_password(password):
                """密码错误"""
                raise serializers.ValidationError("密码错误!")
            #判断状态
            if user.status == UserStatusChoices.UNACTIVE:
                """用户没激活"""
                raise serializers.ValidationError("该用户未激活!")
            elif user.status == UserStatusChoices.LOCKED:
                """用户被锁"""
                raise serializers.ValidationError('用户被锁定，请联系管理员')
            #为了减少SQL语句的次数，这里把user直接放到attrs中，方便在视图里使用
            attrs["user"] = user
        else:
            raise serializers.ValidationError("请输入邮箱和密码")

        return attrs

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = OAUser
        # fields = "__all__"
        exclude = ['password',"groups","user_permissions"]#exclude---排除哪些字段


class ResetpwdSerializer(serializers.Serializer):
    oldpwd = serializers.CharField(min_length=6,max_length=20)
    pwd1 = serializers.CharField(min_length=6,max_length=20)
    pwd2 = serializers.CharField(min_length=6,max_length=20)

    def validate(self, attrs):
        oldpwd = attrs['oldpwd']
        pwd1 =attrs['pwd1']
        pwd2 =attrs["pwd2"]

        user = self.context['request'].user
        if not user.check_password(oldpwd):
            raise exceptions.ValidationError("旧密码错误")
        if pwd1 != pwd2:
            raise exceptions.ValidationError("两次密码不一致")
        return attrs



