# Generated by Django 3.2.13 on 2022-05-31 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0006_auto_20220531_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='member',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='company',
            name='hash',
            field=models.CharField(default='8495f2b80137460c9bfbb743198ff5b3', editable=False, max_length=32),
        ),
    ]
