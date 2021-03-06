# Generated by Django 3.1.3 on 2020-11-04 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people', models.IntegerField()),
                ('booking_date_time_start', models.DateTimeField()),
                ('booking_date_time_end', models.DateTimeField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.table')),
            ],
        ),
    ]
