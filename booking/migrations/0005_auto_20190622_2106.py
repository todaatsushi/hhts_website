# Generated by Django 2.2.2 on 2019-06-22 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20190622_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='age_group',
            field=models.CharField(choices=[('Family', '家族'), ('Adults', '大人'), ('Seniors', '高齢者'), ('Children / Adolescents', '子供・思春期'), ('Mixed', 'ミックス')], max_length=50, verbose_name='年齢層'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='transportation',
            field=models.CharField(choices=[('Train', '電車'), ('Coach', 'コーチ'), ('Car / Van', '自動車・バン'), ('Taxi', 'タクシ'), ('Other', '他の交通手段は後で伝えてください')], max_length=50, verbose_name='使う交通手段'),
        ),
    ]
