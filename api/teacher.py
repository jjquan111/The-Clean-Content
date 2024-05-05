from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination  # rest_framework分页模块
from rest_framework import serializers   # rest_framework序列化模块
from rest_framework.response import Response
from dal import models


# 序列化设置
class PagerSerialiser(serializers.ModelSerializer):

    class Meta:
        model = models.TecInfo
        fields = "__all__"
        depth = 3


class AllTecInfo(APIView):

    authentication_classes = []

    def post(self, request):
        username = str(request.data.get("username"))
        data = {}
        try:
            subjects = models.TecInfo.objects.all().order_by('id')

            pg = PageNumberPagination()
            pg.max_page_size = 200
            pg.page_size_query_param = "size"
            # 在数据库中获取分页的数据
            pager_roles = pg.paginate_queryset(queryset=subjects, request=request, view=self)
            # 对分页数据进行序列化
            ser = PagerSerialiser(instance=pager_roles, many=True)
            data["code"] = 200
            data["data"] = ser.data
            return Response(data)
        except Exception as e:
            print(e)
            data["code"] = 444
            data["message"] = "请求异常"
            return JsonResponse(data)

class TeachInfoBySubject(APIView):

    authentication_classes = []

    def post(self, request):
       
        subject_title = str(request.data.get("subject_title"))
        classid = str(request.data.get("classid"))
        print('subject_title'+subject_title)
        print('classid'+classid)
        data = {}
        try:
            subjects = models.TecInfo.objects.filter(subject_title__subject_title=subject_title).order_by('id')

            pg = PageNumberPagination()
            pg.max_page_size = 200
            pg.page_size_query_param = "size"
            # 在数据库中获取分页的数据
            pager_roles = pg.paginate_queryset(queryset=subjects, request=request, view=self)
            # 对分页数据进行序列化
            ser = PagerSerialiser(instance=pager_roles, many=True)
            data["code"] = 200
            data["data"] = ser.data
            return Response(data)
        except Exception as e:
            print(e)
            data["code"] = 444
            data["message"] = "请求异常"
            return JsonResponse(data)