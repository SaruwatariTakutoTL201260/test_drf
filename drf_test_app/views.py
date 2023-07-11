from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets, generics, status, permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from .serializers import DishSerializer, TableWareSerializer
from drf_test_app.models import TableWare, Dish
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
import logging
from rest_framework.authtoken.models import Token

class ModelRetrieveView(viewsets.ModelViewSet):
    serializer_class = None
    model_class = None
    authentication_classes = [BasicAuthentication,]
    permission_classes = (permissions.IsAuthenticated,)

    # 一覧取得処理
    def list(self, request, *args, **kwargs):
        # クエリパラメータを取得
        query = request.query_params.get('id')
        # 条件に合うデータを一覧取得
        queryset = self.model_class.objects.all()
        if  query:
            queryset = queryset.filter(some_field=query)
        if queryset is None:
            # 対象のデータが存在しない場合404エラーを返す
            response_data = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": "not found"
            }
            return Response(response_data, status=response_data['code'])
        
        # 対象のmodelに合うようにデータをシリアライズ
        serializer = self.serializer_class(queryset, many=True)
        data = {
            self.model_class.__name__.lower(): serializer.data
        }
       
        # 正常に取得できた場合は200とデータを返す
        response_data = {
            "code": status.HTTP_200_OK,
            "message": "success",
            "data" : data[self.model_class.__name__.lower()]
        }
        return Response(response_data, status=response_data['code'])

    # 取得処理
    def retrieve(self,request,pk=None,format=None):
        if not pk.isnumeric():
            response_data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "bod request"
            }
            return Response(response_data, status=response_data['code'])
        queryset = self.model_class.objects.all()
        try:
            object = generics.get_object_or_404(queryset, pk=pk)
        except Http404:
            response_data = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": "not found"
            }
            return Response(response_data, status=response_data['code'])
        serializer = self.serializer_class(object)
        data = {
            self.model_class.__name__.lower(): serializer.data
        }
       
        response_data = {
            "code": status.HTTP_200_OK,
            "message": "success",
            **data
        }
        return Response(response_data, status=response_data['code'])

    # 登録処理
    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception = True)
        except ValidationError as e:
            response_data = {
                "code": 400,
                "message": e.detail
            }
            return Response(response_data, status=response_data['code'])

        serializer.save()
        response_data = {
            "code":status.HTTP_201_CREATED,
            "message": "create success",
            "data": serializer.data
        }
        return Response(response_data,status=response_data['code'])

    # 更新処理
    def update(self, request, pk=None):
        if not pk.isnumeric():
            response_data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request"
            }
            return Response(response_data, status=response_data["code"])
        try:
            object = self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            response_data = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": "not found"
            }
            return Response(response_data, status=response_data["code"])
        try:
            serializer = self.serializer_class(object, data=request.data)
            serializer.is_valid(raise_exception = True)
        except ValidationError as e:
            response_data = {
                "code": 400,
                "message": e.detail
            }
            return Response(response_data, status=response_data['code'])
        serializer.save()
        response_data = {
            "code": status.HTTP_200_OK,
            "message": "update success",
            "data": serializer.data
        }
        
        return Response(response_data, status=response_data["code"])

    def destroy(self, request, pk=None):
        if not pk.isnumeric():
            response_data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request"
            }
            return Response(response_data, status=response_data['code'])
        try:
            object = self.model_class.objects.get(pk=pk,is_deleted=False)
        except self.model_class.DoesNotExist:
            response_data = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": "not found"
            }
            return Response(response_data, status=response_data["code"])
        object.is_deleted = True
        object.save()
        response_data = {
            "code": status.HTTP_200_OK,
            "message": "delete success"
        }

        return Response(response_data,status=response_data['code'])

class DishView(ModelRetrieveView):
    # authentication_classes = [BasicAuthentication,]
    # permission_classes = (permissions.IsAuthenticated,)
    model_class = Dish
    serializer_class = DishSerializer
    basename = "dish"
    queryset = Dish.objects.all()

class TableWareView(ModelRetrieveView):
    model_class = TableWare
    serializer_class = TableWareSerializer
    basename = "tableware"
    queryset = TableWare.objects.all()

# Create your views here.
