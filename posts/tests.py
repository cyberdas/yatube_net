from django.test import TestCase, Client, override_settings
from django.core import mail
from .models import Post, User, Group, Follow
from django.urls import reverse
from django.core.cache import cache


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache',}})
class ProjectTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = {"username": "testemail", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        response = self.client.post(
            reverse("signup"), self.user, follow=True
        )
        self.assertRedirects(response, "/auth/login/", status_code=302, target_status_code=200)
        response = self.client.post("auth/login/", {"username": "testemail", "password": "Test123456"}, follow=True)

    def test_logout(self):
        self.client.logout()
        response = self.client.get("/new/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/", status_code=302, target_status_code=200) 

    def test_user(self):
        self.client.login(username="testemail", password="Test123456")
        self.client.post("/new/", {"text": "Новый текст поста"}, follow=True)
        self.user = User.objects.get(username='testemail')
        self.post = Post.objects.get(author=self.user)
        test_urls = ("/", f'/{self.user.username}/', f'/{self.user.username}/{self.post.pk}/')
        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, "Новый текст поста", count=1)

    def edit_post(self):
        self.client.login(username="testemail", password="Test123456")
        self.user = User.objects.get(username='testemail')
        self.post = Post.objects.create(text="New text", author=self.user)
        self.client.post(f"/{self.user.username}/{self.post.pk}/edit/", {"text": "Измененный текст"})
        test_urls = ("/", f'/{self.user.username}/', f'/{self.user.username}/{self.post.pk}/')
        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, "Измененный текст")

    def test_image(self):
        self.client.login(username="testemail", password="Test123456")
        self.user = User.objects.get(username='testemail')
        self.group = Group.objects.create(title="TestGroup", slug="testimage", description='desc')
        with open('C:/Users/1/Desktop/python/проекты_черновые/final_project/media/posts/image.jpg', 'rb') as fp:
            self.client.post("/new/", {"group": "1", 'text': 'Test post', 'image': fp})
        urls = ("/", f"/{self.user.username}/", f'/{self.user.username}/1/', '/group/testimage/')
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, '<img')
        with open('C:/Users/1/Desktop/python/Команднаястрока.rtf', 'rb') as fp:
            self.client.post('/new/', {'group': '1','text': 'Test post', 'image': fp})
        response = self.client.get("/testemail/")
        self.assertNotEqual(response.context["my_posts"], 2)


    def test_follow_post(self):
        self.client.login(username="testemail", password="Test123456")
        self.author = User.objects.create(username="author")
        self.user = User.objects.get(username='testemail')
        self.post = Post.objects.create(text="New text", author=self.author)
        self.follow = Follow.objects.create(user=self.user, author=self.author)
        response = self.client.get("/follow/")
        self.assertContains(response, "New text")

    def test_unfollow_post(self):
        self.client.login(username="testemail", password="Test123456")
        self.author = User.objects.create(username="author")
        self.post = Post.objects.create(text="New text", author=self.author)
        response = self.client.get("/follow/")
        self.assertNotContains(response, "New text")

class EmailTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = {"username": "testemail", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        self.client.post("/auth/signup/", user, follow=True)

    def test_send_email(self):
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение регистрации Yatube')


class ServerTest(ProjectTest):

    def test_error_404(self):
        response = self.client.get('/404/')
        self.assertEqual(response.status_code, 404)


class CacheTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="TestUser", email="mail@mail.ru", password="Zxc123")
        self.client.login(username='TestUser', password='Zxc123')

    def test_cache_index(self):
        self.client.get("/")
        self.post = Post.objects.create(text="Test post", author=self.user)
        response = self.client.get("/")
        self.assertNotContains(response, "Test post")
        cache.clear()
        response = self.client.get("/")
        self.assertContains(response, "Test post")
