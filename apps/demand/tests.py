from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.accounts.models import User
from django.core import management
from django.core.management.commands import loaddata


class AapiTests(APITestCase):

    def setUp(self):
        """
        Creates users for tests
        """
        anunciante = User.objects.create_user(
            email="anunciante@anunciante.com", password="admin123")
        anunciante.profile = 2
        anunciante.save()
        admin = User.objects.create_user(
            email="admin@admin.com", password="admin123")
        admin.profile = 1
        admin.save()

    def authAnnouncer(self):
        """
        Return JWT Token User Announcer
        """
        # announcer auth
        client = APIClient()
        url = reverse('auth')
        response = client.post(
            url, {"email": "anunciante@anunciante.com", "password": "admin123"}, format="json")
        return response.data.get('token')

    def test_create_user_announcer(self):
        """
        Ensure we can create a new user announcer object.
        """
        client = APIClient()
        url = reverse('auth')
        response = client.post(
            url, {"email": "admin@admin.com", "password": "admin123"}, format="json")
        jwt_admin_token = response.data.get('token')

        user_announcer_credentials = {
            "email": "anunciante@anunciante.com",
            "password": "admin123"
        }

        url = reverse('user_create')
        client.credentials(HTTP_AUTHORIZATION='JWT '+jwt_admin_token)

        body = {
            "profile": 2,
            "email": user_announcer_credentials['email'],
            "first_name": "",
            "last_name": "",
            "password":  user_announcer_credentials['password']
        }
        response = client.post(
            url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_uf(self):
        """
        Retrieve ufs
        """
        # loads uf and city list
        management.call_command(
            'loaddata', 'apps/demand/fixtures/uf_cities.json')

        # announcer auth
        client = APIClient()
        jwt_announcer_token = self.authAnnouncer()

        # list ufs without token
        url = reverse('uf_list')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT '+jwt_announcer_token)

        # list ufs with token
        response = client.get(url, format='json')
        self.assertGreater(response.data.__len__(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_city(self):
        """
        Test city listing by uf_id
        """
        # loads uf and city list
        management.call_command(
            'loaddata', 'apps/demand/fixtures/uf_cities.json')

        client = APIClient()
        jwt_announcer_token = self.authAnnouncer()

        url = reverse('city_list', args=['32'])

        # list cities by uf_id without token
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT '+jwt_announcer_token)

        # list cities by uf_id with token
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_demand(self):
        """
        Test demand CRUD api
        """
        # loads uf and city list
        management.call_command(
            'loaddata', 'apps/demand/fixtures/uf_cities.json')

        jwt_announcer_token = self.authAnnouncer()

        url = reverse('demand_create')
        data = {
            "description": "Descrição da demanda para indústria de droids",
            "address": {
                "street": "street",
                "number": "123",
                "complement": "complement",
                "sector": "sector",
                "zipcode": "12323333",
                "city_id": 5763,
                "uf_id": 32
            },
            "contacts": [
                {"name": "nome teste1", "phone": "12345678911"},
                {"name": "nome teste2", "phone": "12323233332"},
                {"name": "nome teste3", "phone": "12345678911"},
                {"name": "nome teste4", "phone": "12345678911"}
            ]
        }

        # create without token
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT '+jwt_announcer_token)

        # listing demand
        response = client.get(reverse('demand_list'), format='json')
        self.assertEqual(response.data.__len__(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # create with token
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        demand_id = response.data.get('id')

        # test listing
        response_list = client.get(reverse('demand_list'), format='json')
        self.assertEqual(response_list.data.__len__(), 1)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)

        data_updated = {
            "id": demand_id,
            "description": "ALTERADO descricao da demanda para industria de droids",
            "address": {
                "street": "ALTERADO",
                "number": "321",
                "complement": "complement",
                "sector": "ALTERADO",
                "zipcode": "47850000",
                "city_id": 5763,
                "uf_id": 32
            },
            "contacts": [
                {
                    "name": "nome teste4 ALTERADO",
                    "phone": "12345678911"
                },
            ],
        }

        # Update without token
        client.logout()
        url = reverse('demand_update_delete', args=[demand_id])
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Announcer auth
        jwt_announcer_token = self.authAnnouncer()
        client.credentials(HTTP_AUTHORIZATION='JWT '+jwt_announcer_token)

        # Update with token
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve demand with token
        response = client.get(reverse('demand_update_delete', args=[
                              demand_id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # delete demand with token
        response = client.delete(reverse('demand_update_delete', args=[
            demand_id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_demand_status(self):
        """
        Test demand status update
        """
        # loads uf and city list
        management.call_command(
            'loaddata', 'apps/demand/fixtures/uf_cities.json')

        jwt_announcer_token = self.authAnnouncer()

        url = reverse('demand_create')
        data = {
            "description": "Descrição da demanda para indústria de droids",
            "address": {
                "street": "street",
                "number": "123",
                "complement": "complement",
                "sector": "sector",
                "zipcode": "12323333",
                "city_id": 5763,
                "uf_id": 32
            },
            "contacts": [
                {"name": "nome teste1", "phone": "12345678911"},
                {"name": "nome teste2", "phone": "12323233332"},
                {"name": "nome teste3", "phone": "12345678911"},
                {"name": "nome teste4", "phone": "12345678911"}
            ]
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT '+jwt_announcer_token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        demand_id = response.data.get('id')
        response = client.get(reverse('demand_update_delete', args=[
            demand_id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('status'))

        data = {
            "id": demand_id,
            "status": True
        }
        response = client.patch(reverse('demand_status_update', args=[
            demand_id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(reverse('demand_update_delete', args=[
            demand_id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertTrue(response.data.get('status'))
