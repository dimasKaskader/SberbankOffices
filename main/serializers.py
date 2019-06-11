from rest_framework import serializers
from .models import *


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ('latitude', 'longitude', 'is_deleted')


class Branch1Serializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ('latitude', 'longitude', 'is_deleted', 'code', 'city', 'street', 'building')


class CandidateSerializer(serializers.ModelSerializer):
    pop = serializers.IntegerField()
    density = serializers.FloatField()
    count = serializers.IntegerField()
    rating = serializers.FloatField()
    city = serializers.CharField()

    class Meta:
        model = Branch
        fields = ('pop', 'density', 'count', 'rating', 'city')