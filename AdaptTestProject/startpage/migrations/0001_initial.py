# Generated by Django 2.2 on 2019-04-14 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MyTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answers_num', models.PositiveIntegerField(default=0)),
                ('all_answers_num', models.PositiveIntegerField(default=0)),
                ('question_text', models.CharField(max_length=250)),
                ('lvl', models.PositiveSmallIntegerField(default=1)),
                ('correct_answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='correct_answer', to='startpage.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=100)),
                ('questions_number', models.PositiveIntegerField()),
                ('user_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mytest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startpage.MyTest')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='startpage.Question')),
                ('selected_answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='startpage.Answer')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test', to='startpage.Test'),
        ),
        migrations.AddField(
            model_name='mytest',
            name='test',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='startpage.Test'),
        ),
        migrations.AddField(
            model_name='mytest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startpage.Question'),
        ),
    ]
