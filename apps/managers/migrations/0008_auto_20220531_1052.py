# Generated by Django 3.2.13 on 2022-05-31 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0007_auto_20220531_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='user',
            new_name='users',
        ),
        migrations.AlterField(
            model_name='company',
            name='hash',
            field=models.CharField(default='3f71cab862b3400783cfe9ed24323b76', editable=False, max_length=32),
        ),
    ]
