from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate(self, data):
        if data['Employees_vu'] is not None:
            if data['Employees_vf'] > data['Employees_vu']:
                raise serializers.ValidationError("start of validity cant be after end of validity")
        return data

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class MandantSerializer(serializers.ModelSerializer):
    Currency = CurrencySerializer(many=False, read_only=True)
    class Meta:
        model = Mandant
        fields = ['Mandant_id','Currency']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    Product_unit = UnitSerializer(many=False, read_only=True)
    Mandant = MandantSerializer(many=False, read_only=True)
    Product_vf = serializers.DateTimeField(format="%d.%m.%Y")
    Product_vu = serializers.DateTimeField(format="%d.%m.%Y")
    Product_sppu_net = serializers.SerializerMethodField('get_Product_sppu_net')
    
    class Meta:
        model = Product
        fields = '__all__'

    def get_Product_sppu_net(self, obj):
        comma = obj.Product_sppu_net
        comma = str(comma)
        comma = comma.replace(","," ")
        comma = comma.replace(".",",")
        return '{}{}'.format( comma, obj.Mandant.Currency.Currency_symbol) 