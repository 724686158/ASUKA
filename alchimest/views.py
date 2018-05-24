# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from django.shortcuts import render
from django.shortcuts import get_list_or_404

from django.http import JsonResponse

from alchimest.controls import *
from alchimest.serializers import *

import os

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
    queryset = Package.objects.all()
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


@permission_classes((permissions.AllowAny,))
def glm_tree(request, type, name):
    return render(request, 'glm_tree/tree.html', {
        'type': type,
        'name': name,
    })


@permission_classes((permissions.AllowAny,))
def glm_tree_data(request, type, name):
    if type == 'package':
        obj = get_list_or_404(Package, name=name, latest=True)[0]
        return JsonResponse(PackageControl.get_tree_data(obj), safe=False)
    elif type == 'component':
        obj = get_list_or_404(Component, name=name, latest=True)[0]
        return JsonResponse(ComponentControl.get_tree_data(obj), safe=False)
    elif type == 'image':
        obj = get_list_or_404(Image, name=name, latest=True)[0]
        return JsonResponse(ImageControl.get_tree_data(obj), safe=False)
    else:
        return JsonResponse({}, safe=False)


@permission_classes((permissions.AllowAny,))
def dump_data(request, id):
    try:
        replica = get_object_or_404(Replica, id=id)
        ReplicaControl.dump_data(replica)
        return JsonResponse({'dump alchimest data': 'success'}, safe=False)
    except:
        return JsonResponse({'dump alchimest data': 'fail'}, safe=False)


@permission_classes((permissions.AllowAny,))
def load_data(request, id):
    try:
        replica = get_object_or_404(Replica, id=id)
        ReplicaControl.load_data(replica)
        return JsonResponse({'load alchimest data': 'success'}, safe=False)
    except:
        return JsonResponse({'load alchimest data': 'fail'}, safe=False)




