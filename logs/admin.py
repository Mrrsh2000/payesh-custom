from django.contrib import admin

# Register your models here.
from logs.models import *

admin.site.register(Log)
