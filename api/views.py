from gc import garbage
from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Bin, Garbage
from .serializers import GarbageSerializer, BinSerializer
from django.http import JsonResponse

@api_view(["GET"])
def get_garbage_data(request):
    bin_id = request.GET.get('bin_id', None)
    if bin_id:
        try: 
            bin = Bin.objects.get(id=bin_id)
        except:
            return Response({"message": "Invali Bin ID..."}, status=500)
        
        garbages = bin.garbage_set.all().order_by('-date')[:5]
        bin_serializer = BinSerializer(bin)
        garbage_serializer = GarbageSerializer(garbages, many=True)
        return Response({"bin": bin_serializer.data, "garbage": garbage_serializer.data})
    else:
        return Response({"message": "Bin Id Missing..."}, status=500)


@api_view(["POST", "GET"])
def add_garbage_data(request):
    if request.method == "GET":
        serializer = GarbageSerializer(data = request.GET)
    else:
        serializer = GarbageSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["GET"])
def get_bin_data(request):
    bins = Bin.objects.all()
    bin_data = [
        {
            'id': bin.pk,
            'name': bin.name,
            'location': bin.location,
            'lat': float(bin.latitude),
            'lng': float(bin.longitude),
            'garbage_level': float(bin.garbage_level),
            'moisture_status': bin.moisture_status,
            'isFull': bin.garbage_level > 90,
            'type': "red" if bin.moisture_status else "green",
        }
        for bin in bins
        if bin.latitude != None and bin.longitude != None
    ]
    return JsonResponse({'bins': bin_data})