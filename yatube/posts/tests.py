from django.test import TestCase
from django.core import mail
from django.test import Client
from .models import Post
# После регистрации пользователя создается его персональная страница (profile)
# Авторизованный пользователь может опубликовать пост (new)
# Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
# После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице пользователя (profile), и на отдельной странице поста (post)
# Авторизованный пользователь может отредактировать свой пост и его содержимое изменится на всех связанных страницах
# Create your tests here.
class ProfileTest(TestCase):

    def setUp(self):
        self.client = Client()
        user = {"username": "Projecttest", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        self.client.post("/auth/signup/", user, follow=True) # зашли на сайт как пользователь

    def testRegistration(self):
        response = self.client.get("/Projecttest/")
        self.assertEqual(response.status_code, 200, msg="Page not found")

class NewPostTest(TestCase):
    
    def setUp(self):
        self.client = Client()

    def testNewPost(self):
        data = {"text": "text for testing"}
        response = self.client.post("/new/", data, follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/")

    def testRedirect(self):
        response = self.client.get("/new/", follow=True)  # пользователь редиредиректится на страницу авторизации
        self.assertRedirects(response, "/auth/login/?next=/new/", status_code=302, target_status_code=200)

class ConnectedPosts(TestCase):

    def setUp(self):
        self.client = Client()
        user = {"username": "Projecttest", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        self.client.post("/auth/signup/", user, follow=True)
        post = Post.objects.create(text="My post!", author=user)

    def testShowPost(self):
        pass

    def testEditPost(self):
        response = self.client.get("/ProjectTest/1/edit") 
        form = response.context['post']
        data = form(initial={'text':'My post!'})
        data['text'] = 'Edited'
        self.client.post("/ProjectTest/1/edit", data)

class EmailTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = {"username": "testemail", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        self.client.post("/auth/signup/", user, follow=True)

    def test_send_email(self): 
        self.assertEqual(len(mail.outbox), 1) # Проверяем, что письмо лежит в исходящих
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение регистрации Yatube') # Проверяем, что тема первого письма правильная.
