from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import (
    DemandCreateSerializer,
    UfSerializer,
    CitySerializer,
    DemandReadOnlySerializer,
    DemandUpdateStatusSerializer
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin
)
from rest_framework import generics, response, status
from .models import Demand, Uf, City, Contact, Address


class CityListView(generics.ListAPIView):
    """
    A simple view for listing cities by uf_id
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'uf'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(**kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class UfListView(generics.ListAPIView):
    """
    A simple view for listing uf
    """
    queryset = Uf.objects.all()
    serializer_class = UfSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class DemandCreateView(APIView):
    """
    A view for create demand
    """

    def post(self, request, *args, **kwargs):
        serializer = DemandCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return response.Response(status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)


class DemandListView(generics.ListAPIView):
    """
    A simple view for listing demands
    """
    queryset = Demand.objects.all()
    serializer_class = DemandReadOnlySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class DemandUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for update demand
    """
    serializer_class = DemandCreateSerializer
    queryset = Demand.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.id != request.user.id:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DemandStatusUpdateView(generics.UpdateAPIView):
    """
    A view for update demand status only
    """
    serializer_class = DemandUpdateStatusSerializer
    queryset = Demand.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author.id != request.user.id:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
