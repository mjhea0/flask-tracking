from decimal import Decimal

from flask import url_for
from mock import Mock, patch
from werkzeug.datastructures import Headers

from flask_tracking.test_base import BaseTestCase
from flask_tracking.users.models import User
from .models import Site, Visit
from ..tracking import views


class TrackingViewsTests(BaseTestCase):
    def test_visitors_location_is_derived_from_ip(self):
        user = User.create(name='Joe', email='joe@joe.com', password='12345')
        site = Site.create(user_id=user.id)

        mock_geodata = Mock(name='get_geodata')
        mock_geodata.return_value = {
            'city': 'Los Angeles',
            'zipcode': '90001',
            'latitude': '34.05',
            'longitude': '-118.25'
        }

        url = url_for('tracking.add_visit', site_id=site.id)
        wsgi_environment = {'REMOTE_ADDR': '1.2.3.4'}
        headers = Headers([('Referer', '/some/url')])

        with patch.object(views, 'get_geodata', mock_geodata):
            with self.client:
                self.client.get(url, environ_overrides=wsgi_environment,
                                headers=headers)

                visits = Visit.query.all()

                mock_geodata.assert_called_once_with('1.2.3.4')
                self.assertEqual(1, len(visits))

                first_visit = visits[0]
                self.assertEqual("/some/url", first_visit.url)
                self.assertEqual('Los Angeles, 90001', first_visit.location)
                self.assertEqual(Decimal("34.05"), first_visit.latitude)
                self.assertEqual(Decimal("-118.25"), first_visit.longitude)
