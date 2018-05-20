# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from alchimest.serializers import validate_and_save
from alchimest.utils import copy_model_instance
from alchimest.models import *
from alchimest.serializers import *


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


class PackageControl(Control):
    model_name = 'Package'
    model = Package
    serializer = PackageSerializer


class GitLikeModelControl(Control):
    model_name = 'GitLikeModel'
    model = GitLikeModel
    serializer = GitLikeModelSerializer

    @classmethod
    def copy_normal_object(cls, old_obj, now_obj):
        pass

    @classmethod
    def copy_glm_object(cls, old_obj, now_obj):
        pass

    @classmethod
    def commit(cls, old_obj, now_obj):
        old_obj.latest = False
        old_obj.save()
        commit_id = old_obj.commit_id
        now_obj = copy_model_instance(now_obj)
        now_obj.latest = True
        now_obj.changed_from = commit_id
        now_obj.save()
        cls.copy_normal_object(old_obj, now_obj)
        cls.copy_glm_object(old_obj, now_obj)

    @classmethod
    def fork(cls, old_obj, now_obj):
        commit_id = old_obj.commit_id
        now_obj = copy_model_instance(now_obj)
        now_obj.latest = True
        now_obj.changed_from = commit_id
        now_obj.save()
        cls.copy_normal_object(old_obj, now_obj)
        cls.copy_glm_object(old_obj, now_obj)

    @classmethod
    def new(cls, old_obj, now_obj):
        now_obj = copy_model_instance(now_obj)
        now_obj.latest = True
        now_obj.changed_from = None
        now_obj.save()
        cls.copy_normal_object(old_obj, now_obj)
        cls.copy_glm_object(old_obj, now_obj)


class ImageControl(GitLikeModelControl):
    model_name = 'Image'
    model = Image
    serializer = ImageSerializer

    @classmethod
    def release_detail(cls, obj):
        if obj:
            return "{}:{}".format(obj.registry, obj.version)
        else:
            return ""

class ComponentControl(GitLikeModelControl):
    model_name = 'Component'
    model = Component
    serializer = ComponentSerializer

    @classmethod
    def copy_normal_object(cls, old_obj, now_obj):
        vols = Volume.objects.filter(component=old_obj)
        for vol in vols:
            vol.component = now_obj
            vol.pk = None
            vol.save()
        envs = Environment.objects.filter(component=old_obj)
        for env in envs:
            env.component = now_obj
            env.pk = None
            env.save()
        ports = Port.objects.filter(component=old_obj)
        for port in ports:
            port.component = now_obj
            port.pk = None
            port.save()
        affs = Affinity.objects.filter(component=old_obj)
        for aff in affs:
            aff.component = now_obj
            aff.pk = None
            aff.save()

    @classmethod
    def release_detail(cls, obj):
        if obj:
            vols = Volume.objects.filter(component=obj)
            envs = Environment.objects.filter(component=obj)
            ports = Port.objects.filter(component=obj)
            affs = Affinity.objects.filter(component=obj)
            return {
                'name': obj.name,
                'tag': obj.tag,
                'image': ImageControl.release_detail(obj.image),
                'host_network': obj.host_network,
                'mem_per_instance': obj.mem_per_instance,
                'cpu_per_instance': obj.cpu_per_instance,
                'environments': map(lambda x: EnvironmentControl.release_detail(x), envs),
                'volumes': map(lambda x: VolumeControl.release_detail(x), vols),
                'ports': map(lambda x: PortControl.release_detail(x), ports),
                'affinitys': map(lambda x: AffinityControl.release_detail(x), affs),
            }
        else:
            return {}

class PackageControl(GitLikeModelControl):
    model_name = 'Package'
    model = Package
    serializer = PackageSerializer

    @classmethod
    def copy_glm_object(cls, old_obj, now_obj):
        rels = ComponentRelease.objects.filter(in_package=old_obj)
        for rel in rels:
            ComponentRelease.objects.create(component=rel.component,
                                            in_package=now_obj,
                                            quantity=rel.quantity,
                                            examined = False)

    @classmethod
    def release_detail(cls, obj):
        if obj:
            comps = obj.components.all()
            comps_data = []
            for comp in comps:
                cr = ComponentRelease.objects.filter(component=comp, in_package=obj).first()
                comps_data.append({
                    'component': ComponentControl.release_detail(comp),
                    'quantity': cr.quantity,
                })
            return {
                'namespace': obj.namespace.name,
                'name': obj.name,
                'tag': obj.tag,
                'description': obj.description,
                'compents': comps_data,
            }
        else:
            return {}


class VolumeControl(Control):
    model_name = 'Volume'
    model = Volume
    serializer = VolumeSerializer

    @classmethod
    def release_detail(cls, obj):
        if obj:
            return {
                'pvc_name': obj.pvc_name,
                'container_path': obj.container_path,
                'mode': obj.mode,
                'type': obj.type,
                'requests_storage_G' : obj.requests_storage_G,
            }
        else:
            return {}


class PortControl(Control):
    model_name = 'Port'
    model = Port
    serializer = PortSerializer

    @classmethod
    def release_detail(cls, obj):
        if obj:
            return {
                'name': obj.name,
                'container_port': obj.container_port,
                'protocol': obj.protocol,
            }
        else:
            return {}

class EnvironmentControl(Control):
    model_name = 'Environment'
    model = Environment
    serializer = EnvironmentSerializer

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


class AffinityControl(Control):
    model_name = 'Affinity'
    model = Affinity
    serializer = AffinitySerializer

    @classmethod
    def release_detail(cls, obj):
        if obj:
            return {
                'type': obj.type,
                'to_component': obj.to_component.name,
            }
        else:
            return {}


class UniversallyUniqueVariableControl(Control):
    model_name = 'UniversallyUniqueVariable'
    model = UniversallyUniqueVariable
    serializer = UniversallyUniqueVariableSerializer


class UniversallyUniqueVariableClaimControl(Control):
    model_name = 'UniversallyUniqueVariableClaim'
    model = UniversallyUniqueVariableClaim
    serializer = UniversallyUniqueVariableClaimSerializer
