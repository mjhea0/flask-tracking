from flask import url_for
from flask.ext.login import current_user

from app.bases import BaseTestCase
from app.users.models import User


class UserViewsTests(BaseTestCase):
    def test_users_can_login(self):
        User.create(name="Joe", email="joe@joes.com", password="12345")

        with self.client:
            response = self.client.post("/login/", data={"name": "Joe", "password": "12345"})

            self.assert_redirects(response, url_for("index"))
            self.assertTrue(current_user.name == "Joe")
            self.assertFalse(current_user.is_anonymous())

    def test_users_can_logout(self):
        User.create(name="Joe", email="joe@joes.com", password="12345")

        with self.client:
            self.client.post("/login/", data={"name": "Joe", "password": "12345"})
            self.client.get("/logout/")

            self.assertTrue(current_user.is_anonymous())

    def test_invalid_password_is_rejected(self):
        User.create(name="Joe", email="joe@joes.com", password="12345")

        with self.client:
            self.client.post("/login/", data={"name": "Joe", "password": "****"})

            self.assertTrue(current_user.is_anonymous())
