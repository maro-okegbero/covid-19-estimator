from abc import ABC

from rest_framework import serializers


class CovidSerializers(serializers.Serializer):
    region = serializers.DictField(required=True)
    periodType = serializers.CharField(required=True, allow_blank=False)
    timeToElapse = serializers.IntegerField(required=True)
    reportedCases = serializers.IntegerField(required=True)
    population = serializers.IntegerField(required=True)
    totalHospitalBeds = serializers.IntegerField(required=True)


class CovidSerializersResponse(serializers.Serializer):
    data = serializers.DictField(required=True)
    impact = serializers.DictField(required=True)
    severeImpact = serializers.DictField(required=True)


