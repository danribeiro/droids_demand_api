from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin
)
from rest_framework import generics, response, status
from .models import User
from rest_framework.exceptions import APIException


class UserView(APIView):

    def post(self, request, *args, **kwargs):
        if request.user.profile == 2:
            detail = {
                "detail": "Não é permitido para usuários de perfil anunciante"}
            return response.Response(data=detail, status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.profile == 1 or request.user.is_superuser:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    serializer.save()
                except Exception:
                    detail = {
                        "detail": "Já existe um usuário com esse email %s" % request.data.get('email')}
                    return response.Response(data=detail, status=status.HTTP_404_NOT_FOUND)
                return response.Response(status=status.HTTP_201_CREATED)
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
