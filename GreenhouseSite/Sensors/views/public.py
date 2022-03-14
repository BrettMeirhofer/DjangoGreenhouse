from .. import models
from django.shortcuts import render
from django.core import exceptions
import Plants


def gallery_view(request):
    images = models.DatedImage.objects.order_by("-date").filter(camera_id=1)
    return render(request, "admin/gallery.html", {'images': images})


def plants_view(request):
    plants = Plants.models.Plant.objects.order_by("-date_sprouted")
    return render(request, "admin/plants.html", {"plants": plants})


# Displays a page listing realtime information about the greenhouse
def greenhouse_status(request):
    try:
        latest_image = models.DatedImage.objects.latest("date").image.url
    except exceptions.ObjectDoesNotExist:
        latest_image = ""

    return render(request, "admin/dashboard.html", {'img_url': latest_image})


def graphs_page(request):
    return render(request, "admin/graphs_page.html")
