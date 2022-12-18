from rest_framework import serializers
from app.models import Bin, Garbage


class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = '__all__'


class GarbageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garbage
        fields = ["bin_id", "garbage_level", "moisture_status", "date"]