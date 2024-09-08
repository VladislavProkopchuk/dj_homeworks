from django.contrib import admin
from django.utils.safestring import mark_safe

from logistic.models import Product, Stock, StockProduct


class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    inlines = [StockProductInline, ]
