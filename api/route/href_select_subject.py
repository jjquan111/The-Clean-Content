from rest_framework.views import APIView
from django.shortcuts import render



class ProHrefSelect(APIView):
    def get(self,request):
        return render(request, "select-subject.html")

class ProHrefSelect2(APIView):
    def get(self,request):
        return render(request, "select-subject2.html")

class ProHrefSelectTec(APIView):
    def get(self,request):
        return render(request, "select-subjecttec.html")

