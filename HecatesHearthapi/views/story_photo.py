from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from HecatesHearthapi.models import Story, StoryPhoto


class StoryPhotoView(ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        photos = StoryPhoto.objects.all()

        location_id = request.query_params.get("location_id")
        user_id = request.query_params.get("user_id")

        if location_id:
            photos = photos.filter(location_id=location_id)

        if user_id:
            photos = photos.filter(user_id=user_id)

        serializer = StoryPhotoSerializer(
            photos, many=True, context={"request": request}
        )
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

        serializer = StoryPhotoSerializer(photo, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StoryPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = StoryPhoto
        fields = (
            "id",
            "story",
            "location",
            "user",
            "image",
            "image_url",
            "uploaded_at",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
