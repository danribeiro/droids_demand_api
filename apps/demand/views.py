from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DemandCreateSerializer, UfSerializer, CitySerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import generics, response, status
from .models import Demand, Uf, City, Contact, Address


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'uf'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(**kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class UfListView(generics.ListAPIView, ListModelMixin):
    queryset = Uf.objects.all()
    serializer_class = UfSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class DemandCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = DemandCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return response.Response(status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)
