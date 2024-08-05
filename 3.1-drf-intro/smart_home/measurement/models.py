from django.db import models
from django.utils.safestring import mark_safe


class Sensor(models.Model):
    name = models.CharField(max_length=32, verbose_name='Датчик')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        verbose_name='Датчик',
        related_name='measurements',
    )
    temperature = models.FloatField(verbose_name='Температура')
    measured_at = models.DateTimeField(auto_now=True, verbose_name='Дата измерения')
    image_sens = models.ImageField(
        max_length=255,
        blank=True,
        null=True,
        upload_to='uploads/',
        verbose_name='Изображение',
    )

    class Meta:
        verbose_name = 'Температура'
        verbose_name_plural = 'Температуры'

    def __str__(self):
        return f'{self.sensor} T={self.temperature}︒C, {self.measured_at}'

    @property
    def image_sens_preview(self):
        if self.image_sens:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.image_sens.url))
        return ""
