from django.urls import path, include
# level 1
# from profiles.api.views import ProfileList
# level 2
from profiles.api.views import (
    ProfileViewSet,
    ProfileStatusViewSet,
    AvatarUpdateView,
)
# level 3
from rest_framework.routers import DefaultRouter


# level 2
# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})

# level 3
router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"status", ProfileStatusViewSet)


urlpatterns = [
    # level 1
    # path("profiles/", ProfileList.as_view(), name="profile-list")
    # level 2
    # path("profiles/", profile_list, name="profile-list"),
    # path("profiles/<int:pk>/", profile_detail, name="profile-detail")
    # level 3
    path("", include(router.urls)),
    path("avatar/", AvatarUpdateView.as_view(), name="avatar-update")

]
