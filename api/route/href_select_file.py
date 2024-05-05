import os

from django.http import HttpResponse
from rest_framework.views import APIView
from django.shortcuts import render



class FileUpdate(APIView):
    def get(self,request):
        return render(request, "file-update.html")

    def post(self,request):
        print("FILES:", request.FILES)
        print("POST:", request.POST)
        myFile = request.FILES.get("upload_file_form", None)
        if not myFile:
            return HttpResponse("no files for upload")
        # 打开特定的文件进行二进制的写操作
        f = open('upload.mp4', "wb+")
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()
        os.system(r'conda activate tf3srgan & cd C:\2023.01\lift\code\yolo & python predict.py & copy img_out\output.mp4 C:\2023.01\lift\code\liftweb\static\output.mp4 & copy logvisual.log C:\2023.01\lift\code\liftweb\static\logvisual.html')

        return HttpResponse("<script>window.location.replace('http://127.0.0.1:8000/href/FileUpdate/')</script>")

class ScreenShow(APIView):
    def get(self,request):
        return render(request, "screen.html")