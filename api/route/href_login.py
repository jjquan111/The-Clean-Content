from rest_framework.views import APIView
from django.shortcuts import render


# 学生登录
class Login(APIView):
    def get(self,request):
        return render(request, "ui-login.html")
        
class loginTec (APIView):
    def get(self,request):
        return render(request, "ui-loginTec.html")