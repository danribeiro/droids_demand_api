from django.urls import path, include
from django.conf import settings
from rest_framework import routers, serializers, viewsets
from .models import Demand, Uf, City, Address, Contact


class CitySerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return {"id": value.id, "name": value.name}

    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)
    uf = serializers.RelatedField(required=False, read_only=True)

    class Meta:
        model = City
        fields = '__all__'


class UfSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)
    uf = serializers.CharField(required=False)

    class Meta:
        model = Uf
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            'name',
            'phone'
        ]


class AddressSerializer(serializers.ModelSerializer):
    # uf = UfSerializer(read_only=True)
    uf_id = serializers.IntegerField(write_only=True)
    # city = CitySerializer(read_only=True)
    city_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Address
        fields = '__all__'


class DemandCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    contact = ContactSerializer(many=True)

    class Meta:
        model = Demand
        fields = [
            'description',
            'address',
            'contact'
        ]
        read_only_fields = ['author', 'status']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        contacts_data = validated_data.pop('contact')
        demand = Demand.objects.create(**validated_data)
        Address.objects.create(demand=demand, **address_data)
        for contact_data in contacts_data:
            Contact.objects.create(demand=demand, **contact_data)
        return demand
