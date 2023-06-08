from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .serializers import DishSerializer, TableWareSerializer
from drf_test_app.models import TableWare, Dish
import logging

class ModelRetrieveView(viewsets.ModelViewSet):
    serializer_class = None
    model_class = None

    def retrieve(self,request,pk=None):
        queryset = self.model_class.objects.all()
        object = generics.get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(object)
        logging.basicConfig(filename='app.log', level=logging.INFO)
        logging.info(serializer)
        data = {
            self.model_class.__name__.lower(): serializer.data
        }
        if status.is_success(status.HTTP_200_OK):
            response_data = {
                "code": status.HTTP_200_OK,
                "message": "success",
                **data
            }
        elif status.is_client_error(status.HTTP_400_BAD_REQUEST):
            response_data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request"
            }
        elif status.is_client_error(status.HTTP_404_NOT_FOUND):
            response_data = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": "not found"
            }
        else:
            response_data = {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "server error"
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
