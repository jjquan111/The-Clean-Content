from rest_framework.views import APIView
from django.shortcuts import render


# 数据首页
class StudyIndex(APIView):
    def get(self,request):
        return render(request, "index.html")
class TecIndex(APIView):
    def get(self,request):
        return render(request, "indextec.html")