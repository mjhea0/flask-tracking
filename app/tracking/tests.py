from flask import url_for
from mock import Mock, patch

from app.bases import BaseTestCase
from app.users.models import User
from app.tracking.models import Site, Visit

import app.tracking.views


class TrackingViewsTests(BaseTestCase):
    def test_visitors_location_is_derived_from_ip(self):
        user = User.create(name="Joe", email="joe@joe.com", password="12345")
        site = Site.create(user_id=user.id)

        mock_geodata = Mock(name="get_geodata")
        mock_geodata.return_value = {
            'city': 'Los Angeles',
            'zipcode': '90001',
            'latitude': '34.05',
            'longitude': '-118.25'
        }

        url = url_for("tracking.register_visit", site_id=site.id)
        wsgi_environment = {"REMOTE_ADDR": "1.2.3.4"}

        with patch.object(app.tracking.views, "get_geodata", mock_geodata):
            with self.client:
                self.client.get(url, environ_overrides=wsgi_environment)

                visits = Visit.query.all()

                mock_geodata.assert_called_once_with("1.2.3.4")
                self.assertEquals(1, len(visits))
                self.assertEquals("Los Angeles, 90001", visits[0].location)
                self.assertEquals("Los Angeles, 90001, 34.05, -118.25",
                                  visits[0].location_full)
