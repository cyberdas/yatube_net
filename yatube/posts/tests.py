from django.test import TestCase, Client
from django.core import mail
from .models import Post, User
from django.urls import reverse
# После регистрации пользователя создается его персональная страница (profile)
# Авторизованный пользователь может опубликовать пост (new)
# Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
# После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице пользователя (profile), и на отдельной странице поста (post)
# Авторизованный пользователь может отредактировать свой пост и его содержимое изменится на всех связанных страницах
# Create your tests here.

class ProjectTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = {"username": "testemail", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        response = self.client.post(
            reverse("signup"), self.user, follow=True
        ) # регистрация
        self.assertRedirects(response, "/auth/login/", status_code=302, target_status_code=200)
        response = self.client.post("auth/login/", {"username": "testemail", "password": "Test123456"}, follow=True)

    def test_profile(self):
        response = self.client.get("/testemail/")
        self.assertEqual(response.status_code, 200)

    def test_logout(self): # неавторизованный пользователь не может опубликовать пост
        self.client.logout()
        response = self.client.get("/new/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/", status_code=302, target_status_code=200) 

    def test_user(self):
        self.client.login(username="testemail", password="Test123456")
        self.client.post(reverse("new_post"), {"text": "Новый текст поста"}, follow=True) # публикуем пост
        self.user = User.objects.get(username='testemail')
        self.post = Post.objects.get(author=self.user)
        test_urls = ("/", f'/{self.user.username}/', f'/{self.user.username}/{self.post.pk}/')
        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, "Новый текст поста", count=1, html=False)  # страницы содержат текст поста

    def edit_post(self):
        self.client.login(username="testemail", password="Test123456")
        self.user = User.objects.get(username='testemail')
        self.post = Post.objects.create(text="New text", author=self.user)
        self.client.post(f"/{self.user.username}/{self.post.pk}/edit", {"text": "Измененный текст"})
        test_urls = ("/", f'/{self.user.username}/', f'/{self.user.username}/{self.post.pk}/')
        for url in test_urls:
            response = response = self.client.get(url)
            self.assertContains(response, "Измененный текст", count=1)

class EmailTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = {"username": "testemail", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        self.client.post("/auth/signup/", user, follow=True)

    def test_send_email(self): 
        self.assertEqual(len(mail.outbox), 1) # Проверяем, что письмо лежит в исходящих
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение регистрации Yatube') # Проверяем, что тема первого письма правильная.
