# Generated by Django 3.1.4 on 2020-12-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllureReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.JSONField()),
                ('report', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
