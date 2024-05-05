from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination  # rest_framework分页模块
from rest_framework import serializers   # rest_framework序列化模块
from rest_framework.response import Response
from dal import models


# 序列化设置
class PagerSerialiser(serializers.ModelSerializer):

    class Meta:
        model = models.UserInfo
        fields = "__all__"

class PagerSerialiserTec(serializers.ModelSerializer):

    class Meta:
        model = models.TecInfo
        fields = "__all__"


class ProMessage(APIView):

    authentication_classes = []

    def post(self, request):
        username = str(request.data.get("username"))
        data = {}
        try:
            articles = models.UserInfo.objects.filter(username=username).order_by('id')
            pg = PageNumberPagination()
            pg.max_page_size = 200
            pg.page_size_query_param = "size"
            # 在数据库中获取分页的数据
            pager_roles = pg.paginate_queryset(queryset=articles, request=request, view=self)
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
            
            
class ProMessageTec(APIView):

    authentication_classes = []

    def post(self, request):
        username = str(request.data.get("username"))
        print('username:'+username)
        data = {}
        try:
            articles = models.TecInfo.objects.filter(username=username).order_by('id')
            pg = PageNumberPagination()
            pg.max_page_size = 200
            pg.page_size_query_param = "size"
            # 在数据库中获取分页的数据
            pager_roles = pg.paginate_queryset(queryset=articles, request=request, view=self)
            # 对分页数据进行序列化
            ser = PagerSerialiserTec(instance=pager_roles, many=True)
            data["code"] = 200
            data["data"] = ser.data
            return Response(data)
        except Exception as e:
            print(e)
            data["code"] = 444
            data["message"] = "请求异常"
            return JsonResponse(data)