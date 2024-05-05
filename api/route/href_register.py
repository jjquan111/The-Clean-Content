from rest_framework.views import APIView
from django.shortcuts import render


# 注册
class Register(APIView):
    def get(self,request):
        return render(request, "ui-register.html")