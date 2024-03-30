# Generated by Django 4.2.1 on 2023-06-26 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='collectedApprovedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CollectedApprovedBy', to=settings.AUTH_USER_MODEL),
        ),
    ]
