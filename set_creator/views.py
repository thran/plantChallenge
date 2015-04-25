from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from flowerchecker.models import Answer, Flowers, Request, Imagefile, ImportedPlants, PlantType


def test(request):
    return render_to_response('sets/test.html')