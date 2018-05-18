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
        is_success = True
        error_detail = {}
        result_detail = {}
        # STATUS_TYPE = (
        #     ('PACKAGE_404', 'package 404 not found'),
        #     ('ENVIRONMENT_404', 'environment 404 not found'),
        #     ('ALCHIMEST_LOST', 'lost connect with alchimest'),
        #     ('FURION_LOST', 'lost connect with furion'),
        #     ('PACKAGE_ERROE', 'package has wrong variable declaration'),
        #     ('ENVIRONMENT_ERROR', 'environment has wrong variable declaration'),
        #     ('VARIABLE_NOT_MATCH', 'missing variable in the environment'),
        #     ('SUCCESS', 'success')
        # )

        furions = FurionHookControl.list()
        if len(furions) > 0:
            furion_ping_url = '{}/_ping/'.format(furions[0]['url'])
            furion_ping_res = requests.get(furion_ping_url)
            furion_ping_data = furion_ping_res.text
            if furion_ping_data == 'working properly':
                environment_url = '{}/environment_detail/{}/'.format(furions[0]['url'], environment_name)
                environment_res = requests.get(environment_url)
                environment_data = json.loads(environment_res.text)
                result_detail['environment_data'] = environment_data
            else:
                is_success = False
                error_detail['furion_connect_detail'] = 'lost connect with furion'
        else:
            is_success = False
            error_detail['furion_hock_detail'] = 'need at least one furion_hock'

        alchimests = AlchimestHookControl.list()
        if len(alchimests) > 0:

            alchimest_ping_url = '{}/_ping'.format(alchimests[0]['url'])
            alchimest_ping_res = requests.get(alchimest_ping_url)
            alchimest_ping_data = alchimest_ping_res.text
            if alchimest_ping_data == 'working properly':
                package_url = '{}/package_detail/{}/{}/{}/'.format(alchimests[0]['url'], package_namespace,
                                                                     package_name, package_tag)
                package_res = requests.get(package_url)
                package_data = package_res.text
                result_detail['package_data'] = package_data
            else:
                is_success = False
                error_detail['alchimest_connect_detail'] = 'lost connect with alchimest'
        else:
            is_success = False
            error_detail['alchimest_hock_detail'] = 'need at least one alchimest_hock'
        result_file_name = 'media/coil/{}_{}_{}_in_{}.json'.format(package_namespace,
                                                                      package_name, package_tag, environment_name)
        if is_success:
            result = {
                'is_success': is_success,
                'detail': result_detail,
            }
            os.system('echo "{}" > {}'.format(result, result_file_name))
        else:
            result = {
                'is_success': is_success,
                'detail': error_detail,
            }
            os.system('echo "{}" > {}'.format(result, result_file_name))
        file = open('{}'.format(result_file_name))
        history = {
            'user': request.user.id,
            'package_name': package_name,
            'package_namespace': package_namespace,
            'package_tag': package_tag,
            'environment_name': environment_name,
            'is_success': is_success,
            'result': File(file),
        }
        HistoryControl.save(history)
        return Response(data=result)
