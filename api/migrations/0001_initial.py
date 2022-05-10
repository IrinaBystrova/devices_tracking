# Generated by Django 2.2 on 2022-05-09 08:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NameModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=180, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('namemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.NameModel')),
            ],
            bases=('api.namemodel',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('namemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.NameModel')),
            ],
            bases=('api.namemodel',),
        ),
        migrations.CreateModel(
            name='ProjectMembership',
            fields=[
                ('namemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.NameModel')),
                ('email', models.EmailField(max_length=254)),
                ('project_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Project')),
            ],
            bases=('api.namemodel',),
        ),
        migrations.CreateModel(
            name='Releases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('version', models.CharField(max_length=180, validators=[django.core.validators.RegexValidator(code='invalid_version', message='Version must match *SemVer 2.0*', regex='^\\d+(\\.\\d+){2,3}$')])),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Devices')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMembershipAPIKeys',
            fields=[
                ('keymodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.KeyModel')),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.ProjectMembership')),
            ],
            bases=('api.keymodel',),
        ),
        migrations.CreateModel(
            name='DeviceAPIKeys',
            fields=[
                ('keymodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.KeyModel')),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Devices')),
            ],
            bases=('api.keymodel',),
        ),
        migrations.AddField(
            model_name='devices',
            name='project_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Project'),
        ),
    ]
