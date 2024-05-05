import os
import subprocess

from rest_framework.views import APIView
from django.shortcuts import render


# 数据首页
class usecam(APIView):
    def get(self,request):

        cmd_command = 'usecam.bat'
        subprocess.call(['start', 'cmd', '/c', cmd_command], shell=True)
        return render(request, "index.html")
# class TecIndex(APIView):
#     def get(self,request):
#         return render(request, "indextec.html")