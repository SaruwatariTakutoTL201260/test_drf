from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .serializers import DishSerializer, TableWareSerializer
from drf_test_app.models import TableWare, Dish
from rest_framework.authentication import TokenAuthentication

class ModelRetrieveView(viewsets.ModelViewSet):
    serializer_class = None
    model_class = None
    authentication_classes = [TokenAuthentication,]

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


class DishView(ModelRetrieveView):
    model_class = Dish
    serializer_class = DishSerializer
    basename = "dish"

class TableWareView(ModelRetrieveView):
    model_class = TableWare
    serializer_class = TableWareSerializer
    basename = "tableware"

# Create your views here.
