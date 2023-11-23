# Generated by Django 4.2.7 on 2023-11-23 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reclama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='Reclama')),
                ('time', models.TimeField(null=True)),
                ('link', models.CharField(max_length=500, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.admin')),
            ],
        ),
    ]
