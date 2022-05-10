import uuid
from django.core.validators import RegexValidator
from django.db import models


class NameModel(models.Model):
    name = models.CharField(max_length=180, editable=False, unique=True)


class KeyModel(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Project(NameModel):

    def __str__(self):
        return f'Project {self.name}'


class Devices(NameModel):
    project_obj = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'Device {self.name} {self.project_obj}'


class DeviceAPIKeys(KeyModel):
    device = models.OneToOneField(Devices, on_delete=models.CASCADE)


class ProjectMembership(NameModel):
    project_obj = models.ForeignKey(Project, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return f'Membership {self.name} {self.email} {self.project_obj}'


class ProjectMembershipAPIKeys(KeyModel):
    member = models.OneToOneField(ProjectMembership, on_delete=models.CASCADE)


class Releases(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Devices, on_delete=models.DO_NOTHING)
    version = models.CharField(max_length=180,
                               validators=[RegexValidator(regex='^\d+(\.\d+){2,3}$',
                                                          message='Version must match *SemVer 2.0*',
                                                          code='invalid_version')])

    def __str__(self):
        return f'{self.device} {self.version} {self.date_created}'
