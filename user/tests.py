import json

from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, force_authenticate

from user.models import User
from user.views import UserDataTableView


class DatatableTests(TestCase):

    def setUp(self) -> None:
        self.adminUser = User.objects.create_user(
            username="admin",
            password="admin",
            first_name="Admin",
            last_name="Admin",
            mobile_number="+989375867152",
            is_kashef=True,
            is_superuser=True
        )

        self.factory = APIRequestFactory()

    def test_user_datatable(self):
        # add test subject to table
        User.objects.create_user(
            username="admin1",
            password="admin1",
            first_name="Admin1",
            last_name="Admin1",
            mobile_number="+989375867151",
            is_kashef=True
        )
        # test view
        view = UserDataTableView.as_view()
        # create request
        request = self.factory.post('/user/user/datatable/')
        # authenticate a user with required permissions
        force_authenticate(request, user=self.adminUser)
        # get response
        response = view(request)
        # assert is 200
        self.assertEqual(response.status_code, 200)
        # convert retrieved data to json
        response = json.loads(response.content.decode("utf-8"))
        # assert number of returned data match number of expected values
        self.assertEqual(2, len(response['data']))
        data = response['data'][0]
        # assert number of columns
        self.assertEqual(len(data), 8)
        # assert datatype
        types = tuple([type(i) for i in data])
        self.assertEqual(types, (str, str, str, str, str, str, str, str,))
