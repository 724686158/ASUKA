# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from coil.models import *
from coil.serializers import *
from rest_framework.response import Response
from django.core.files import File
import requests
import json
import os

class Control(object):
    model_name = None
    model = None
    serializer = None

    @classmethod
    def _pre_save(cls, data, **args):
        return data

    @classmethod
    def save(cls, data, **args):
        """Save input data to db after validate."""
        resp = validate_and_save(cls.serializer(data=cls._pre_save(data, **args)))
        cls._post_save(resp)
        return resp

    @classmethod
    def _post_save(cls, data):
        """After db save hook."""
        return

    @classmethod
    def get_object(cls, **filters):
        return get_object_or_404(cls.model, **filters)

    @classmethod
    def get_info(cls, **filters):
        return cls._format(cls.get_object(**filters))

    @classmethod
    def _format(cls, obj):
        return cls.get_origin_info(obj)

    @classmethod
    def get_origin_info(cls, obj):
        """Simple model_to_dict """
        return cls.serializer(obj).data

    @classmethod
    def list(cls, **args):
        return [cls._format(x) for x in cls._get_list(**args)]

    @classmethod
    def _get_list(cls, **args):
        return cls.model.objects.filter(**args)

    @classmethod
    def delete(cls, **args):
        try:
            obj = cls.get_object(**args)
        except Exception:
            return
        try:
            obj.delete()
        except Exception as e:
            msg = "Delete {} failed. | filters={}, err={}".format(cls.model_name, args, e)
            raise Exception('resource_state_conflict', message=msg)

    @classmethod
    def update(cls, data, **args):
        try:
            if "_state" in data:
                del data['_state']
            else:
                data = cls._pre_update(data, **args)
            # LOG.debug("Get update data for {} | {}".format(cls.model_name, data))
            cls.model.objects.filter(**args).update(**data)
        except Exception as e:
            # LOG.error("Update fail. stack: {} {}".format(e, traceback.format_exc()))
            raise Exception('invalid_args', message=str(e))

    @classmethod
    def _pre_update(cls, data, **args):
        return data


class DeploymentRecordControl(Control):
    model_name = 'DeploymentRecord'
    model = DeploymentRecord
    serializer = DeploymentRecordSerializer



    @classmethod
    def link_and_create_histoy(cls, obj):
        package_namespace = obj.package_namespace
        package_name = obj.package_name
        package_tag = obj.package_tag
        environment_name = obj.environment_name
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
                package_data = json.loads(package_res.text)
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
        obj.is_success = is_success
        obj.result = File(file)
        obj.save()


class FurionHookControl(Control):
    model_name = 'FurionHook'
    model = FurionHook
    serializer = FurionHookSerializer


class AlchimestHookControl(Control):
    model_name = 'AlchimestHook'
    model = AlchimestHook
    serializer = AlchimestHookSerializer
