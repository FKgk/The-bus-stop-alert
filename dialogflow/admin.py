from django.contrib import admin
from .models import User_infomation, Bus_cancel_list, Alarm


admin.site.register(User_infomation)
admin.site.register(Bus_cancel_list)
admin.site.register(Alarm)
'''
from .models import Pizza


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
'''

