# Generated by Django 5.0.1 on 2024-05-04 19:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0002_alter_hformation_personnel'),
    ]

    operations = [
        migrations.CreateModel(
            name='HConge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeconges', models.CharField(max_length=50)),
                ('dateDeb', models.DateField()),
                ('dateFin', models.DateField()),
                ('observation', models.CharField(max_length=50)),
                ('personnel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Application.personnel')),
            ],
            options={
                'db_table': 'T_HConge',
            },
        ),
    ]
