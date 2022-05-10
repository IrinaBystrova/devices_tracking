from api.models import Devices, DeviceAPIKeys, ProjectMembership, ProjectMembershipAPIKeys, Releases
from django.core import serializers
from django.db.models import Max
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


DEVICE_ERROR_MSG = 'Device object does not exist'
MEMBER_ERROR_MSG = 'Member object does not exist'


class ReleaseApiView(GenericViewSet):

    @staticmethod
    def check_device(device_id, device_key, project_name):
        device_key = DeviceAPIKeys.objects.filter(device_id=device_id, key=device_key).first()
        if not device_key:
            return

        device_obj = Devices.objects.filter(id=device_key.device_id, project_obj__name=project_name).first()
        if not device_obj:
            return

        return device_obj

    def get_device(self, request):
        params = request.query_params
        device_id = params.get('device_id')
        device_key = params.get('device_key')
        project_name = params.get('project_name')
        return self.check_device(device_id, device_key, project_name)

    @staticmethod
    def check_member(member_name, member_key, project_name):
        member_key = ProjectMembershipAPIKeys.objects.filter(member__name=member_name, key=member_key).first()
        if not member_key:
            return

        member = ProjectMembership.objects.filter(id=member_key.member_id, project_obj__name=project_name).exists()
        if not member:
            return

        return True

    def member_exists(self, request):
        params = request.query_params
        member_name = params.get('member_name')
        member_key = params.get('member_key')
        project_name = params.get('project_name')
        return self.check_member(member_name, member_key, project_name)

    @action(detail=False)
    def get_version(self, request, *args, **kwargs):
        """ Firmware updated event """
        device = self.get_device(request)
        if not device:
            return Response({'success': False, 'error': DEVICE_ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)

        version_id = Releases.objects.aggregate(max_date=Max('date_created'))
        version = Releases.objects.filter(device_id=device.id, date_created=version_id['max_date'])
        version = serializers.serialize('json', version)
        return Response(version, status=status.HTTP_200_OK, content_type='application/json')

    @action(detail=False)
    def get_versions_list(self, request, *args, **kwargs):
        """ List of firmware events per device """
        if not self.member_exists(request):
            return Response({'success': False, 'error': MEMBER_ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)

        device = self.get_device(request)
        if not device:
            return Response({'success': False, 'error': DEVICE_ERROR_MSG}, status=status.HTTP_400_BAD_REQUEST)

        versions = Releases.objects.filter(device_id=device.id).order_by('date_created')
        versions = serializers.serialize('json', versions)
        return Response(versions, status=status.HTTP_200_OK)
