from rest_framework.views import APIView
from django.shortcuts import render



class Subject(APIView):
    def get(self,request):
        return render(request, "pro-subject.html")
class Subject2(APIView):
    def get(self,request):
        return render(request, "pro-subject2.html")
class SubjectTec(APIView):
    def get(self,request):
        return render(request, "pro-subjecttel.html")