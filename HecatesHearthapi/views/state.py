from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from HecatesHearthapi.models import State


class StateView(ViewSet):
    def list(self, request):
        states = State.objects.all().order_by("abbreviation")
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("id", "abbreviation", "name")
