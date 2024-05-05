from rest_framework.views import APIView
from django.shortcuts import render


# 个人信息跳转
class ProHref(APIView):
    def get(self,request):
        return render(request, "pro-message.html")
class ProHrefTec(APIView):
    def get(self,request):
        return render(request, "pro-messagetec.html")
