from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv

BUS_STATIONS = []


def _load_content_from_file(src: str) -> list:
    with open(src, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_num = int(request.GET.get('page', 1))
    if not BUS_STATIONS:
        BUS_STATIONS.extend(_load_content_from_file(settings.BUS_STATION_CSV))
    paginator = Paginator(BUS_STATIONS, 10)
    page = paginator.get_page(page_num)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
