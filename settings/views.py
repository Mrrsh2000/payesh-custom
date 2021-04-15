from django.db.models import Q

from payesh.dynamic import DynamicCreateView, DynamicUpdateView
from payesh.dynamic_api import DynamicModelApi
from settings.serializers import *


class SettingCreateView(DynamicCreateView):
    template_name = 'settings/dynamic/create.html'

    def get_deleteURL(self):
        return '/api/v1/{0}/0'.format(str(self.model._meta).split('.')[1])

    def get_datatableURL(self):
        return '/api/v1/{0}/datatable/'.format(str(self.model._meta).split('.')[1])

    def get_createURL(self):
        return '/api/v1/{0}/'.format(str(self.model._meta).split('.')[1])

    def get_context_data(self, *args, **kwargs):
        res = super().get_context_data(*args, **kwargs)
        res['createURL'] = self.get_createURL()
        res['updateApiURL'] = self.get_createURL()
        return res


class SettingUpdateView(DynamicUpdateView):
    template_name = 'settings/dynamic/update.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context_pk = self.kwargs['pk']
        context['context_pk'] = context_pk
        context['updateApiURL'] = '/api/v1/{0}/{1}/'.format(str(self.model._meta).split('.')[1], context_pk)
        context['successURL'] = self.get_success_url()
        return context


class CityViewSet(DynamicModelApi):
    model = City
    queryset = City.objects.all()
    serializer_class = CitySerializer
    custom_perms = {
        'retrieve': 'can_city',
        'create': 'can_city',
        'update': 'can_city',
        'destroy': 'can_city',
        'list': 'can_city'
    }

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__icontains=search))
        return qs


class PartViewSet(DynamicModelApi):
    model = Part
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    custom_perms = {
        'retrieve': 'can_part',
        'create': 'can_part',
        'update': 'can_part',
        'destroy': 'can_part',
        'list': 'can_part'
    }

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__icontains=search))
        return qs


class TownViewSet(DynamicModelApi):
    model = Town
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    custom_perms = {
        'retrieve': 'can_town',
        'create': 'can_town',
        'update': 'can_town',
        'destroy': 'can_town',
        'list': 'can_town'
    }

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__icontains=search))
        return qs


class VillageViewSet(DynamicModelApi):
    model = Village
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    custom_perms = {
        'retrieve': 'can_village',
        'create': 'can_village',
        'update': 'can_village',
        'destroy': 'can_village',
        'list': 'can_village'
    }

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__icontains=search))
        return qs
