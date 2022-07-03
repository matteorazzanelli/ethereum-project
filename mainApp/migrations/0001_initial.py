# Generated by Django 3.2.13 on 2022-06-25 16:10

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('times', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
