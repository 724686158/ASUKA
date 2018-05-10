# -*- coding: utf-8 -*-
from rest_framework import serializers

from alchimest.models import Namespace
from alchimest.models import Image
from alchimest.models import Component
from alchimest.models import Package
from alchimest.models import Volume
from alchimest.models import Port
from alchimest.models import Environment
from alchimest.models import Affinity
from alchimest.models import Employee
from alchimest.models import GitLikeModel


class NamespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Namespace


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package


class VolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume


class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment


class AffinitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Affinity


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee


class GitLikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitLikeModel


def validate_and_save(serializer):
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data
