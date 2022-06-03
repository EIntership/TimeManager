# Generated by Django 3.2.13 on 2022-06-03 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('managers', '0015_auto_20220602_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='hash',
            field=models.CharField(default='821566f9b95b4ae49086c106faec4df5', editable=False, max_length=32),
        ),
        migrations.CreateModel(
            name='ProjectUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managers.project')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
