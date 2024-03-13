from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import UserProfile
from apps.users.factories import UserFactory, AccessTokenFactory, ApplicationFactory

from django.contrib.auth import get_user_model
User = get_user_model()


class TestUserCreation(APITestCase, TestCase):
    """
    Tests below APIs
    1. User creation
    """
    def setUp(self):
        super().setUp()
        self.user_creation_data = {
            "username": "test1",
            "email": "test1@codal.com",
            "password": "Codal@123"
        }

    def test_create_account(self):
        url = reverse('user-creation')
        repsonse = self.client.post(
            url,
            data=self.user_creation_data,
            format='json'
        )
        self.assertEqual(
            repsonse.status_code,
            status.HTTP_200_OK
        )
        email = self.user_creation_data['email']
        self.assertTrue(
            User.objects.filter(
                email=email
            ).exists()
        )
        self.user = User.objects.get(
            email=email
        )


class TestUserProfileCreation(APITestCase):
    """
    Tests below APIs
    1. User profile creation
    2. User profile image updation
    """
    def setUp(self):
        super().setUp()
        self.user_profile_data = {
            "name": "Test 1",
            "mobile_number": "9033304748",
            "date_of_birth": "1998-07-03"
        }

    def test_user_profile(self):
        user = UserFactory.create()
        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user,
            application=application
        )

        headers = {
            'Authorization': f'Bearer {access_token.token}'
        }

        url = reverse('user-profile', kwargs={'pk': user.id})
        response = self.client.post(
            url,
            data=self.user_profile_data,
            headers=headers,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertTrue(
            UserProfile.objects.filter(
                user=user
            ).exists()
        )

        # Test image upload
        profile_url = reverse('user-profile-image', kwargs={'pk': user.id})

        file_content = b'The file content'
        uploaded_file = SimpleUploadedFile('testfile.png', file_content)

        headers["Content-Disposition"] = "attachment; filename=testfile.png"

        response = self.client.post(
            profile_url,
            {'file': uploaded_file},
            headers=headers,
            format='multipart'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
