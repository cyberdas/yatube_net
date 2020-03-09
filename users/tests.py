from django.test import TestCase

# Create your tests here.
class Profile_test(self):

  def setUp(self):
        self.client = Client()
        self.user = {"username": "testemail", "password1": "Test123456", "password2": "Test123456", "email": "noodles00777@gmail.com"}
        response = self.client.post(reverse("signup"), self.user, follow=True)

  def test_profile(self):
        response = self.client.get("/testemail/")
        self.assertEqual(response.status_code, 200)