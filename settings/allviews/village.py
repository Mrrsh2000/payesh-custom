"""ماژول آخرین وضیعت

این ماژول جهت اضافه کردن، ویرایش کردن و حذف کردن
آخرین وضیعت ها استفاده میشود.

"""
import json
import os
from pathlib import Path
from django.contrib import messages
from payesh.dynamic import *
from settings.views import *
import pandas


class VillageCreateView(SettingCreateView):
    model = Village
    template_name = None

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            count = 0

            if request.FILES.__len__:
                FileModel.objects.all().delete()
                newdoc = FileModel(excel_file=request.FILES['excel_file'])
                newdoc.save()
                path = str(Path(__file__).resolve().parent.parent.parent)
                excel_data_fragment = pandas.read_excel(path + newdoc.excel_file.url, sheet_name='Sheet1')

                village_list = excel_data_fragment.values
                for item in village_list:
                    try:
                        city, was_created = City.objects.get_or_create(title=item[0])
                        part, was_created = Part.objects.get_or_create(title=item[1], father_id=city.id)
                        town, was_created = Town.objects.get_or_create(title=item[2], father_id=part.id)
                        village, was_created = Village.objects.get_or_create(title=item[3],
                                                                             father_id=town.id)
                        if was_created:
                            count += 1
                    except:
                        pass
                messages.success(request, f'با موفقیت {str(count)} روستا ثبت شد')

        return super().post(request, *args, **kwargs)


class VillageUpdateView(SettingUpdateView):
    model = Village
    template_name = None

    def get_extra_context(self, context):
        context['city'] = self.get_object().father.father.father
        context['part'] = self.get_object().father.father
        return super().get_extra_context(context)


class VillageDatatableView(DynamicDatatableView):
    model = Village


class VillageDeleteView(DynamicDeleteView):
    model = Village
