from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from HecatesHearthapi.models import Story, Location, HauntingType, State


class StoryView(ViewSet):
    def list(self, request):
        stories = Story.objects.all().order_by("-created_at")
        serializer = StorySerializer(stories, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        story = Story.objects.get(pk=pk)
        serializer = StorySerializer(story, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        location = Location.objects.get(pk=request.data["location_id"])

        story = Story.objects.create(
            title=request.data["title"],
            content=request.data["content"],
            location=location,
            user=request.user,
        )

        haunting_type_ids = request.data.get("haunting_type_ids", [])
        story.haunting_types.set(haunting_type_ids)

        serializer = StorySerializer(story, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        story = Story.objects.get(pk=pk)

        if story.user != request.user:
            return Response(
                {"message": "You can only edit your own stories."},
                status=status.HTTP_403_FORBIDDEN,
            )

        location = Location.objects.get(pk=request.data["location_id"])

        story.title = request.data["title"]
        story.content = request.data["content"]
        story.location = location
        story.save()

        haunting_type_ids = request.data.get("haunting_type_ids", [])
        story.haunting_types.set(haunting_type_ids)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        story = Story.objects.get(pk=pk)

        if story.user != request.user:
            return Response(
                {"message": "You can only delete your own stories."},
                status=status.HTTP_403_FORBIDDEN,
            )

        story.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class HauntingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HauntingType
        fields = ("id", "name")


class StoryStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("id", "abbreviation", "name")


class StoryLocationSerializer(serializers.ModelSerializer):
    state = StoryStateSerializer()
    user_id = serializers.IntegerField(source="user.id")
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "city",
            "state",
            "user_id",
            "creator_name",
            "created_at",
        )

    def get_creator_name(self, obj):
        first_initial = obj.user.first_name[:1]
        return f"{first_initial}. {obj.user.last_name}"


class StoryPhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class StorySerializer(serializers.ModelSerializer):
    location = StoryLocationSerializer()
    haunting_types = HauntingTypeSerializer(many=True)
    photos = StoryPhotoSerializer(many=True)
    user_id = serializers.IntegerField(source="user.id")
    author_name = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = (
            "id",
            "title",
            "content",
            "location",
            "haunting_types",
            "photos",
            "user_id",
            "author_name",
            "is_owner",
            "created_at",
        )

    def get_author_name(self, obj):
        first_initial = obj.user.first_name[:1]
        return f"{first_initial}. {obj.user.last_name}"

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request and obj.user == request.user
