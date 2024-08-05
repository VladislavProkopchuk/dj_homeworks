from django.urls import path

from measurement.views import SensorView, MeasurementView, SensorListView, MeasurementUploadImage

urlpatterns = [
    path('sensors/', SensorListView.as_view()),
    path('sensors/<int:pk>/', SensorView.as_view(), name='sensor_id'),
    path('measurements/', MeasurementView.as_view()),
    path('measurements/upload/', MeasurementUploadImage.as_view()),
]
