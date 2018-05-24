# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from django.core.files import File
from django.shortcuts import get_list_or_404

from coil.controls import *
from coil.serializers import *
import requests
import json
import os

def dump_data():
    try:
        os.system('python manage.py dumpdata coil > media/coil/coil_data.json')
        return {'dump coil data': 'success'}
    except:
        return {'dump coil data': 'fail'}


def load_data():
    try:
        os.system('python manage.py loaddata media/coil/coil_data.json')
        return {'load coil data': 'success'}
    except:
        return {'load coil data': 'fail'}


@permission_classes((permissions.AllowAny,))
class LinkView(APIView):

    def get(self, request, environment_name, package_namespace, package_name, package_tag):
        obj = DeploymentRecord()
        obj.environment_name = environment_name
        obj.package_namespace = package_namespace
        obj.package_name = package_name
        obj.package_tag = package_tag
        obj.user = request.user
        result = DeploymentRecordControl.create_deployment_record_and_get_result(obj)
        return Response(data=result)
