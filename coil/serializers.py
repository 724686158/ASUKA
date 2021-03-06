# -*- coding: utf-8 -*-
from rest_framework import serializers

from coil.models import *


class FurionHookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurionHook


class AlchimestHookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlchimestHook


class DeploymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentRecord


def validate_and_save(serializer):
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data