# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from django.shortcuts import get_list_or_404

from alchimest.controls import *
from alchimest.serializers import *

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def package_list(request):
    if request.method == 'GET':
        package = Package.objects.all()
        packageserializer = PackageSerializer(package, many=True)
        return Response(packageserializer.data)
    elif request.method == 'POST':
        packageserializer = PackageSerializer(data=request.data)
        if packageserializer.is_valid():
            packageserializer.save()
            return Response(packageserializer.data, status=status.HTTP_201_CREATED)
        return Response(packageserializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReleasesView(APIView):
    def get(self, request):
        data = PackageControl.list(**request.query_params)
        # result = [FurionClient(region=x).merge_region() for x in regions]
        # return json_response(result)
        return {'result ': data}


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all().order_by('commit_time')
    serializer_class = PackageSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def package_detail(request, namespace, name, tag):
    if request.method == 'GET':
        package = get_list_or_404(Package, namespace__name=namespace,
                                  name=name,
                                  tag=tag,
                                  approved=True)[0]
        return Response(data=PackageControl.release_detail(package))




