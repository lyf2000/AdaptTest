# Generated by Django 2.2 on 2019-04-27 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('startpage', '0006_auto_20190423_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionresult',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='startpage.Question'),
        ),
    ]