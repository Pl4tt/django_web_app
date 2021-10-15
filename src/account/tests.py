from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth

from .models import Account


class AccountTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {
            "email": "test.test@test.com",
            "username": "test_user",
            "password": "test_password"
        }
    
    def test_authentication(self):
        # check registration form
        response = self.client.post(reverse("account:register"), {
            "email": self.user_data.get("email"),
            "username": self.user_data.get("username"),
            "password1": self.user_data.get("password"),
            "password2": self.user_data.get("password"),
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # check if account exists in database
        account = Account.objects.get(pk=1)
        self.assertEqual(account.pk, 1)

        # check if client is logged in as himself
        client_user = auth.get_user(self.client)
        self.assertEqual(client_user, account)

        # check logout url
        response = self.client.get(reverse("account:logout"), follow=True)
        self.assertEqual(response.status_code, 200)

        # check if client is logged out
        client_user = auth.get_user(self.client)
        self.assertEqual(client_user.is_authenticated, False)

        # create new account
        user = Account.objects.create(email="test2.test2@test.com", username="test2_user", password="test2_password")
        self.assertEqual(user.pk, 2)

        # check @login_required decorator on settings
        response = self.client.get(reverse("account:settings", kwargs={"user_id": 2}))
        self.assertRedirects(response, "/login/?next=/settings/2/")

        # check valid login form
        response = self.client.post(reverse("account:login"), {
            "email": self.user_data.get("email"),
            "password": self.user_data.get("password"),
        })
        self.assertEqual(response.status_code, 302)

        # check if logged in user can't get access to someone else's account settings
        response = self.client.get(reverse("account:settings", kwargs={"user_id": 2}))
        self.assertTemplateUsed(response, "error.html")

        # check admin permissions
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)

    def test_follow_system(self):
        user_data = self.user_data
        client_user = Account.objects.create(email=user_data.get("email"), username=user_data.get("email"), password=user_data.get("password"))
        user2 = Account.objects.create(email="user2@test.com", username="user2", password="test_password")
        user3 = Account.objects.create(email="user3@test.com", username="user3", password="test_password")

        self.client.get(reverse("account:login"), {
            "email": user_data.get("email"),
            "password": user_data.get("password"),
        })
        
        # TODO