import os.path

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from shortuuid import uuid

from .seriallizers import *

class UploadImageView(APIView):
    def post(self,request):
        serializer = UploadImageSerializer(data = request.data)
        if serializer.is_valid():
            file = serializer.validated_data.get('image')
            # abc.png => sdfsfsdffv + '.png'
            #os.path.splitext('abc.png) = ('abc','png')
            filename = uuid() + os.path.splitext(file.name)[-1]
            path = settings.MEDIA_ROOT / filename
            try:
                with open(path,'wb') as fp:
                    for chunk in file.chunks():
                        fp.write(chunk)
            except Exception:
                return Response(
                    {
                        'erron':1,
                        'message':"图片保存失败拉"

                    }
                )
            file_url = settings.MEDIA_URL + filename
            return Response({
                'errno' : 0,
                'data' : {
                    'url':file_url,
                    'alt':"",
                    'href':file_url
                }
            })
        else:
            print(serializer.errors)
            return Response({
                'erron':1,
                'message':list(serializer.errors.values())[0][0]

            })
