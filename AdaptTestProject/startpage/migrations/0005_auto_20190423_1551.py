# Generated by Django 2.2 on 2019-04-23 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('startpage', '0004_remove_test_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytest',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mytest_test', to='startpage.Test'),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_correct_answer', to='startpage.Answer'),
        ),
    ]