from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from HecatesHearthapi.models import HauntingType


class HauntingTypeView(ViewSet):
    def list(self, request):
        haunting_types = HauntingType.objects.all().order_by("name")
        serializer = HauntingTypeSerializer(haunting_types, many=True)
        return Response(serializer.data)


class HauntingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HauntingType
        fields = ("id", "name")
