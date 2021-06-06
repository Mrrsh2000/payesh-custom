from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.views import View
from rest_framework import permissions
from rest_framework.views import APIView

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

