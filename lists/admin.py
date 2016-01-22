from django.contrib import admin
from lists.models import EventList, Item, Pledge


@admin.register(EventList)
class EventListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at', 'active')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'deleted', 'created_at',
                    'reserved', 'modified_at')


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'item', 'amount', 'status', 'created_at',
                    'modified_at')

