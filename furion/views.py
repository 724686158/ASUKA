# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from furion.controls import EnvironmentControl
from furion.models import Environment

from furion.serializers import EnvironmentSerializer
from django.shortcuts import get_list_or_404

class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all().order_by('name')
    serializer_class = EnvironmentSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def environment_list(request):
    if request.method == 'GET':
        env = Environment.objects.all()
        environment_serializer = EnvironmentSerializer(env, many=True)
        return Response(environment_serializer.data)
    elif request.method == 'POST':
        environment_serializer = EnvironmentSerializer(data=request.data)
        if environment_serializer.is_valid():
            environment_serializer.save()
            return Response(environment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(environment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def environment_detail(request, environment):
    if request.method == 'GET':
        environment = get_list_or_404(Environment, name=environment)[0]
        return Response(data=EnvironmentControl.release_detail(environment))