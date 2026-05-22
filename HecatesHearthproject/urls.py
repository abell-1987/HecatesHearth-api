from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from HecatesHearthapi.views import (
    register_user,
    login_user,
    get_current_user,
    LocationView,
    StoryView,
    HauntingTypeView,
    StoryPhotoView,
    StateView,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"locations", LocationView, "location")
router.register(r"stories", StoryView, "story")
router.register(r"hauntingtypes", HauntingTypeView, "hauntingtype")
router.register(r"storyphotos", StoryPhotoView, "storyphoto")
router.register(r"states", StateView, "state")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("current_user", get_current_user),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
