from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt.exceptions import ExpiredSignatureError
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
import jwt
from django.conf import settings
from rest_framework.status import HTTP_403_FORBIDDEN
from django.contrib.auth import get_user_model


class LoginCheckMiddleware(MiddlewareMixin):
    keyword = "JWT"

    white_list = ['/auth/login', '/staff/active']

    def process_view(self,request,view_func,view_args,view_kwargs):
        #1.如果返回None，那么会正常执行，（包括执行视图、执行其他的中间件的代码）
        #2。如果返回一个HttpResponse对象，那么将不会执行视图，以后后面的中间件代码
        if request.path in self.white_list or request.path.startswith(settings.MEDIA_URL):#如果是登录界面，则不用
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser
            request.auth = None
            return None

        try:
            auth = get_authorization_header(request).split()
            print('auth:',auth)
            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.AuthenticationFailed("请传入jwt")

            if len(auth) == 1:
                msg = "不可用的JWT头部"
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = "不可用的JWT头部，JWT中间不应该有空格"
                raise exceptions.AuthenticationFailed(msg)

            try:
                jwt_token = auth[1]
                jwt_info = jwt.decode(jwt_token,settings.SECRET_KEY,algorithms='HS256')
                userid = jwt_info.get('userid')
                try:
                    OAUser = get_user_model()
                    #绑定当前user到request对象上
                    user = OAUser.objects.get(pk = userid)
                    request.user = user
                    request.auth = jwt_token
                except:
                    msg = "用户不存在"
                    raise exceptions.AuthenticationFailed(msg)
            except ExpiredSignatureError:
                msg = "JWT Token已过期"
                raise exceptions.AuthenticationFailed(msg)

        except Exception as e:
            print(e)
            return JsonResponse(data = {"detail":"请先登录"},status = HTTP_403_FORBIDDEN)


