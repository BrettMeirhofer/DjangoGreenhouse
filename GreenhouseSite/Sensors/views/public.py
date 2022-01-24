from .. import models
from django.shortcuts import render
from django.core import exceptions


def gallery_view(request):
    urls = [x.image.url for x in models.DatedImage.objects.order_by("-date")]
    return render(request, "admin/gallery.html", {'url_list': urls})


# Displays a page listing realtime information about the greenhouse
def greenhouse_status(request):
    try:
        latest_image = models.DatedImage.objects.latest("date").image.url
    except exceptions.ObjectDoesNotExist:
        latest_image = ""

    return render(request, "admin/dashboard.html", {'img_url': latest_image})
