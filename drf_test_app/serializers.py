from rest_framework import serializers
from drf_test_app.models import TableWare, Dish
 
class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id','table_id','modified','name','is_deleted')
 
class TableWareSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableWare
        fields = ('id','contents')