from rest_framework.views import APIView
from django.shortcuts import render,redirect,HttpResponse
from dal import models
from django.http import JsonResponse


class Register(APIView):

    def get(self,request):
        return render(request, "ui-login.html")

    def post(self,request):
        username = str(request.data.get("register_username"))
        email = str(request.data.get("register_email"))
        name = str(request.data.get("register_name"))
        classname = str(request.data.get("register_classname"))
        phone = str(request.data.get("register_phone"))
        password = str(request.data.get("register_password"))
        message = {}
        print(username,password)
        try:
            models.UserInfo.objects.create(username=username,password=password,
                                           email=email,name=name,classname=classname,
                                           phone=phone)
            message['code'] = 200
            message['message'] = "注册成功"
            return JsonResponse(message)
        except Exception as e:
            print(e)
            message['code'] = 444
            message['message'] = "注册失败"
            return JsonResponse(message)

