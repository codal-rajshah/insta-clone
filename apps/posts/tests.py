from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.posts.models import Post, PostComment, PostLike
from apps.posts.factories import PostFactory
from apps.users.factories import (
    UserFactory,
    ApplicationFactory,
    AccessTokenFactory,
)
from apps.friends.factories import FriendFactory


class TestPostCreation(APITestCase):
    """
    Tests below APIs
    1. List of user created posts
    2. Post detail API
    3. Post file upload and metadata creation
    """

    def test_post_list(self):
        user = UserFactory.create()
        post1 = PostFactory.create(user=user)
        post2 = PostFactory.create(user=user)

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user, application=application
        ).token

        url = reverse("post-list")
        response = self.client.get(
            url, headers={"Authorization": f"Bearer {access_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_post_ids = [post1.id, post2.id]
        response_post_ids = sorted([p["id"] for p in response.json()])

        self.assertListEqual(created_post_ids, response_post_ids)

    def test_post_detail(self):
        user = UserFactory.create()
        post1 = PostFactory.create(user=user)
        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user, application=application
        ).token

        url = reverse("post-detail", kwargs={"pk": post1.id})
        response = self.client.get(
            url, headers={"Authorization": f"Bearer {access_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post1.id, response.json()["id"])

    def test_post_creation(self):
        user = UserFactory.create()
        application = ApplicationFactory.create()
        access_token = AccessTokenFactory(
            user=user, application=application
        ).token

        headers = {"Authorization": f"Bearer {access_token}"}

        url = reverse("post-upload-file")
        file_content = b"The file content"
        uploaded_file = SimpleUploadedFile("testfile.png", file_content)

        headers["Content-Disposition"] = "attachment; filename=testfile.png"
        response = self.client.post(
            url, {"file": uploaded_file}, headers=headers, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_id = response.json().get("id")

        # update created post
        update_url = reverse("post-detail", kwargs={"pk": post_id})
        update_data = {
            "caption": "Test Post",
            "location": "Location",
            "music": "Song",
            "hide_like_and_view_counts": False,
            "turn_off_comments": False,
            "audience": "friends",
        }

        headers.pop("Content-Disposition")
        update_response = self.client.put(
            update_url, data=update_data, headers=headers
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Post.objects.filter(
                caption="Test Post", location="Location", music="Song"
            ).exists()
        )


class TestFeed(APITestCase):
    """
    Tests below APIs
    1. Feed API
    """

    def test_feed_list_api(self):
        user1 = UserFactory.create(username="user1")
        user2 = UserFactory.create(username="user2")

        FriendFactory.create(user=user1, friend=user2)

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user1, application=application
        ).token

        PostFactory.create(user=user2)

        url = reverse("feed-list")

        response = self.client.get(
            url, headers={"Authorization": f"Bearer {access_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        results = response_data.get("results", [])
        self.assertEqual(len(results), 1)


class TestPostLikeUnlike(APITestCase):
    """
    Tests below APIs
    1. Post like
    2. Post unlike
    """

    def test_post_like(self):
        user1 = UserFactory.create(username="user1")
        user2 = UserFactory.create(username="user2")

        FriendFactory.create(user=user1, friend=user2)

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user1, application=application
        ).token

        post = PostFactory.create(user=user2)

        url = reverse("post-like")
        data = {"post": post.id, "action": "like"}

        response = self.client.post(
            url, data, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            PostLike.objects.filter(
                post=post, liked_by=user1, is_liked=True
            ).exists()
        )

    def test_post_unlike(self):
        user1 = UserFactory.create(username="user1")
        user2 = UserFactory.create(username="user2")

        FriendFactory.create(user=user1, friend=user2)

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user1, application=application
        ).token

        post = PostFactory.create(user=user2)

        url = reverse("post-like")
        data = {"post": post.id, "action": "unlike"}

        response = self.client.post(
            url, data, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            PostLike.objects.filter(
                post=post, liked_by=user1, is_liked=False
            ).exists()
        )


class TestPostComment(APITestCase):
    """
    Tests below APis
    1. Post comment
    """

    def test_post_comment(self):
        user1 = UserFactory.create(username="user1")
        user2 = UserFactory.create(username="user2")

        FriendFactory.create(user=user1, friend=user2)

        application = ApplicationFactory.create()
        access_token = AccessTokenFactory.create(
            user=user1, application=application
        ).token

        post = PostFactory.create(user=user2)

        url = reverse("post-comment-list")
        comment_text = "Test Comment"
        data = {"post": post.id, "comment": comment_text}

        response = self.client.post(
            url, data, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            PostComment.objects.filter(
                post=post, commented_by=user1, comment=comment_text
            ).exists()
        )
