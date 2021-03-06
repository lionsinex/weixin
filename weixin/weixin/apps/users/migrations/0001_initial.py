# Generated by Django 2.1.7 on 2020-01-27 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
                ('birthday', models.DateTimeField(null=True)),
                ('gender', models.CharField(max_length=16, null=True)),
                ('avatar', models.CharField(max_length=1024, null=True)),
                ('signature', models.CharField(max_length=4096, null=True)),
                ('phone', models.BigIntegerField(unique=True)),
                ('email', models.CharField(max_length=128, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_robot', models.BooleanField(default=False)),
                ('is_boss', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('forbidden_end_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('is_robot', 'id')},
        ),
    ]
