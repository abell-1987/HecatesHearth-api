from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from HecatesHearthapi.models import Story, StoryPhoto, HauntingType


class StoryPhotoView(ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        photos = StoryPhoto.objects.all().order_by("-uploaded_at")

        story_id = request.query_params.get("story_id")
        location_id = request.query_params.get("location_id")
        user_id = request.query_params.get("user_id")
        haunting_type_id = request.query_params.get("haunting_type_id")

        if story_id:
            photos = photos.filter(story_id=story_id)

        if location_id:
            photos = photos.filter(location_id=location_id)

        if user_id:
            photos = photos.filter(user_id=user_id)

        if haunting_type_id:
            photos = photos.filter(haunting_types__id=haunting_type_id)

        serializer = StoryPhotoSerializer(
            photos, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        photo = StoryPhoto.objects.get(pk=pk)
        serializer = StoryPhotoSerializer(photo, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        story = Story.objects.get(pk=request.data["story_id"])

        if story.user != request.user:
            return Response(
                {"message": "You can only add photos to your own stories."},
                status=status.HTTP_403_FORBIDDEN,
            )

        photo = StoryPhoto.objects.create(
            story=story,
            location=story.location,
            user=request.user,
            image=request.FILES["image"],
        )

        photo.haunting_types.set(story.haunting_types.all())

        serializer = StoryPhotoSerializer(photo, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        photo = StoryPhoto.objects.get(pk=pk)

        if photo.user != request.user:
            return Response(
                {"message": "You can only delete your own photos."},
                status=status.HTTP_403_FORBIDDEN,
            )

        photo.image.delete(save=False)
        photo.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PhotoStateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    abbreviation = serializers.CharField()
    name = serializers.CharField()


class PhotoLocationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    city = serializers.CharField()
    state = PhotoStateSerializer()


class PhotoStorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class PhotoHauntingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HauntingType
        fields = ("id", "name")


class StoryPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    location = PhotoLocationSerializer()
    story = PhotoStorySerializer()
    haunting_types = PhotoHauntingTypeSerializer(many=True)

    class Meta:
        model = StoryPhoto
        fields = (
            "id",
            "story",
            "location",
            "user",
            "image",
            "image_url",
            "haunting_types",
            "uploaded_at",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
