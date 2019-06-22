# Generated by Django 2.2.2 on 2019-06-22 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='duration',
            field=models.CharField(max_length=50, verbose_name='期間・分'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='extra_details',
            field=models.TextField(null=True, verbose_name='他に伝えたい情報'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='transportation',
            field=models.CharField(choices=[('使う交通手段', '使う交通手段'), ('電車', '電車'), ('コーチ', 'コーチ'), ('自動車・バン', '自動車・バン'), ('タクシ', 'タクシ'), ('その他', '他の交通手段は後で伝えてください')], max_length=50, verbose_name='使う交通手段'),
        ),
    ]
