from rest_framework.views import APIView
from django.shortcuts import render


# 修改密码跳转
class ProUpdatePwd(APIView):
    def get(self,request):
        return render(request, "pro_updatepwd.html")
class ProUpdatePwdTec(APIView):
    def get(self,request):
        return render(request, "pro_updatepwdtec.html")