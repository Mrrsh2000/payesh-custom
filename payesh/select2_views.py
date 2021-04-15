from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.views import View
from rest_framework import permissions
from rest_framework.views import APIView

from data.models import CustomWaterNeed, ReplaceTanker, HouseSourceNeed, WaterNetworkNeed, Season
from settings.models import *
from user.models import User


class Select2(View):
    """
    کلاس اصلی select2 است

    این کلاس برای صرفه جویی در زمان برای فیلد های select که اطلاعاتشان
    را از پایگاه داده میخانند ایجاد شده است و از Ajax استفاده میکند و همچنین
    قابلیت جستجو به کاربر میدهد
    """
    model = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.per_page = 20
        self.id = 'id'
        self.text = 'title'

    def get_model(self):
        if self.model is None:
            thing = User.objects.all()
            return thing
        else:
            return self.model

    def get(self, request):
        page = request.GET.get('page', 1)
        search = request.GET.get('search')

        thing = self.get_model()

        if search is not None and len(search.strip()) > 0:
            thing = thing.filter(**{self.text + '__contains': search})
        if self.id != 'id':
            thing = thing.annotate(id=F(self.id), text=self.get_text())
        else:
            thing = thing.annotate(text=self.get_text())
        thing = thing.values('id', 'text')
        paginator = Paginator(thing, self.per_page)
        results = paginator.page(int(page)).object_list
        results_bitten = list(results)
        return JsonResponse({
            'results': results_bitten,
            "pagination": {
                "more": paginator.page(page).has_next()
            }
        }, safe=False)

    def get_text(self):
        return F(self.text)


class DynamicSelect2(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    کلاس اصلی select2 است

    این کلاس برای صرفه جویی در زمان برای فیلد های select که اطلاعاتشان
    را از پایگاه داده میخانند ایجاد شده است و از Ajax استفاده میکند و همچنین
    قابلیت جستجو به کاربر میدهد
    """
    model = None
    qs = None
    id = 'id'
    text = 'title'
    per_page = 20
    string = False

    def get_model(self):
        return self.model.objects.all() if not self.qs else self.qs

    def get(self, request):
        page = request.GET.get('page', 1)
        search = request.GET.get('search')

        thing = self.get_model()

        if search is not None and len(search.strip()) > 0:
            thing = thing.filter(**{self.text + '__contains': search})
        if self.string:
            thing = thing.values('title')
        else:
            if self.id != 'id':
                thing = thing.annotate(id=F(self.id), text=self.get_text())
            else:
                thing = thing.annotate(text=self.get_text())
            thing = thing.values('id', 'text')

        paginator = Paginator(thing, self.per_page)
        results = paginator.page(int(page)).object_list
        results_bitten = list(results)
        if self.string:
            results_bitten = list(map(lambda x: {'id': x['title'], 'text': x['title']}, results_bitten))
        return JsonResponse({
            'results': results_bitten,
            "pagination": {
                "more": paginator.page(page).has_next()
            }
        })

    def get_text(self):
        return F(self.text)


class CitySelect2(DynamicSelect2):
    model = City


class PartSelect2(DynamicSelect2):

    def get_model(self):
        if self.request.GET.get('father') != '0':
            qs = Part.objects.filter(father__id=self.request.GET.get('father'))
        elif not self.request.GET.get('father'):
            return Part.objects.none()
        else:
            self.per_page = 100000
            qs = Part.objects.all()
        return qs


class TownSelect2(DynamicSelect2):
    def get_model(self):
        if self.request.GET.get('father') != '0':
            qs = Town.objects.filter(father__id=self.request.GET.get('father'))
        elif not self.request.GET.get('father'):
            return Town.objects.none()
        else:
            self.per_page = 100000
            qs = Town.objects.all()
        return qs


class VillageSelect2(DynamicSelect2):

    def get_model(self):
        if self.request.GET.get('father') != '0':
            qs = Village.objects.filter(father__id=self.request.GET.get('father'))
        elif not self.request.GET.get('father'):
            return Village.objects.none()
        else:
            self.per_page = 100000
            qs = Village.objects.all()
        return qs


class ExcelFilterSelect2(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_model(self):
        qs = Village.objects.filter(Waters=None)
        if self.request.data.get('village__father__father__father__title'):
            qs = qs.filter(father__father__father__title__icontains=self.request.data.get(
                'village__father__father__father__title'))
        if self.request.data.get('village__father__father__title'):
            qs = qs.filter(father__father__title__icontains=self.request.data.get(
                'village__father__father__title'))
        if self.request.data.get('village__father__title'):
            qs = qs.filter(father__title__icontains=self.request.data.get(
                'village__father__title'))
        if self.request.data.get('village__title'):
            get = self.request.data.get('village__title')
            qs = qs.filter(title__icontains=get)

        return qs

    def get_text(self, obj):
        return obj.father.father.father.title + ' > ' + obj.father.father.title + ' > ' + obj.father.title + ' > ' + obj.title

    def post(self, request):
        return JsonResponse({
            'values': [self.get_text(obj) for obj in self.get_model()]
        })


class SeasonSelect2(DynamicSelect2):

    def get_model(self):
        bahar, x = Season.objects.get_or_create(title='بهار')
        tabestan, x = Season.objects.get_or_create(title='تابستان')
        paeez, x = Season.objects.get_or_create(title='پاییز')
        zemestan, x = Season.objects.get_or_create(title='زمستان')
        return Season.objects.all()


class ReplaceTankerStrSelect2(DynamicSelect2):
    model = ReplaceTanker
    string = True


class CustomWaterNeedStrSelect2(DynamicSelect2):
    model = CustomWaterNeed
    string = True


class HouseSourceNeedStrSelect2(DynamicSelect2):
    model = HouseSourceNeed
    string = True


class WaterNetworkNeedStrSelect2(DynamicSelect2):
    model = WaterNetworkNeed
    string = True
