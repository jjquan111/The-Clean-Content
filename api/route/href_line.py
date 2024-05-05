from rest_framework.views import APIView
from django.shortcuts import render


# 数据首页
class line(APIView):
    def get(self,request):
        return render(request, "line.html")
# class TecIndex(APIView):
#     def get(self,request):
#         return render(request, "indextec.html")


class linemain(APIView):
    def get(self,request):
        return render(request, "main.html")