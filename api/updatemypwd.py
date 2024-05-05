from rest_framework.views import APIView
from django.shortcuts import render,redirect,HttpResponse
from dal import models
from django.http import JsonResponse


class UpdateMyPwd(APIView):


    def post(self,request):
        old_password = str(request.data.get("old_password"))
        new_password1 = str(request.data.get("new_password1"))
        userid = str(request.data.get("userid"))
        print("old_password:"+old_password)
        print("new_password1:"+new_password1)
        print("userid:"+userid)
        message = {}
        user = models.UserInfo.objects.filter(id=userid,password=old_password).first()
        if user:
            obj = models.UserInfo.objects.get(id=userid)
            obj.password = new_password1
            obj.save()
            message['code'] = 200
            message['message'] = "修改成功"
            return JsonResponse(message)
        else :
           message['code'] = 444
           message['message'] = "修改失败"
           return JsonResponse(message)
class UpdateMyPwdTec(APIView):


    def post(self,request):
        old_password = str(request.data.get("old_password"))
        new_password1 = str(request.data.get("new_password1"))
        userid = str(request.data.get("userid"))
        print("old_password:"+old_password)
        print("new_password1:"+new_password1)
        print("userid:"+userid)
        message = {}
        user = models.TecInfo.objects.filter(id=userid,password=old_password).first()
        if user:
            obj = models.TecInfo.objects.get(id=userid)
            obj.password = new_password1
            obj.save()
            message['code'] = 200
            message['message'] = "修改成功"
            return JsonResponse(message)
        else :
           message['code'] = 444
           message['message'] = "修改失败"
           return JsonResponse(message)