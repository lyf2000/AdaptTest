# Generated by Django 2.2 on 2019-04-23 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('startpage', '0005_auto_20190423_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionresult',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='startpage.Question'),
        ),
    ]
