# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from furion.serializers import validate_and_save
from furion.models import Environment
from furion.models import Variable
from furion.models import Service
from furion.models import Region
from furion.models import UseService
from furion.models import PartnerVariable
from furion.models import PartnerVariableInEnvironment
from furion.serializers import EnvironmentSerializer
from furion.serializers import VariableSerializer
from furion.serializers import ServiceSerializer
from furion.serializers import RegionSerializer
from furion.serializers import PartnerVariableSerializer
from furion.serializers import PartnerVariableInEnvironmentSerializer


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


class EnvironmentControl(Control):
    model_name = 'Environment'
    model = Environment
    serializer = EnvironmentSerializer

    @classmethod
    def release_detail(cls, obj):
        if obj:
            services = obj.services.all()
            services_data = []
            for service in services:
                us = UseService.objects.filter(service=service, in_environment=obj).first()
                services_data.append({
                    'service': ServiceControl.release_detail(service),
                    'exclusive': us.exclusive,
                })
            partner_variables = PartnerVariableInEnvironment.objects.filter(in_environment=obj)
            partner_variables_data = []
            for partner_variable in partner_variables:
                partner_variables_data.append(PartnerVariableInEnvironmentControl.release_detail(partner_variable))
            for service in services:
                us = UseService.objects.filter(service=service, in_environment=obj).first()
                services_data.append({
                    'service': ServiceControl.release_detail(service),
                    'exclusive': us.exclusive,
                })
            return {
                'name': obj.name,
                'region': RegionControl.release_detail(obj.region),
                'services': services_data,
                'partner_variables': partner_variables_data,
            }
        else:
            return {}


class RegionControl(Control):
    model_name = 'Region'
    model = Region
    serializer = RegionSerializer

    @classmethod
    def release_detail(cls, obj):
        if obj:
            return {
                'name': obj.name,
                'k8s_api_endpoint': obj.k8s_api_endpoint,
                'auth_token': obj.auth_token,
            }
        else:
            return {}


class VariableControl(Control):
    model_name = 'Variable'
    model = Variable
    serializer = VariableSerializer

    @classmethod
    def release_detail(cls, obj):
        if obj:
            return {
                'name': obj.name,
                'type': obj.type,
                'value': obj.value,
            }
        else:
            return {}


class ServiceControl(Control):
    model_name = 'Service'
    model = Service
    serializer = ServiceSerializer

    @classmethod
    def release_detail(cls, obj):
        if obj:
            vars = Variable.objects.filter(in_service=obj)
            return {
                'name': obj.name,
                'type': obj.type,
                'variable': map(lambda x: VariableControl.release_detail(x), vars),
            }
        else:
            return {}


class PartnerVariableControl(Control):
    model_name = 'PartnerVariable'
    model = PartnerVariable
    serializer = PartnerVariableSerializer


class PartnerVariableInEnvironmentControl(Control):
    model_name = 'PartnerVariable'
    model = PartnerVariableInEnvironment
    serializer = PartnerVariableInEnvironmentSerializer

    @classmethod
    def release_detail(cls, obj):
        if obj and obj.checked:
            return {
                "key": obj.partner_variable.key,
                "value": obj.value
            }
        else:
            return {}


