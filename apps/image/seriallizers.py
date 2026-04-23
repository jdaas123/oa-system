from rest_framework import serializers
from django.core.validators import FileExtensionValidator

class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField(
        validators=[FileExtensionValidator(['png','jpg','jpeg','gif'])],
        error_messages={'required':'请上传图片！','invalid_image':'请上传正确格式的图片！'}
    )

    def validate_image(self,value):
        #图片大小单位是字节
        size = value.size
        max_size = 0.5 * 1024 * 1024
        if size > max_size:
            raise serializers.ValidationError("图片大小最大不超过0.5MB")
        return value