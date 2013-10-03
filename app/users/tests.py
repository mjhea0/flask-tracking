from flask import url_for

from app.bases import BaseTestCase
from app.users.models import User

class UserViewsTests(BaseTestCase):
    def test_users_can_login(self):
        User.create(name="Joe", email="joe@joes.com", password="12345")
        response = self.client.post("/login", data={"name": "Joe", "password": "12345"},
                                    follow_redirects=True)

        self.assert_200(response)
        self.assertEquals(url_for("index", _external=True), response.location)
