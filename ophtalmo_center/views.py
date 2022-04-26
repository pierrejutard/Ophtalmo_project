from django.shortcuts import render, get_object_or_404
from ophtalmo_center.models import ophtalmo_center

def ophtalmo_center_index(request):
    ophtalmo_centers = ophtalmo_center.objects.all()
    return render(request, 'ophtalmo_center/ophtalmo_center_index.html', context={"ophtalmo_centers":ophtalmo_centers})

def ophtalmo_center_details(request, slug):
    ophtalmo_center_detail = get_object_or_404 (ophtalmo_center, slug=slug)
    return render(request, 'ophtalmo_center/ophtalmo_center_details.html', context={"ophtalmo_center":ophtalmo_center_detail})