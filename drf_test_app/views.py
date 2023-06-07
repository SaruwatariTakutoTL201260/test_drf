from django.shortcuts import render
from rest_framework import viewsets
from .serializers import DishSerializer, TableWareSerializer
from drf_test_app.models import TableWare, Dish

class DishView(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class TableWareView(viewsets.ModelViewSet):
    queryset = TableWare.objects.all()
    serializer_class = TableWareSerializer

# Create your views here.
