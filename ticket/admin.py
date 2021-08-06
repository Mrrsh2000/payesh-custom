from django.contrib import admin

# Register your models here.
from ticket.models import Message, Ticket

admin.site.register(Message)
admin.site.register(Ticket)
