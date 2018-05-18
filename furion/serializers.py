# -*- coding: utf-8 -*-
from rest_framework import serializers
from furion.models import Region
from furion.models import Variable
from furion.models import Service
from furion.models import Environment


def validate_and_save(serializer):
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region


