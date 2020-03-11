from django.test import TestCase, Client
from django.urls import reverse
from posts.models import User, Follow, Post, Comment
# Авторизованный пользователь может подписываться на других пользователей и удалять их из подписок.
# Только авторизированный пользователь может комментировать посты.
# Create your tests here.
class ProfileTest(TestCase):    
    def setUp(self):
        self.client = Client()
        self.user = {"username": "testemail", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        response = self.client.post(reverse("signup"), self.user, follow=True)

    def test_profile(self):
        response = self.client.get("/testemail/")
        self.assertEqual(response.status_code, 200)
      
    def test_auth_follow(self):
        self.client.login(username="testemail", password="Test123456")
        self.user = User.objects.get(username='testemail')
        self.author = User.objects.create(username='author')
        response = self.client.get("/author/follow", follow=True)  
        follow = Follow.objects.get(user=self.user, author=self.author) # создается Follow
        self.assertTrue(follow)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/author/unfollow', follow=True)
        unfollow = Follow.objects.filter(user=self.user, author=self.author)
        self.assertFalse(unfollow)    
        self.assertEqual(response.status_code, 200)

    def test_auth_comment(self):
        self.client.login(username="testemail", password="Test123456")
        self.user = User.objects.get(username='testemail')
        self.post = Post.objects.create(text='New text', author = self.user)
        self.client.post(f"/testemail/{self.post.pk}/comment/", {"text": "First comment"})
        comment = Comment.objects.get(post=self.post, author=self.user)
        response = self.client.get(f"/testemail/{self.post.pk}/")   
        self.assertContains(response, f"{comment.text}")
