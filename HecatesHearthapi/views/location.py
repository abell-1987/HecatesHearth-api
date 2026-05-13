from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from HecatesHearthapi.models import Location


class LocationView(ViewSet):
    def list(self, request):
        locations = Location.objects.all().order_by("name")
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        location = Location.objects.get(pk=pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def create(self, request):
        location = Location.objects.create(
            name=request.data["name"],
            city=request.data["city"],
            state=request.data["state"],
            description=request.data["description"],
            history=request.data.get("history", ""),
            source_url=request.data.get("source_url", ""),
            user=request.user,
        )
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        location = Location.objects.get(pk=pk)

        if location.user != request.user:
            return Response(
                {"message": "You can only edit your own locations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        location.name = request.data["name"]
        location.city = request.data["city"]
        location.state = request.data["state"]
        location.description = request.data["description"]
        location.history = request.data.get("history", "")
        location.source_url = request.data.get("source_url", "")
        location.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        location = Location.objects.get(pk=pk)

        if location.user != request.user:
            return Response(
                {"message": "You can only delete your own locations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        location.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class LocationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "city",
            "state",
            "description",
            "history",
            "source_url",
            "user_id",
            "is_owner",
            "created_at",
        )

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request and obj.user == request.user
