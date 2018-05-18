# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from coil.models import *
from coil.serializers import *


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


class HistoryControl(Control):
    model_name = 'History'
    model = History
    serializer = HistorySerializer


class FurionHookControl(Control):
    model_name = 'FurionHook'
    model = FurionHook
    serializer = FurionHookSerializer


class AlchimestHookControl(Control):
    model_name = 'AlchimestHook'
    model = AlchimestHook
    serializer = AlchimestHookSerializer
