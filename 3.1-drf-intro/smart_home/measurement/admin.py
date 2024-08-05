from django.contrib import admin
from django.utils.safestring import mark_safe

from measurement.models import Sensor, Measurement


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    readonly_fields = ('image_sens_preview',)

    def image_sens_preview(self, obj):
        return obj.image_sens_preview

    image_sens_preview.short_description = 'Image_sens Preview'
    image_sens_preview.allow_tags = True
