# Generated by Django 3.2.13 on 2022-05-31 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0002_alter_company_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='hash',
            field=models.CharField(default='3849314b657242e99e4129636d0863a6', editable=False, max_length=32),
        ),
    ]
