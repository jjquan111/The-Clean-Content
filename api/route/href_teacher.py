from rest_framework.views import APIView
from django.shortcuts import render



class Subject(APIView):
    def get(self,request):
        return render(request, "pro-teacher.html")
