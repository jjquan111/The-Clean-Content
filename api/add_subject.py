from rest_framework.views import APIView
from django.shortcuts import render,redirect,HttpResponse
from dal import models
from django.http import JsonResponse


class AddSubject(APIView):


    def post(self,request):
        username = str(request.data.get("username"))
        subject_title_id = str(request.data.get("subject_title_id"))
        user_id = models.UserInfo.objects.get(username=username).pk  

        subject_title_obj = models.Subject.objects.get(pk=subject_title_id) 
        message = {}
        try:

            subject_title_obj.subject_student.add(user_id)

            message['code'] = 200
            message['message'] = "success"
            return JsonResponse(message)
        except Exception as e:
            print(e)
            message['code'] = 444
            message['message'] = "faile"
            return JsonResponse(message)
