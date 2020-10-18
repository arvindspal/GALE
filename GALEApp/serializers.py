from rest_framework import serializers
from .models import *


class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matches
        fields = '__all__'


class DeliveriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliveries
        fields = '__all__'
