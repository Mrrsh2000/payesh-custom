from payesh.dynamic import api_error_creator
from payesh.dynamic_api import DynamicSerializer
from settings.models import *


class CitySerializer(DynamicSerializer):
    class Meta:
        model = City
        extra_kwargs = api_error_creator(City, ['title'],
                                         blank_fields=[],
                                         required_fields=['title'])
        fields = ['id', 'title']


class PartSerializer(DynamicSerializer):
    class Meta:
        model = Part
        extra_kwargs = api_error_creator(Part, ['title', 'father'],
                                         blank_fields=[],
                                         required_fields=['title', 'father'])
        fields = ['id', 'title', 'father']


class TownSerializer(DynamicSerializer):
    class Meta:
        model = Town
        extra_kwargs = api_error_creator(Town, ['title', 'father'],
                                         blank_fields=[],
                                         required_fields=['title', 'father'])
        fields = ['id', 'title', 'father']


class VillageSerializer(DynamicSerializer):
    class Meta:
        model = Village
        extra_kwargs = api_error_creator(Village, ['title', 'father'],
                                         blank_fields=[],
                                         required_fields=['title', 'father'])
        fields = ['id', 'title', 'father']
