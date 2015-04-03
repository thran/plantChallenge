from django.http import JsonResponse


def typehead(request):
    data = {"plants": [
        {
            "id": 7,
            "name": "Kytka hezka",
            "url": "http://seznam.cz",
            },
        {
            "id": 8,
            "name": "Kytka hnusna",
            "url": "http://google.cz",
            }
    ]}
    return JsonResponse(data)