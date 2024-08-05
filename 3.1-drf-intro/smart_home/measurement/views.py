# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from django.urls import reverse

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer


class SensorListView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def get_success_headers(self, data):
        return {'Location': reverse('sensor_id', kwargs={'pk': data.get('id', 1)})}

    # def post(self, request):
    #     name = request.data.get('name', '')
    #     description = request.data.get('description', '')
    #     if name:
    #         sensor = Sensor(name=name, description=description)
    #         sensor.save()
    #         message = {
    #             'message': 'sensor created',
    #             'Location': reverse('sensor_id', kwargs={'pk': sensor.id})
    #         }
    #         sts = status.HTTP_201_CREATED
    #     else:
    #         message = {'error': 'sensor name not set'}
    #         sts = status.HTTP_400_BAD_REQUEST
    #     return Response(message, status=sts)


class SensorView(RetrieveUpdateAPIView):
    serializer_class = SensorDetailSerializer
    queryset = Sensor.objects.all()

    # def get_queryset(self):
    #     """
    #     This view should return a list of all details for
    #     the sensor as determined by the id portion of the URL.
    #     """
    #     pk = self.kwargs['pk']
    #     sensor = Sensor.objects.filter(pk=pk)
    #     return sensor
    #
    # def patch(self, request, pk):
    #     name = request.data.get('name', '')
    #     description = request.data.get('description', '')
    #     sensor = Sensor.objects.get(pk=pk)
    #
    #     if not name and not description:
    #         message = {'error': f'blank parameters'}
    #         sts = status.HTTP_400_BAD_REQUEST
    #     else:
    #         sts = status.HTTP_200_OK
    #         message = {'message': ''}
    #         if name:
    #             old_name = sensor.name
    #             sensor.name = name
    #             message['message'] += f'Sensor name: {old_name} changed to {name}.'
    #         if description:
    #             old_description = sensor.description
    #             sensor.description = description
    #             message['message'] += f'Sensor description: {old_description} changed to {description}'
    #         sensor.save()
    #     return Response(message, status=sts)


class MeasurementView(ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    # parser_classes = [MultiPartParser, ]

    def get_success_headers(self, data):
        return {'Location': reverse('sensor_id', kwargs={'pk': data.get('sensor', 1)})}

    # def post(self, request):
    #     sensor_pk = request.data.get('sensor', '')
    #     sensor = Sensor.objects.get(pk=sensor_pk)
    #     temperature = request.data.get('temperature', '')
    #     image_sens = request.data.get('image_sens', '')
    #     measurement = Measurement(sensor=sensor, temperature=temperature, image_sens=image_sens)
    #     measurement.save()
    #     message = {'message': f'temperature {temperature} for sensor {sensor} added'}
    #     sts = status.HTTP_200_OK
    #
    #     return Response(message, status=sts)


class MeasurementUploadImage(CreateAPIView):
    def post(self, request):
        f = request.FILES
        img = f.get('image', '')
        if img:
            path_dir = os.path.join(
                Measurement.image_sens.field.upload_to,
                f'{img.name}'
            )
            path = default_storage.save(f'{path_dir}', ContentFile(img.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            sts = status.HTTP_200_OK
            message = {'Location': f'{path}'}
        else:
            sts = status.HTTP_400_BAD_REQUEST
            message = {'error': 'file has not found'}

        return Response(message, status=sts)
