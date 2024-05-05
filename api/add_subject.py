from rest_framework.views import APIView
from django.shortcuts import render,redirect,HttpResponse
from dal import models
from django.http import JsonResponse


class AddSubject(APIView):


    def post(self,request):
        username = str(request.data.get("username"))
        subject_title_id = str(request.data.get("subject_title_id"))
        user_id = models.UserInfo.objects.get(username=username).pk     #  学生ID

        subject_title_obj = models.Subject.objects.get(pk=subject_title_id) # 课程ID
        message = {}
        try:
            # 课程ID 多对多 添加对应字段的 学生ID
            subject_title_obj.subject_student.add(user_id)

            message['code'] = 200
            message['message'] = "添加成功"
            return JsonResponse(message)
        except Exception as e:
            print(e)
            message['code'] = 444
            message['message'] = "添加失败"
            return JsonResponse(message)