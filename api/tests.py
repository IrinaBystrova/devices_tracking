import json
from api.models import Project, Devices, DeviceAPIKeys, ProjectMembership, ProjectMembershipAPIKeys, Releases
from django.test import TestCase, Client
from django.urls import reverse


client = Client()


class ReleaseApiTest(TestCase):
    """ Test module for API """
    device_error = {
        'success': False, 'error': 'Device object does not exist'
    }

    member_error = {
        'success': False, 'error': 'Member object does not exist'
    }

    def setUp(self):
        self.mars = Project.objects.create(name='mars')
        self.venus = Project.objects.create(name='venus')

        self.device_one = Devices.objects.create(name='Opportunity', project_obj=self.mars)
        self.device_two = Devices.objects.create(name='Curiosity', project_obj=self.mars)
        self.device_three = Devices.objects.create(name='venus-1', project_obj=self.venus)
        self.device_for = Devices.objects.create(name='venus-2', project_obj=self.venus)

        self.device_one_key = DeviceAPIKeys.objects.create(device=self.device_one)
        self.device_two_key = DeviceAPIKeys.objects.create(device=self.device_two)
        self.device_three_key = DeviceAPIKeys.objects.create(device=self.device_three)
        self.device_for_key = DeviceAPIKeys.objects.create(device=self.device_for)

        self.member_one = ProjectMembership.objects.create(name='member_one', project_obj=self.mars,
                                                           email='test@test.com')
        self.member_two = ProjectMembership.objects.create(name='member_two', project_obj=self.venus,
                                                           email='test@test.com')

        self.member_one_key = ProjectMembershipAPIKeys.objects.create(member=self.member_one)
        self.member_two_key = ProjectMembershipAPIKeys.objects.create(member=self.member_two)

        self.release_one = Releases.objects.create(device=self.device_one, version='1.0.0')
        self.release_two = Releases.objects.create(device=self.device_one, version='2.0.0')

    def test_get_version_wrong_params(self):
        response = client.get(reverse('api-get-version'), format='json')
        self.assertEqual(response.data, self.device_error)
        self.assertEqual(response.status_code, 400)

        response = client.get(reverse('api-get-version'),
                              data={'device_id': self.device_one.id,
                                    'device_key': self.device_two_key.key,
                                    'project_name': 'mars'},
                              format='json')
        self.assertEqual(response.data, self.device_error)
        self.assertEqual(response.status_code, 400)

        response = client.get(reverse('api-get-version'),
                              data={'device_id': self.device_one.id,
                                    'device_key': self.device_one_key.key,
                                    'project_name': 'venus'},
                              format='json')
        self.assertEqual(response.data, self.device_error)
        self.assertEqual(response.status_code, 400)

    def test_get_version_success(self):
        response = client.get(reverse('api-get-version'),
                              data={'device_id': self.device_one.id,
                                    'device_key': self.device_one_key.key,
                                    'project_name': 'mars'},
                              format='json')
        result = json.loads(response.data)[0]['fields']
        self.assertEqual(self.release_two.device.id, result['device'])
        self.assertEqual(self.release_two.version, result['version'])
        self.assertEqual(response.status_code, 200)

    def test_get_versions_list_wrong_params(self):
        response = client.get(reverse('api-get-versions-list'), format='json')
        self.assertEqual(response.data, self.member_error)
        self.assertEqual(response.status_code, 400)

        response = client.get(reverse('api-get-versions-list'),
                              data={'member_name': self.member_one.name,
                                    'member_key': self.member_two_key.key,
                                    'project_name': 'mars'},
                              format='json')
        self.assertEqual(response.data, self.member_error)
        self.assertEqual(response.status_code, 400)

        response = client.get(reverse('api-get-versions-list'),
                              data={'member_name': self.member_one.name,
                                    'member_key': self.member_one_key.key,
                                    'project_name': 'venus'},
                              format='json')
        self.assertEqual(response.data, self.member_error)
        self.assertEqual(response.status_code, 400)

        response = client.get(reverse('api-get-versions-list'),
                              data={'member_name': self.member_one.name,
                                    'member_key': self.member_one_key.key,
                                    'project_name': 'mars',
                                    'device_id': self.device_one.id,
                                    'device_key': self.device_two_key.key},
                              format='json')
        self.assertEqual(response.data, self.device_error)
        self.assertEqual(response.status_code, 400)

    def test_get_versions_list_success(self):
        response = client.get(reverse('api-get-versions-list'),
                              data={'member_name': self.member_one.name,
                                    'member_key': self.member_one_key.key,
                                    'project_name': 'mars',
                                    'device_id': self.device_one.id,
                                    'device_key': self.device_one_key.key},
                              format='json')
        release_one = json.loads(response.data)[0]['fields']
        self.assertEqual(self.release_one.device.id, release_one['device'])
        self.assertEqual(self.release_one.version, release_one['version'])

        release_two = json.loads(response.data)[1]['fields']
        self.assertEqual(self.release_two.device.id, release_two['device'])
        self.assertEqual(self.release_two.version, release_two['version'])
        self.assertEqual(response.status_code, 200)
