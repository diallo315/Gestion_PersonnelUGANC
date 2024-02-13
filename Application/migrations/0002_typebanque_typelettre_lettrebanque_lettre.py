# Generated by Django 4.2.7 on 2024-02-10 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeBanque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'T_TypeBanque',
            },
        ),
        migrations.CreateModel(
            name='TypeLettre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'T_TypeLettre',
            },
        ),
        migrations.CreateModel(
            name='LettreBanque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombanque', models.CharField(max_length=50)),
                ('numerobanque', models.CharField(max_length=50)),
                ('typebanque', models.CharField(max_length=50)),
                ('datejour', models.DateField()),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.personnel')),
            ],
            options={
                'db_table': 'T_LettreBanque',
            },
        ),
        migrations.CreateModel(
            name='Lettre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datejour', models.DateField()),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.personnel')),
                ('typelettre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.typelettre')),
            ],
            options={
                'db_table': 'T_Lettre',
            },
        ),
    ]
