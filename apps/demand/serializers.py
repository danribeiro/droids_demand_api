from django.urls import path, include
from django.conf import settings
from rest_framework import routers, serializers, viewsets
from .models import Demand, Uf, City, Address, Contact
from rest_framework.utils.field_mapping import (
    ClassLookupDict, get_field_kwargs, get_nested_relation_kwargs,
    get_relation_kwargs, get_url_kwargs
)
from rest_framework.utils import html, model_meta, representation


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
    uf_id = serializers.IntegerField(write_only=True)
    city_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Address
        fields = '__all__'


class DemandCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=True)
    contacts = ContactSerializer(many=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Demand
        fields = [
            'description',
            'address',
            'contacts'
        ]
        read_only_fields = ['author', 'status']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        contacts_data = validated_data.pop('contacts')
        demand = Demand.objects.create(**validated_data)
        Address.objects.create(demand=demand, **address_data)
        for contact_data in contacts_data:
            Contact.objects.create(demand=demand, **contact_data)
        return demand

    def update(self, instance, validated_data):
        contacts_data = validated_data.get('contacts')
        demand = Demand.objects.filter(id=instance.id).update(
            description=validated_data['description'])
        address = Address.objects.filter(id=instance.address.id).update(
            **validated_data.get('address'))

        Contact.objects.filter(demand=instance.id).delete()
        for contact_data in contacts_data:
            Contact.objects.create(demand=instance, **contact_data)
        return demand


class DemandReadOnlySerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Demand
        fields = [
            'id',
            'description',
            'author',
            'address',
            'contacts',
            'status'
        ]


class DemandUpdateStatusSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)
    status = serializers.BooleanField(required=True)

    class Meta:
        model = Demand
        fields = [
            'id',
            'status'
        ]
