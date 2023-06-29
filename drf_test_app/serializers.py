from rest_framework import serializers
from drf_test_app.models import TableWare, Dish, User
 
class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id','table_id','modified','name','is_deleted')
 
class TableWareSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableWare
        fields = ('id','contents','is_deleted')

class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('code','message')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name')