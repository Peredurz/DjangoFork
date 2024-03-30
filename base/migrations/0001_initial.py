# Generated by Django 4.2 on 2023-06-23 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Manufacturer', models.CharField(max_length=100)),
                ('Cures', models.TextField()),
                ('SideEffects', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(max_length=100)),
                ('Date_Of_Birth', models.DateField(blank=True, null=True)),
                ('BioText', models.TextField()),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(blank=True, null=True)),
                ('Collected', models.BooleanField(default=False)),
                ('CollectedApproved', models.BooleanField(default=False)),
                ('CollectedApprovedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CollectedApprovedBy', to=settings.AUTH_USER_MODEL)),
                ('Medition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.medicine')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
