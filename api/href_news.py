from rest_framework.views import APIView
from django.shortcuts import render
from dal import models

# # 数据首页
# class news(APIView):
#     def get(self,request):
#         return render(request, "news.html")
# # class TecIndex(APIView):
# #     def get(self,request):
# #         return render(request, "indextec.html")


from django.shortcuts import render

class news_List(APIView):
    def news_list(self):
        news = models.news.objects.all()
        return render('news.html', {'news': news})

