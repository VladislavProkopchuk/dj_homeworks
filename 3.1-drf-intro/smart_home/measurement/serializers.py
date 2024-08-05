from rest_framework import serializers

from rest_framework import serializers

from measurement.models import Sensor, Measurement


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class MeasurementSerializer(serializers.ModelSerializer):
    queryset = Sensor.objects.all()
    sensor = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'measured_at', 'image_sens']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
