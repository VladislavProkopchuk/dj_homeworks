from django.contrib import admin

from advertisements.models import Advertisement, FavoriteAdvertisement


@admin.register(Advertisement)
class StockAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


@admin.register(FavoriteAdvertisement)
class FavoriteAdvertisementAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
