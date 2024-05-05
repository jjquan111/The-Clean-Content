from rest_framework.views import APIView
from django.shortcuts import render, redirect, HttpResponse
from dal import models
from django.http import JsonResponse


class Login(APIView):
    def get(self, request):
        return render(request, "ui-login.html")

    def post(self, request):
        username = str(request.data.get("username"))
        password = str(request.data.get("password"))
        message = {}
        # 认证账号密码
        user = models.UserInfo.objects.filter(username=username,password=password).first()
        if user:
            request.session['username'] = username
            message['code'] = 200
            message['message'] = "登录成功"
            return JsonResponse(message)
        else :
            message['code'] = 444
            message['message'] = "登录失败"
            return JsonResponse(message)

class LoginTec(APIView):
    def get(self, request):
        return render(request, "ui-loginTec.html")

    def post(self, request):
        username = str(request.data.get("username"))
        password = str(request.data.get("password"))
        message = {}
        # 认证账号密码
        user = models.TecInfo.objects.filter(username=username,password=password).first()
        if user:
            request.session['username'] = username
            message['code'] = 200
            message['message'] = "登录成功"
            return JsonResponse(message)
        else :
            message['code'] = 444
            message['message'] = "登录失败"
            return JsonResponse(message)
