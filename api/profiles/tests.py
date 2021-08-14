# from django.test import TestCase
import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles.api.serializers import ProfileSerializer, ProfileStatusSerializer
from profiles.models import Profile, ProfileStatus

# Create your tests here.


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "test", "email": "test@gmail.com",
                "password1": "testpassword", "password2": "testpassword"}
        response = self.client.post("/api/rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):

    list_url = reverse('profile-list')

    def setUp(self):
        self.user = User.objects.create_user(
            username="testname",
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse('profile-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "testname")

    def test_profile_update_by_owner(self):
        response = self.client.put(
            reverse('profile-detail', kwargs={'pk': 1}),
            {"city": "Klang, Selangor", "bio": "Genius"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {"id": 1,
             "user": "testname",
             "city": "Klang, Selangor",
             "bio": "Genius",
             "avatar": None
             }
        )

    def test_profile_update_by_not_owner(self):
        not_owner = User.objects.create_user(
            username="notowner",
            password="notownerpassword",
        )
        self.client.force_authenticate(user=not_owner)
        response = self.client.put(
            reverse('profile-detail', kwargs={'pk': 1}),
            {"city": "Hacked!", "bio": "Hacked!"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProfileStatusViewSetTestCase(APITestCase):

    list_url = reverse('status-list')

    def setUp(self):
        self.user = User.objects.create_user(
            username="testname",
            password="testpassword"
        )
        self.status = ProfileStatus.objects.create(
            user_profile=self.user.profile,
            status_content="status test"
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_profile_status_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_status_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_status_create(self):
        data = {"status_content": "a new status!"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_profile"], "testname")
        self.assertEqual(response.data["status_content"], "a new status!")

    def test_single_status_retrieve(self):
        serializer_data = ProfileStatusSerializer(instance=self.status).data
        response = self.client.get(reverse("status-detail", kwargs={'pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)

        self.assertEqual(serializer_data, response_data)

    def test_status_update_by_owner(self):
        data = {"status_content": "content updated"}
        response = self.client.put(
            reverse("status-detail", kwargs={'pk': 1}),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status_content"], "content updated")
    
    def test_status_update_not_by_owner(self):
        
        not_owner = User.objects.create_user(
            username="notowner",
            password="notownerpassword",
        )
        self.client.force_authenticate(user=not_owner)

        data = {"status_content": "Hacked!"}
        response = self.client.put(
            reverse("status-detail", kwargs={'pk': 1}),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
       
