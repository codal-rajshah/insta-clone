from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from apps.users.factories import UserFactory, ApplicationFactory, AccessTokenFactory
from apps.friends.models import FriendRequest, Friend
from apps.friends.factories import FriendFactory, FriendRequestFactory


class TestFriendRequests(APITestCase):
    """
    Tests following APIs
    1. Sending friend request
    2. Accepting friend request
        -> 403 response if you don't have permission
        -> 200 response on success
    3. Rejecting friend request
        -> 403 response if you don't have permission
        -> 200 response on success
    """
    def test_friend_request_create(self):
        friend1 = UserFactory.create(
            username='friend1'
        )
        friend2 = UserFactory.create(
            username='friend2'
        )
        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=friend1,
            application=application
        )

        headers = {
            "Authorization": f"Bearer {access_token.token}"
        }

        url = reverse('friendrequest-list')
        data = {'to_user': friend2.username}
        response = self.client.post(
            url,
            data,
            headers=headers
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # Check if object created in DB
        self.assertTrue(
            FriendRequest.objects.filter(
                from_user=friend1,
                to_user=friend2,
                accepted=False
            ).exists()
        )

    def test_friend_request_accept(self):
        friend1 = UserFactory.create(
            username='friend1'
        )
        friend2 = UserFactory.create(
            username='friend2'
        )
        friend_request = FriendRequestFactory.create(
            from_user=friend1,
            to_user=friend2
        )

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=friend1,
            application=application
        ).token

        url = reverse('friendrequest-accept-request', kwargs={'pk': friend_request.id})

        bad_response = self.client.post(
            url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        self.assertEqual(
            bad_response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        access_token = AccessTokenFactory.create(
            user=friend2,
            application=application
        ).token

        success_response = self.client.post(
            url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        self.assertEqual(
            success_response.status_code,
            status.HTTP_200_OK
        )
        self.assertTrue(
            FriendRequest.objects.filter(
                from_user=friend1,
                to_user=friend2,
                accepted=True
            ).exists()
        )
        self.assertTrue(
            Friend.objects.filter(
                user=friend1,
                friend=friend2
            ).exists()
        )

    def test_friend_request_reject(self):
        friend1 = UserFactory.create(
            username='friend1'
        )
        friend2 = UserFactory.create(
            username='friend2'
        )
        friend_request = FriendRequestFactory.create(
            from_user=friend1,
            to_user=friend2
        )

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=friend1,
            application=application
        ).token

        url = reverse('friendrequest-reject-request', kwargs={'pk': friend_request.id})

        bad_response = self.client.post(
            url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        self.assertEqual(
            bad_response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        access_token = AccessTokenFactory.create(
            user=friend2,
            application=application
        ).token

        success_response = self.client.post(
            url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        self.assertEqual(
            success_response.status_code,
            status.HTTP_200_OK
        )
        self.assertFalse(
            FriendRequest.objects.filter(
                from_user=friend1,
                to_user=friend2,
                accepted=True
            ).exists()
        )


class TestFriends(APITestCase):
    """
    Tests following APIs
    1. Friend list
    2. Add close friend
    3. Remove close friend
    4. Remove friend
    """
    def test_friend_list(self):
        user1 = UserFactory.create(username='user1')
        user2 = UserFactory.create(username='user2')
        user3 = UserFactory.create(username='user3')

        friendship1 = FriendFactory.create(user=user1, friend=user2)
        friendship2 = FriendFactory.create(user=user1, friend=user3)

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user1,
            application=application
        ).token

        url = reverse('friends-list')
        response = self.client.get(
            url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = response.json()
        original_friend_ids = [friendship1.id, friendship2.id]
        response_friend_ids = [d['friend_id'] for d in data]
        self.assertListEqual(response_friend_ids, original_friend_ids)

    def test_add_close_friend(self):
        user1 = UserFactory.create(username='user1')
        user2 = UserFactory.create(username='user2')

        friendship = FriendFactory.create(user=user1, friend=user2)

        url = reverse('friends-add-close-friend', kwargs={'pk': friendship.id})
        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user1,
            application=application
        ).token

        response = self.client.put(
            url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Friend.objects.filter(
                user=user1,
                friend=user2,
                is_close_friend=True
            ).exists()
        )

    def test_remove_close_friend(self):
        user1 = UserFactory.create(username='user1')
        user2 = UserFactory.create(username='user2')

        friendship = FriendFactory.create(
            user=user1,
            friend=user2,
            is_close_friend=True,
        )

        url = reverse('friends-remove-close-friend', kwargs={'pk': friendship.id})
        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user1,
            application=application
        ).token

        response = self.client.put(
            url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Friend.objects.filter(
                user=user1,
                friend=user2,
                is_close_friend=True
            ).exists()
        )

    def test_remove_friend(self):
        user1 = UserFactory.create(username='user1')
        user2 = UserFactory.create(username='user2')

        friendship = FriendFactory.create(
            user=user1,
            friend=user2
        )

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user1,
            application=application
        ).token

        url = reverse('friends-remove-friend', kwargs={'pk': friendship.id})
        response = self.client.delete(
            url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Friend.objects.filter(user=user1, friend=user2).exists()
        )
        self.assertFalse(
            FriendRequest.objects.filter(from_user=user1, to_user=user2).exists()
        )
