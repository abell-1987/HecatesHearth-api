from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from HecatesHearthapi.models import Location, State


class LocationView(ViewSet):
    def list(self, request):
        locations = Location.objects.all().order_by("name")
        serializer = LocationSerializer(
            locations, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        location = Location.objects.get(pk=pk)
        serializer = LocationSerializer(location, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        name = request.data["name"].strip()
        city = request.data["city"].strip()
        description = request.data["description"].strip()
        history = request.data.get("history", "").strip()
        source_url = request.data.get("source_url", "").strip()
        is_famous = request.data.get("is_famous", False)
        state = State.objects.get(pk=request.data["state_id"])

        if isinstance(is_famous, str):
            is_famous = is_famous.lower() == "true"

        if is_famous and (not history or not source_url):
            return Response(
                {"message": "Famous locations require history and source URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if name.lower() != "private residence":
            location_exists = Location.objects.filter(
                name__iexact=name, city__iexact=city, state=state
            ).exists()

            if location_exists:
                return Response(
                    {"message": "Location already exists."},
                    status=status.HTTP_409_CONFLICT,
                )

        location = Location.objects.create(
            name=name,
            city=city,
            state=state,
            description=description,
            history=history,
            source_url=source_url,
            is_famous=is_famous,
            user=request.user,
        )

        serializer = LocationSerializer(location, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        location = Location.objects.get(pk=pk)

        if location.user != request.user:
            return Response(
                {"message": "You can only edit your own locations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        name = request.data["name"].strip()
        city = request.data["city"].strip()
        description = request.data["description"].strip()
        history = request.data.get("history", "").strip()
        source_url = request.data.get("source_url", "").strip()
        is_famous = request.data.get("is_famous", False)
        state = State.objects.get(pk=request.data["state_id"])

        if isinstance(is_famous, str):
            is_famous = is_famous.lower() == "true"

        if is_famous and (not history or not source_url):
            return Response(
                {"message": "Famous locations require history and source URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if name.lower() != "private residence":
            location_exists = (
                Location.objects.filter(
                    name__iexact=name, city__iexact=city, state=state
                )
                .exclude(pk=location.id)
                .exists()
            )

            if location_exists:
                return Response(
                    {"message": "Location already exists."},
                    status=status.HTTP_409_CONFLICT,
                )

        location.name = name
        location.city = city
        location.state = state
        location.description = description
        location.history = history
        location.source_url = source_url
        location.is_famous = is_famous
        location.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        location = Location.objects.get(pk=pk)

        if location.user != request.user:
            return Response(
                {"message": "You can only delete your own locations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if location.name.lower() != "private residence":
            return Response(
                {"message": "Only admin users may delete public or famous locations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        location.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("id", "abbreviation", "name")


class LocationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    creator_name = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    state = StateSerializer()

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
            "is_famous",
            "user_id",
            "creator_name",
            "is_owner",
            "created_at",
        )

    def get_creator_name(self, obj):
        first_initial = obj.user.first_name[:1]
        return f"{first_initial}. {obj.user.last_name}"

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request and obj.user == request.user
